#!/bin/bash
# install.sh — 스코프 기반 선별 설치 (skills-manifest.json 참조)
#
# 사용:
#   bash install.sh                       # scope=global 스킬만 ~/.claude/skills 에 설치 (권장)
#   bash install.sh --list                # 스코프 표만 출력, 설치 안 함
#   bash install.sh --all                 # 전부 설치 (비권장 — project 스킬이 전역 컨텍스트 차지)
#   bash install.sh --skill <이름>        # 특정 스킬 1개만 설치
#   bash install.sh --skill <이름> --to <프로젝트경로>/.claude/skills
#                                         # project 스킬을 해당 프로젝트에만 설치
#
# 원칙: scope=project 스킬은 전역(~/.claude/skills)에 깔지 않는다.
#        전역에 깔면 모든 세션의 스킬 목록에 실려 무관한 컨텍스트를 차지한다.

set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
MANIFEST="$ROOT/skills-manifest.json"
DEST="$HOME/.claude/skills"
MODE="global"
SKILL=""

while [ $# -gt 0 ]; do
    case "$1" in
        --list)  MODE="list" ;;
        --all)   MODE="all" ;;
        --skill) SKILL="$2"; MODE="one"; shift ;;
        --to)    DEST="$2"; shift ;;
        *) echo "알 수 없는 옵션: $1"; exit 1 ;;
    esac
    shift
done

PY=$(command -v python3 || command -v python || true)
[ -z "$PY" ] && { echo "python3가 필요합니다 (macOS: xcode-select --install / Ubuntu: sudo apt install python3)"; exit 1; }
"$PY" - "$MANIFEST" "$ROOT" "$DEST" "$MODE" "$SKILL" <<'EOF'
import json, shutil, sys
from pathlib import Path

manifest_path, root, dest, mode, skill = sys.argv[1:6]
manifest = json.loads(Path(manifest_path).read_text())["skills"]
root, dest = Path(root), Path(dest)

if mode == "list":
    print(f"{'스킬':34} {'scope':8} 출처/용도")
    print("-" * 90)
    for name, meta in manifest.items():
        print(f"{name:34} {meta['scope']:8} {meta['origin']}")
        dep = meta.get("dependsOn")
        if dep:
            print(f"{'':34} {'':8} └─ 의존(하드, 함께 설치): {', '.join(dep)}")
        odep = meta.get("optionalDependsOn")
        if odep:
            print(f"{'':34} {'':8} └─ 권장(소프트, 있으면 품질↑·함께 설치): {', '.join(odep)}")
    sys.exit(0)

targets = []
if mode == "global":
    targets = [n for n, m in manifest.items() if m["scope"] == "global"]
elif mode == "all":
    targets = list(manifest)
elif mode == "one":
    if skill not in manifest:
        sys.exit(f"매니페스트에 없는 스킬: {skill}")
    m = manifest[skill]
    if m["scope"] == "project" and str(dest).endswith("/.claude/skills") is False and ".claude" not in str(dest):
        print(f"⚠️  '{skill}' 은 scope=project ({m['origin']}) — 전역 설치는 컨텍스트를 낭비합니다.")
        print(f"   권장: bash install.sh --skill {skill} --to <프로젝트>/.claude/skills")
    targets = [skill]

# dependsOn(하드) + optionalDependsOn(소프트) 자동 포함 (전이적).
#  - 하드: 참조를 재사용 → 없으면 작동 안 함. 반드시 함께.
#  - 소프트: 없어도 작동하나 있으면 품질↑ → [권장]으로 함께.
def expand(names):
    seen, out, stack = set(), [], list(names)
    while stack:
        n = stack.pop(0)
        if n in seen:
            continue
        seen.add(n); out.append(n)
        for d in manifest.get(n, {}).get("dependsOn", []) + manifest.get(n, {}).get("optionalDependsOn", []):
            if d not in seen:
                stack.append(d)
    return out
requested = list(targets)
targets = expand(targets)
auto = [n for n in targets if n not in requested]
hard_names = {d for n in targets for d in manifest.get(n, {}).get("dependsOn", [])}
opt_names  = {d for n in targets for d in manifest.get(n, {}).get("optionalDependsOn", [])}
auto_hard = [n for n in auto if n in hard_names]
auto_opt  = [n for n in auto if n in opt_names and n not in hard_names]
if auto_hard:
    print(f"ℹ️  의존성 자동 포함(하드): {', '.join(auto_hard)} — 참조 재사용, 없으면 작동 안 함")
if auto_opt:
    print(f"ℹ️  권장 자동 포함(소프트): {', '.join(auto_opt)} — 없어도 작동하나 있으면 품질↑")

dest.mkdir(parents=True, exist_ok=True)
installed, skipped = [], []
for name in targets:
    src = root / name
    if not src.is_dir():
        skipped.append(name); continue
    shutil.copytree(src, dest / name, dirs_exist_ok=True)
    installed.append(name)

print(f"설치 완료 → {dest}")
for n in installed:
    tag = " [의존성 자동포함]" if n in auto_hard else (" [권장 자동포함]" if n in auto_opt else "")
    print(f"  ✅ {n} ({manifest[n]['scope']}){tag}")
for n in skipped:   print(f"  ⚠️  {n}: 폴더 없음 — 건너뜀")
posts = [(n, manifest[n]["postInstall"]) for n in installed if manifest[n].get("postInstall")]
if posts:
    print("\n▶ 설치 후 꼭 실행할 것 (스킬 폴더가 있는 이 저장소 위치에서):")
    for n, c in posts: print(f"  - {n}: {c}")
if mode == "global":
    projs = [n for n, m in manifest.items() if m["scope"] == "project"]
    if projs:
        print(f"\nscope=project 스킬 {len(projs)}개는 설치하지 않았습니다 (전역 컨텍스트 보호).")
        print("필요한 프로젝트에서만: bash install.sh --skill <이름> --to <프로젝트>/.claude/skills")
EOF
