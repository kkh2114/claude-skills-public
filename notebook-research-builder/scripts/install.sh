#!/usr/bin/env bash
# notebook-research-builder 설치 시작점 (macOS·Linux·WSL)
#   bash scripts/install.sh [--check] [--skip a,b] [--login] [--agent claude|codex|both]
# uv(파이썬·도구 관리자)만 확보한 뒤, 나머지 탐색·설치는 setup.py가 한다. 파이썬이 없어도 uv가 받아 온다.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"

if command -v uv >/dev/null 2>&1; then
  echo "✓ uv: 이미 설치됨 ($(uv --version)) — 건너뜀"
elif [[ " $* " == *" --check "* ]]; then
  echo "✗ uv: 없음 (탐색 모드라 설치하지 않음)"; exit 2
else
  echo "… uv: 설치 중 (공식 설치 스크립트 https://astral.sh/uv/install.sh)"
  if command -v curl >/dev/null 2>&1; then curl -LsSf https://astral.sh/uv/install.sh | sh
  elif command -v wget >/dev/null 2>&1; then wget -qO- https://astral.sh/uv/install.sh | sh
  else echo "⚠ 사람 차례: curl 또는 wget을 먼저 설치하세요 (예: sudo apt-get install -y curl) → 다시 실행"; exit 2; fi
  export PATH="$HOME/.local/bin:$PATH"
  command -v uv >/dev/null 2>&1 || { echo "✗ uv 설치 후에도 찾을 수 없음 — 새 터미널에서 다시 실행"; exit 2; }
  echo "✓ uv: 설치 완료 ($(uv --version))"
fi

exec uv run --quiet --python ">=3.10" "$DIR/setup.py" "$@"
