---
name: harness-starter-workspace
description: |
  비개발자·초보자용 하네스 생성 스킬 (워크스페이스 도메인 — 분석·기획·문서·리서치).
  harness-100의 검증된 exemplar를 복제·치환하여 빠르고 안전하게 하네스를 만든다.
  3개의 객관식 질문만 받으며, 자유 설계 대신 template 복제 전략을 사용한다.
  "쉽게 하네스 만들어줘", "처음 만들어봐", "간단하게 팀 만들어줘", "템플릿으로 시작",
  "유튜브 팀 만들어줘", "블로그 팀", "계약서 검토 팀", "강의 만들기 팀",
  "비개발자", "코딩 모름", "starter harness", "easy harness", "template harness",
  표현 시 사용. 단, 코드·API·앱·데이터 파이프라인 등 코딩 도메인은
  harness-starter-coding 을 사용.

  호출 전에 사용자 의도를 3가지 관점(①도메인: 코딩·문서·혼합·검증 / ②숙련도: 처음·숙련·전문가 / ③목적: 시작·개선·검증)으로 간단히 확인한 뒤 진행한다. 사용자가 이미 명시한 경우 확인을 생략할 수 있다.
---

# Starter Harness Designer — Workspace v1

> "좋은 템플릿 하나가 100페이지 가이드보다 낫다."

## 이 스킬은 누구를 위한 것인가

- **처음 하네스를 만드는 사람**
- **개발자가 아닌 사람** (기획자·마케터·작가·변호사·교사·운영자 등)
- **빠르게 검증된 구조로 시작하고 싶은 사람**

전문가용 `harness-designer-workspace` 와 동일한 **Planner → Generator → Evaluator 3단 철학**을 유지하되,
각 단계의 입력 복잡도와 출력 정밀도만 초보자 수준으로 재배분했다.

| 단계 | 전문가용 | Starter (이 스킬) |
|------|---------|----------------|
| Planner | 4단계 Discovery, 개방형 질문 | **3개 객관식 질문** → exemplar 번호 매칭 |
| Generator | 설계안 → 파일·구조 생성 | **exemplar 복제 + 치환** |
| Evaluator | 8대 기둥 독립 검증 | **경량 체크리스트** — 치환 누락·깨진 참조만 |

---

## 스킬과 다른 하네스 스킬의 관계

```
              │ 전문가 (자유 설계)            │ 초보자 (exemplar 복제)
──────────────┼─────────────────────────────┼────────────────────────────
 워크스페이스  │ harness-designer-workspace  │ harness-starter-workspace ★ (이 스킬)
──────────────┼─────────────────────────────┼────────────────────────────
 코딩         │ harness-designer-coding     │ harness-starter-coding
```

**이 스킬을 쓰면 안 되는 경우**
- 앱·웹서비스·API 개발 → `harness-starter-coding`
- 설계 자유도가 필요한 고급 사용자 → `harness-designer-workspace`
- 단순 질문·1회성 작업 → 스킬 사용 불필요

---

## 실행 흐름 (전체 5분)

```
1. [Planner] 3개 객관식 질문
2. [Planner] exemplar 번호 매칭 + 프리셋 추천
3. [Generator] harness-100 exemplar 복제
4. [Generator] 프로젝트명·도메인 용어 치환
5. [Evaluator] 경량 체크리스트 (5초)
6. 완료 안내 ("이제 이렇게 쓰세요")
```

---

# Phase 0: Pattern Match (Planner)

## 질문 1 — 무슨 일을 시키고 싶나요? (자연어 1문장)

사용자에게 1문장으로 받는다. 예:
- "유튜브 영상 하나 만들 때 기획·대본·썸네일까지 팀이 해줬으면"
- "계약서 받으면 위험조항 뽑아주는 팀"
- "매달 뉴스레터 발송 자동화"

## 질문 2 — 가장 가까운 카테고리는? (객관식 8개)

[references/exemplar-index.md](./references/exemplar-index.md) 참조. 아래 8개 중 선택:

| 번호 | 카테고리 | 예시 |
|-----|--------|------|
| 1 | 🎬 콘텐츠 제작 | 유튜브, 팟캐스트, 뉴스레터, 만화, 번역 |
| 4 | 📊 비즈니스·전략 | 스타트업, 시장조사, 가격책정, 재무모델 |
| 5 | 🎓 교육·학습 | 언어튜터, 시험대비, 커리큘럼 설계 |
| 6 | ⚖️ 법률·컴플라이언스 | 계약서, 특허, GDPR/개인정보 |
| 7 | 🏃 라이프스타일 | 식단, 피트니스, 세무, 여행 |
| 8 | 📝 커뮤니케이션·문서 | 테크니컬라이팅, SOP, 제안서 |
| 9 | 🏢 운영·프로세스 | 채용, 온보딩, 감사, 구매 |
| 10 | 🌐 특화 도메인 | 부동산, ESG, IP포트폴리오 |

