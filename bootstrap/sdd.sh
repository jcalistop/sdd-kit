#!/usr/bin/env bash
# Wrapper CLI SDD
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/cli/sdd.py" "$@"
