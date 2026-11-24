#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / "lab"
CONFIG_PATH = LAB / "config.json"
STATE_DIR = ROOT / ".git" / "continuity-lab"
EVENTS_PATH = STATE_DIR / "events.jsonl"


@dataclass
class CmdResult:
    returncode: int
    stdout: str


def run(*args: str, check: bool = True, cwd: Path = ROOT) -> CmdResult:
    p = subprocess.run(
        list(args),
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if check and p.returncode:
        print(p.stdout, file=sys.stderr)
        raise subprocess.CalledProcessError(p.returncode, args, output=p.stdout)
    return CmdResult(p.returncode, p.stdout)


def git(*args: str, check: bool = True) -> CmdResult:
    return run("git", *args, check=check)


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def event(**payload) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with EVENTS_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def ensure_clean() -> None:
    status = git("status", "--porcelain").stdout.strip()
    if status:
        raise SystemExit(
            "Working tree is not clean. Commit/stash changes before replaying upstream.\n"
            + status
        )


def ensure_upstream(cfg: dict) -> None:
    remotes = git("remote").stdout.split()
    if "upstream" not in remotes:
        git("remote", "add", "upstream", cfg["upstream_url"])
    git("fetch", "upstream", "main", "--tags")


def first_parent_sequence(cfg: dict) -> list[str]:
    out = git(
        "rev-list",
        "--reverse",
        "--first-parent",
        f"{cfg['baseline_upstream_sha']}..{cfg['upstream_ref']}",
    ).stdout
    return [x for x in out.splitlines() if x]


def subject(sha: str) -> str:
    return git("show", "-s", "--format=%s", sha).stdout.strip()


def body(sha: str) -> str:
    return git("show", "-s", "--format=%B", sha).stdout.rstrip()


def parent_count(sha: str) -> int:
    parents = git("show", "-s", "--format=%P", sha).stdout.strip()
    return len(parents.split()) if parents else 0


def latest_replayed_sha(sequence: list[str]) -> str | None:
    # The continuity branch is a baseline snapshot, not a rewritten copy of
    # upstream ancestry, so progress is recorded in commit trailers.
    log = git("log", "--format=%B%x00").stdout
    known = set(sequence)
    for msg in log.split("\x00"):
        m = re.search(r"(?m)^Upstream-Commit:\s*([0-9a-f]{40})\s*$", msg)
        if m and m.group(1) in known:
            return m.group(1)
    return None


def slice_pending(sequence: list[str], last: str | None) -> list[str]:
    if last is None:
        return sequence
    try:
        i = sequence.index(last)
    except ValueError:
        raise SystemExit(
            f"Last replayed SHA {last} is not on the configured first-parent "
            "sequence. Inspect branch/upstream history before continuing."
        )
    return sequence[i + 1 :]


def commit_message(
    sha: str,
    prefix: str | None = None,
    extra: list[str] | None = None,
) -> str:
    original = body(sha)
    if prefix:
        lines = original.splitlines()
        first = lines[0] if lines else subject(sha)
        rest = "\n".join(lines[1:]).strip()
        original = f"{prefix} {first}"
        if rest:
            original += "\n\n" + rest

    trailers = [
        f"Upstream-Commit: {sha}",
        "Continuity-Lab: deepseek-retained",
    ]
    if extra:
        trailers.extend(extra)
    return original.rstrip() + "\n\n" + "\n".join(trailers) + "\n"


def git_path_exists_at_head(path: str) -> bool:
    return git("cat-file", "-e", f"HEAD:{path}", check=False).returncode == 0


def strip_filtered_paths(cfg: dict) -> list[str]:
    changed = git("diff", "--name-only", "--cached").stdout.splitlines()
    filters = tuple(cfg.get("filtered_path_prefixes", []))
    stripped: list[str] = []

    for path in changed:
        if not any(path == p.rstrip("/") or path.startswith(p) for p in filters):
            continue

        stripped.append(path)
        if git_path_exists_at_head(path):
            git("restore", "--source=HEAD", "--staged", "--worktree", "--", path)
        else:
            git("rm", "-f", "--cached", "--ignore-unmatch", "--", path, check=False)
            p = ROOT / path
            if p.is_file() or p.is_symlink():
                p.unlink(missing_ok=True)
            elif p.is_dir():
                import shutil
                shutil.rmtree(p)

    return stripped


def apply_without_commit(sha: str) -> CmdResult:
    if parent_count(sha) > 1:
        return git("cherry-pick", "-m", "1", "-n", sha, check=False)
    return git("cherry-pick", "-n", sha, check=False)


def conflict_files() -> list[str]:
    return [
        x
        for x in git(
            "diff", "--name-only", "--diff-filter=U", check=False
        ).stdout.splitlines()
        if x
    ]


def commit_current(msg: str, allow_empty: bool = False) -> None:
    args = ["commit"]
    if allow_empty:
        args.append("--allow-empty")
    args += ["-F", "-"]

    p = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        input=msg,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if p.returncode:
        print(p.stdout, file=sys.stderr)
        raise SystemExit(p.returncode)
    print(p.stdout.rstrip())


def run_probe(cfg: dict) -> int:
    command = cfg.get("probe_command", ["bash", "lab/tools/probe.sh"])
    p = subprocess.run(command, cwd=ROOT)
    return p.returncode


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Replay Strata integration history while retaining DeepSeek DSV41."
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="List pending commits and skip decisions without modifying the tree.",
    )
    ap.add_argument(
        "--no-probe",
        action="store_true",
        help="Replay commits without running the continuity probe.",
    )
    ap.add_argument(
        "--max",
        type=int,
        default=0,
        help="Stop after N pending upstream commits (0 = no limit).",
    )
    args = ap.parse_args()

    cfg = load_config()
    ensure_clean()
    ensure_upstream(cfg)

    sequence = first_parent_sequence(cfg)
    last = latest_replayed_sha(sequence)
    pending = slice_pending(sequence, last)
    if args.max > 0:
        pending = pending[: args.max]

    skip_re = re.compile(cfg["skip_subject_regex"], re.IGNORECASE)
    skip_shas = set(cfg.get("skip_commit_shas", []))

    def skip_reason(sha: str, sub: str) -> str | None:
        if sha in skip_shas:
            return "removal-integration-merge"
        if skip_re.search(sub):
            return "explicit-removal-commit"
        return None

    print(f"Baseline upstream SHA : {cfg['baseline_upstream_sha']}")
    print(f"Integration ref       : {cfg['upstream_ref']}")
    print(f"Last replayed         : {last or '(none)'}")
    print(f"Pending first-parent  : {len(pending)}")

    if args.dry_run:
        for sha in pending:
            sub = subject(sha)
            reason = skip_reason(sha, sub)
            tag = "SKIP-REMOVAL" if reason else "REPLAY"
            suffix = f"  [{reason}]" if reason else ""
            print(f"{tag:12} {sha[:12]}  {sub}{suffix}")
        return 0

    for index, sha in enumerate(pending, 1):
        sub = subject(sha)
        short = sha[:12]
        print(f"\n[{index}/{len(pending)}] {short} {sub}")

        reason = skip_reason(sha, sub)
        if reason:
            msg = commit_message(
                sha,
                prefix="[continuity-skip/removal]",
                extra=[
                    "Continuity-Classification: R0-explicit-removal-policy",
                    f"Continuity-Skip-Reason: {reason}",
                ],
            )
            commit_current(msg, allow_empty=True)
            event(
                kind="skip-removal",
                upstream_sha=sha,
                subject=sub,
                reason=reason,
            )
            continue

        result = apply_without_commit(sha)
        if result.returncode:
            files = conflict_files()
            event(
                kind="replay-conflict",
                upstream_sha=sha,
                subject=sub,
                conflict_files=files,
                output=result.stdout[-16000:],
            )
            print(result.stdout)
            print("\nReplay stopped at a real patch conflict.")
            print(
                "Classify it before resolving. A Git conflict alone is not evidence "
                "of an architecture break."
            )
            print("Conflict files:")
            for path in files:
                print(f"  - {path}")
            return 10

        stripped = strip_filtered_paths(cfg)
        git("add", "-A")
        has_changes = bool(
            git("diff", "--cached", "--name-only").stdout.strip()
        )

        extra: list[str] = []
        if stripped:
            extra.append(
                "Continuity-Filtered-Paths: " + ", ".join(stripped)
            )

        if has_changes:
            commit_current(commit_message(sha, extra=extra))
        else:
            extra.append("Continuity-Classification: R1-neutral-after-filter")
            commit_current(
                commit_message(
                    sha,
                    prefix="[continuity-empty]",
                    extra=extra,
                ),
                allow_empty=True,
            )

        if not args.no_probe:
            rc = run_probe(cfg)
            event(
                kind="probe",
                upstream_sha=sha,
                subject=sub,
                returncode=rc,
            )
            if rc:
                print(
                    f"\nProbe failed immediately after upstream commit {sha}."
                )
                print(
                    "HEAD is intentionally left at the failing replay commit "
                    "for inspection/bisection."
                )
                return 20

    print(
        "\nAll selected upstream integration commits survived the current "
        "replay/probe rules."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