질문 1의 키워드로 **자동 추천 1~3개**를 제시하고, 사용자가 확인만 하면 된다.

**매칭 실패 처리** (유사도 < 0.5):
- 가장 가까운 후보 3개를 제시하고 "이 중 어느 것이 가장 가까운가요?" 재질문
- 모두 아니면 `harness-designer-workspace` (전문가용) 로 전환 안내

## 질문 3 — 프로젝트 이름은?

폴더명·파일명으로 쓸 수 있게 짧게 (예: `youtube-production`, `contract-review`, `monthly-newsletter`).

## 질문 4 — 변경 이력을 남길까요? (선택, yes/no)

"나중에 이 팀을 개선할 때 **무엇이·왜 바뀌었는지**를 기록할 공간을 만들까요?"

- **yes** → `05-flow-history/` 위키 + `flow-change-protocol.md` 자동 생성 (초기 빌드는 change 0001로 기록)
- **no** → 생성 안 함 (나중에 수동 추가 가능)

용도: 팀 개선 회고, 롤백 시 근거 확인, 다른 유사 팀 만들 때 참고. 일상 사용에는 영향 없음.

**관리 원칙**: 이 이력은 워크플로우 시스템(규칙·절차·도구·CLAUDE.md)의 변화만 기록한다.
시스템이 만들어낸 산출물(리서치 결과·보고서·분석·어젠다 등록)은 기록 대상이 아니다.
구별 기준: "이 변경이 없었더라면 다음에 실행하는 결과가 달라지는가?"
→ 달라진다 = 시스템 변경 = 기록 / 달라지지 않는다 = 산출물 = 기록 불필요
상세: `00-system/protocols/flow-change-protocol.md`

### Question 3.5 (조건부 — 연구 계열 카테고리만)

> 📊 Business & Strategy, 🎓 Education & Learning, 🌐 Specialized Domains 카테고리 선택 시에만 표시.
> 콘텐츠 제작 등 비연구 카테고리에서는 스킵.

"여러 어젠다를 진행하며 기존 연구를 참조할 필요가 있습니까?"
- 예 → wiki 포함:
  - /graphify 스킬 설치 확인 (자동: ~/.claude/skills/graphify/ 또는 .claude/skills/graphify/)
  - 미설치 시 설명 + 설치 선택 (전역/프로젝트/미설치)
  - ⚠️ 미설치 선택 시: "wiki 기능은 비활성. 나중에 /graphify 설치 후 /wiki-update로 생성 가능"
- 아니오 → wiki 불포함

---

# Phase 1: Preset 선택 (평가 가중치)

매칭 완료 후 **프리셋 3종** 중 추천 + 확인:

| 프리셋 | 설명 | 자동 추천 기준 |
|-------|------|-------------|
| **[균형]** (기본) | 모든 품질 기준 균등 | 기본값 |
| **[품질우선]** | Reviewer·테스트시나리오·NOT-trigger 2배 가중 | 법률·의료·재무·IP 카테고리 |
| **[속도우선]** | Scale Mode=Single, 경량 체크리스트만 | 1회성 프로토타입·1인 작업 |

선택된 프리셋은 `_workspace/00_input.md`에 기록된다.

---

# Phase 2: Generator — exemplar 복제·치환

## 복제 단계 (자동 fallback)

`gh` 유무를 자동 감지하여 최적 방식으로 다운로드한다. `git`만 있어도 동일하게 작동.

```bash
EXEMPLAR="{NN}-{exemplar-name}"   # Planner 매칭 결과 (예: 01-youtube-production)
BASE="ko/$EXEMPLAR/.claude"

if command -v gh &>/dev/null && gh auth status &>/dev/null 2>&1; then
  # ── 방식 A: GitHub CLI (gh) ──────────────────────────────
  echo "📡 gh api 방식으로 다운로드..."
  FILES=$(gh api "repos/revfactory/harness-100/git/trees/main?recursive=1" \
    --jq ".tree[] | select(.path | startswith(\"$BASE/\")) | select(.type==\"blob\") | .path")
  mkdir -p .claude/agents .claude/skills
  while IFS= read -r filepath; do
    rel="${filepath#$BASE/}"
    dest=".claude/$rel"
    mkdir -p "$(dirname "$dest")"
    gh api "repos/revfactory/harness-100/contents/$filepath" \
      --jq '.content' | base64 -d > "$dest"
    echo "  ✅ $dest"
  done <<< "$FILES"
else
  # ── 방식 B: git sparse checkout (gh 없을 때) ─────────────
  echo "📡 git sparse checkout 방식으로 다운로드..."
  TMP=$(mktemp -d)
  git clone --depth 1 --filter=blob:none --sparse \
    https://github.com/revfactory/harness-100.git "$TMP"
  git -C "$TMP" sparse-checkout set "$BASE"
  mkdir -p .claude
  cp -r "$TMP/$BASE/." .claude/
  rm -rf "$TMP"
  echo "  ✅ sparse checkout 완료"
fi
```

