#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

MODE="${CONTINUITY_PROBE_MODE:-static}"
BACKEND="${CONTINUITY_BACKEND:-cuda}"
BUILD_DIR="${CONTINUITY_BUILD_DIR:-build-continuity}"

echo "== DeepSeek Continuity Probe =="
echo "head=$(git rev-parse HEAD)"
echo "mode=$MODE backend=$BACKEND"

fail=0

require_path() {
  if [[ ! -e "$1" ]]; then
    echo "MISSING: $1"
    fail=1
  else
    echo "present: $1"
  fi
}

require_path src/dsv41
require_path include/strata/dsv41
require_path strata_control/dsv41_engine.py
require_path docs/DEEPSEEK41.md

if ! grep -R -n   --exclude-dir=.git   --exclude-dir="$BUILD_DIR"   -E 'option\(STRATA_BUILD_DSV41|add_executable\(strata-dsv41'   CMakeLists.txt cmake engine 2>/dev/null | head -n 20; then
  echo "MISSING: DSV41 CMake target declaration"
  fail=1
fi

if [[ $fail -ne 0 ]]; then
  exit 21
fi

if [[ "$MODE" == "static" ]]; then
  echo "STATIC PASS"
  exit 0
fi

rm -rf "$BUILD_DIR"

case "$BACKEND" in
  cuda)
    cmake -S . -B "$BUILD_DIR"       -DSTRATA_ENABLE_CUDA=ON       -DSTRATA_ENABLE_HIP=OFF       -DSTRATA_BUILD_DSV41=ON       -DSTRATA_BUILD_TESTS=ON
    ;;
  hip)
    cmake -S . -B "$BUILD_DIR"       -DSTRATA_ENABLE_CUDA=OFF       -DSTRATA_ENABLE_HIP=ON       -DSTRATA_BUILD_DSV41=ON       -DSTRATA_BUILD_TESTS=ON
    ;;
  *)
    echo "Unsupported CONTINUITY_BACKEND=$BACKEND (expected cuda or hip)"
    exit 22
    ;;
esac

cmake --build "$BUILD_DIR" --target strata-dsv41 -j"${CONTINUITY_JOBS:-2}"

if [[ "${CONTINUITY_RUN_PYTEST:-0}" == "1" ]]; then
  python3 -m pytest -q     tests/terminal/test_dsv41_engine.py     tests/terminal/test_dsv41_context.py     tests/terminal/test_launch_dsv41.py
fi

if [[ -n "${CONTINUITY_RUNTIME_CMD:-}" ]]; then
  echo "Running supplied real-model smoke test..."
  bash -lc "$CONTINUITY_RUNTIME_CMD"
fi

echo "BUILD/RUNTIME PASS"