| 조건 | 사용 방식 | 필요 도구 |
|------|---------|---------|
| `gh` 설치 + 로그인 | 방식 A (gh api) | gh |
| `git` 만 있을 때 | 방식 B (sparse checkout) | git |
| 둘 다 없거나 실패 | 방식 C (사용자 확인 후 Claude 직접 생성) | 없음 |

방식 A·B 모두 실패 시 Claude가 사용자에게 직접 안내한다:

> ⚠️ **GitHub에서 템플릿을 가져올 수 없습니다.**
>
> 원인: `gh`와 `git` 모두 사용 불가 또는 인터넷 미연결 상태입니다.
>
> 이 경우 Claude가 exemplar 인덱스 설명을 참고하여 하네스 파일을 직접 작성할 수 있습니다.
> 단, 실제 검증된 템플릿이 아니라 Claude가 구조를 재현하는 것이므로 품질 차이가 있을 수 있습니다.
>
> **계속 진행할까요?**
> - **예** → Claude가 `.claude/` 파일 직접 생성 (exemplar-index.md 기반)
> - **아니오** → 여기서 중단. 인터넷 연결 또는 git 설치 후 다시 시도해 주세요.

사용자가 **예** 선택 시: `references/exemplar-index.md`의 해당 exemplar 설명을 읽고 CLAUDE.md, agents/, skills/ 구조를 직접 작성.
사용자가 **아니오** 선택 시: 즉시 중단, 재시도 방법 안내 후 종료.

완료 후 구조:
```
.claude/
├── CLAUDE.md
├── agents/
│   ├── {specialist-1}.md
│   ├── {specialist-2}.md
│   ├── {specialist-3}.md
│   ├── {specialist-4}.md
│   └── {reviewer}.md
└── skills/
    ├── {orchestrator}/skill.md
    └── {agent-extending}/skill.md
```

3. `_workspace/` 폴더 생성 (산출물용, 번호 컨벤션 `00_input.md`, `01_*.md`, ...)

## 치환 규칙

| 원본 요소 | 치환 내용 | 예시 |
|---------|---------|------|
| 하네스 이름 | 사용자 프로젝트명 | `01-youtube-production` → `my-youtube-show` |
| 도메인 용어 (전역) | 사용자 도메인 용어 | "YouTube 영상" → "팟캐스트 에피소드" |
| 트리거 키워드 | 사용자 도메인 키워드 | 유튜브 관련 → 팟캐스트 관련 |
| 에이전트 역할명 | 필요시만 치환 | `scriptwriter` → 유지 권장 |
| 도메인 프레임워크 | **절대 유지** | Porter's·IRAC·Bloom's는 핵심 전문성 |
| `_workspace/NN_*.md` | 유지 (번호 컨벤션) | 절대 번호 바꾸지 말 것 |

**추가 폴더 구조 (v2)**:
- `50-reports/[어젠다명]/v[N]/report.md` — 어젠다별 격리된 보고서
- `60-exports/[어젠다명]/` — 파생 산출물 (슬라이드, 외부 공유 등)
- CARL frontmatter: `agenda:`, `type:`, `tags:` YAML frontmatter를 70-playbook/ 템플릿에 포함
- (wiki 선택 시) `45-wiki/` — knowledge graph 저장소
- (wiki 선택 시) `research-wiki` 스킬 — 독립성 보호 wiki 참조
- (wiki 선택 시) `/wiki-update` 커맨드 — wiki 생성·업데이트
- (질문 4 yes 시) `05-flow-history/` + `00-system/protocols/flow-change-protocol.md` — 플로우 변경 이력 위키. `~/.claude/skills/harness-designer-workspace/references/flow-history-template.md` 참조하여 5+1개 파일 생성.

**자동 치환 금지 목록**:
- 임베디드 프레임워크명 (AIDA, IRAC, Bloom's, ADDIE, Porter's, DCF, Van Westendorp, SMART 등)
- `_workspace/` 디렉토리명과 산출물 번호
- `SendMessage`, `TaskCreate` 등 프로토콜 용어
- Scale Modes 정의
- `45-wiki/` 디렉토리명
- `research-wiki` 스킬명
- independence-protocol wiki 참조 규칙 텍스트
- bkit 자동 수정: Domain frameworks(AIDA·IRAC·Bloom's 등), independence-protocol, SendMessage 프로토콜, `_workspace/` 번호 체계는 bkit 에이전트(code-analyzer, pm-lead 등) 제안으로 수정 금지
- 루프 요소: 완료 기준(종료 조건), Reviewer 검토 순서(Reviewer가 마지막), review_report의 판정 형식 — 치환·삭제 금지 (루프는 Goal+Check+종료 조건이 있어야 성립)

## 용어 평문화 (사용자 설명용, 내부 구조는 유지)

내부 파일은 원어 유지. 사용자에게 설명할 때만 평문화:

| 원어 | 평문 |
|-----|------|
| Orchestrator | 팀장 |
| Agent-Extending Skill | 전문 지식 책자 |
| Dependency DAG | 작업 순서표 |
| Scale Modes | 팀 규모 모드 |
| Trigger Boundaries | 호출 조건 |
| Cross-validation | 교차 검토 |

---

# Phase 3: Evaluator — 경량 체크리스트

전문가용 스킬의 8대 기둥 검증 대신, **치환 무결성**만 확인한다.

## 자동 체크 (5초)

- [ ] `.claude/CLAUDE.md` 존재
- [ ] `agents/` 안에 4~5개 `.md` 파일 존재 (Reviewer 포함)
- [ ] `skills/<orchestrator>/skill.md` 존재
- [ ] `skills/` 안에 agent-extending 스킬 최소 1개 존재
- [ ] `_workspace/` 폴더 생성됨
- [ ] 원본 하네스명(예: `01-youtube-production`)이 파일 내부에 **잔존하지 않음** (grep 0건)
- [ ] 임베디드 프레임워크명 **보존됨** (IRAC/Bloom's 등 원본 수치와 동일)
- [ ] Trigger Boundaries의 `should-NOT` 섹션 존재
- [ ] Scale Modes 표 존재 (Full / Reduced / Single)
- [ ] 3가지 테스트 시나리오 섹션 존재 (Normal / Existing / Error)
- [ ] 50-reports/에 어젠다별 폴더 구조 존재
- [ ] 60-exports/ 폴더 존재 (파생 산출물 분리)
- [ ] 70-playbook/ CARL 템플릿에 frontmatter 포함
- [ ] /synthesize 커맨드에 잔여과제 필수 게이트 포함
- [ ] orchestrator skill.md에 체크 가능한 완료 기준(종료 조건) 존재
- [ ] Reviewer 산출물(review_report)이 통과/수정필요 판정을 포함하는 형식임
- [ ] (wiki 선택 시) 45-wiki/ 폴더 존재
- [ ] (wiki 선택 시) research-wiki 스킬 존재
- [ ] (wiki 선택 시) independence-protocol에 wiki 참조 규칙 존재

## 실패 시

- 치환 누락 발견 → Planner에 재질문 ("어떤 용어로 바꿀까요?")
- 구조적 결손 → 해당 exemplar 재복제 후 다시 치환
- 3회 실패 → `harness-designer-workspace` 전환 안내

---

# Phase 4: 완료 안내 (비개발자용 평문 리포트)

```
✅ 하네스가 준비됐어요!

📁 위치: /your-project/.claude/
👥 팀 구성 (5명):
   - 전략가: 주제 발굴·경쟁분석
   - 대본작가: 실제 대본 작성
   - 썸네일 디자이너: 이미지 기획
   - SEO 담당자: 검색 최적화
   - 검토자: 전체 품질 검증

🚀 사용법:
   1. Claude Code에서 "/my-youtube-show 다음 영상 기획해줘" 입력
   2. 팀이 순서대로 작업, _workspace/ 폴더에 산출물 저장
   3. 결과물은 00_input.md ~ 05_review_report.md 순서

🔄 팀이 일하는 방식 (루프):
   팀은 "목표(Goal) → 작업 → 검토(Check) → 통과 시 완료"의 루프로 돕니다.
   마지막 검토자 리포트(0X_review_report.md)가 검증 결과예요.
   결과가 마음에 안 들면 구체적으로 다시 요청하세요 —
   그 최종 판단이 당신의 역할(outer loop)입니다.

📘 다음 단계:
   - 마음에 안 드는 부분이 있으면 .claude/agents/{역할}.md 를 수정
   - 더 복잡하게 만들고 싶다면 harness-designer-workspace 스킬 사용
```

---

# 참고 자료

- [exemplar-index.md](./references/exemplar-index.md) — 73개 워크스페이스 exemplar 인덱스
- 원본: https://github.com/revfactory/harness-100 (Apache-2.0)
- 전문가용 변형: `harness-designer-workspace`
- 코딩용 변형: `harness-starter-coding`
