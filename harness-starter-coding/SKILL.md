---
name: harness-starter-coding
description: |
  비개발자·초보자용 하네스 생성 스킬 (코딩 도메인 — 웹앱·API·모바일·데이터/AI).
  harness-100의 검증된 exemplar를 복제·치환하여 빠르고 안전하게 하네스를 만든다.
  3개의 객관식 질문만 받으며, 자유 설계 대신 template 복제 전략을 사용한다.
  "쉽게 코딩 하네스 만들어줘", "처음 앱 만들어봐", "간단하게 개발 팀 만들어줘",
  "템플릿으로 웹앱 시작", "풀스택 팀 빠르게", "API 팀 템플릿", "ML 실험 팀",
  "비개발자 앱", "starter coding harness", "easy coding harness",
  표현 시 사용. 단, 문서·분석·기획 등 워크스페이스 도메인은
  harness-starter-workspace 를 사용.

  호출 전에 사용자 의도를 3가지 관점(①도메인: 코딩·문서·혼합·검증 / ②숙련도: 처음·숙련·전문가 / ③목적: 시작·개선·검증)으로 간단히 확인한 뒤 진행한다. 사용자가 이미 명시한 경우 확인을 생략할 수 있다.
---

# Starter Harness Designer — Coding v1

> "에이전트가 못한 건 능력 부족이 아니라, 환경이 부족했기 때문이다."

## 이 스킬은 누구를 위한 것인가

- **처음 코딩 하네스를 만드는 사람**
- **개발 팀을 꾸리고 싶은 비개발자 / 주니어**
- **검증된 풀스택·API·ML 템플릿으로 빠르게 시작하고 싶은 사람**

전문가용 `harness-designer-coding` 과 동일한 **Planner → Generator → Evaluator 3단 철학**을 유지하되,
각 단계의 입력 복잡도와 출력 정밀도만 초보자 수준으로 재배분했다.

| 단계 | 전문가용 | Starter (이 스킬) |
|------|---------|----------------|
| Planner | 4단계 Discovery, 개방형 질문 | **3개 객관식 질문** → exemplar 번호 매칭 |
| Generator | 설계안 → 파일·구조 생성 | **exemplar 복제 + 치환** |
| Evaluator | 8대 기둥 독립 검증 | **경량 체크리스트** — 치환 누락·깨진 참조만 |

---

## 스킬 매트릭스

```
              │ 전문가 (자유 설계)            │ 초보자 (exemplar 복제)
──────────────┼─────────────────────────────┼────────────────────────────
 워크스페이스  │ harness-designer-workspace  │ harness-starter-workspace
──────────────┼─────────────────────────────┼────────────────────────────
 코딩         │ harness-designer-coding     │ harness-starter-coding ★ (이 스킬)
```

**이 스킬을 쓰면 안 되는 경우**
- 문서·분석·콘텐츠 제작 → `harness-starter-workspace`
- 아키텍처 자유도가 필요한 고급 사용자 → `harness-designer-coding`
- 엔터프라이즈 마이크로서비스 → `enterprise` 스킬

---

## 실행 흐름 (전체 5~10분)

```
1. [Planner] 3개 객관식 질문 (앱 유형·데이터 성격·규모)
2. [Planner] exemplar 번호 매칭 + Scale Mode 추천 + 프리셋 추천
3. [Generator] harness-100 exemplar 복제
4. [Generator] 프로젝트명·기술스택·도메인 용어 치환
5. [Evaluator] 경량 체크리스트 (10초)
6. 완료 안내 ("이제 이렇게 개발하세요")
```

---

# Phase 0: Pattern Match (Planner)

## 질문 1 — 무엇을 만들고 싶나요? (객관식)

| 번호 | 앱 유형 | 대표 exemplar |
|-----|-------|-------------|
| 1 | 🌐 풀스택 웹앱 (프론트+백+DB) | #16-fullstack-webapp |
| 2 | 🔌 API 서버만 | #18-api-designer |
| 3 | 📱 모바일 앱 (iOS/Android) | #17-mobile-app-builder |
| 4 | 🗃️ 데이터 파이프라인·ETL | #27-data-pipeline |
| 5 | 🤖 AI/LLM 앱·RAG | #41-llm-app-builder |
| 6 | 🧪 ML 실험·모델 학습 | #31-ml-experiment |
| 7 | 🎨 디자인 시스템 (shadcn 기반) | #36-design-system |
| 8 | 🔐 보안 감사·침투테스트 | #28-security-audit |
| 9 | 🚀 CI/CD·인프라만 | #20-cicd-pipeline |
| 10 | ♻️ 레거시 현대화·리팩터링 | #22-legacy-modernizer |

## 질문 2 — 규모는? (객관식 → Scale Mode 자동 결정)

| 규모 | Scale Mode | 배치 에이전트 |
|-----|-----------|------------|
| 1인 MVP / 프로토타입 | **Single** | 가장 핵심 1명만 |
| 소규모 팀 / 1개월 이내 | **Reduced** | 3명 (architect + 핵심개발자 + qa) |
| 중규모 이상 / 프로덕션 | **Full** | 5명 (architect + frontend + backend + qa + devops) |

## 질문 3 — 프로젝트 이름은?

폴더명 기준. 기술 스택은 물어보지 않음 — exemplar의 **기본 스택을 그대로 사용**한다 (필요시 사용자가 나중에 교체).

**기본 스택 (교체 없이 진행)**:
- 풀스택: Next.js + Prisma + SQLite
- API: FastAPI 또는 Express
- 모바일: React Native (Expo)
- 데이터/ML: Python + pandas + scikit-learn
- RAG: Next.js + Vercel AI SDK + pgvector

## 질문 4 — 변경 이력을 남길까요? (선택, yes/no)

"나중에 이 하네스를 개선할 때 **무엇이·왜 바뀌었는지**를 기록할 공간을 만들까요?"

- **yes** → `05-flow-history/` 위키 + `00-system/protocols/flow-change-protocol.md` 자동 생성 (초기 빌드는 change 0001로 기록). 참조: `~/.claude/skills/harness-designer-workspace/references/flow-history-template.md`
- **no** → 생성 안 함 (나중에 수동 추가 가능)

용도: 플로우 개선 회고, 롤백 시 근거, 다른 유사 하네스 만들 때 참고. 1~2주 프로토타입에서는 no 권장.

**관리 원칙**: 이 이력은 워크플로우 시스템(프롬프트·프로토콜·템플릿·커맨드·CLAUDE.md)의 변화만 기록한다.
시스템이 만들어낸 산출물(코드·빌드 결과·배포 기록)은 기록 대상이 아니다.
구별 기준: "이 변경이 없었더라면 다음에 실행하는 결과가 달라지는가?"
→ 달라진다 = 시스템 변경 = 기록 / 달라지지 않는다 = 산출물 = 기록 불필요
상세: `00-system/protocols/flow-change-protocol.md`

---

# Phase 1: Preset 선택 (평가 가중치)

| 프리셋 | 설명 | 자동 추천 |
|-------|------|---------|
| **[균형]** (기본) | 모든 품질 기준 균등 | 기본값 |
| **[품질우선]** | OWASP·테스트·Reviewer 2배 가중 | 보안감사·결제·의료·금융 |
| **[속도우선]** | Scale=Single, 테스트 최소화 | 해커톤·1인 프로토타입 |

선택은 `_workspace/00_input.md`에 기록.

---

# Phase 2: Generator — exemplar 복제·치환

## 복제 단계 (자동 fallback)

`gh` 유무를 자동 감지하여 최적 방식으로 다운로드한다. `git`만 있어도 동일하게 작동.

```bash
EXEMPLAR="{NN}-{exemplar-name}"   # Planner 매칭 결과 (예: 16-fullstack-webapp)
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
│   ├── architect.md        — 요구·아키텍처·DB·API 설계
│   ├── frontend-dev.md     — React/Next.js (Scale에 따라 제거)
│   ├── backend-dev.md      — API·DB·Auth
│   ├── qa-engineer.md      — 테스트·코드리뷰 (Reviewer)
│   └── devops-engineer.md  — CI/CD·인프라 (Scale에 따라 제거)
└── skills/
    ├── {orchestrator}/skill.md
    ├── component-patterns/skill.md
    └── api-security-checklist/skill.md
```

3. **Scale Mode에 따라 에이전트 파일 삭제**:
   - Single → architect 1명만 (또는 가장 관련된 1명)
   - Reduced → architect + 핵심개발자 + qa
   - Full → 5명 전체
4. `_workspace/` 폴더 생성. 산출물 번호 컨벤션:
   - `00_input.md` — 조직된 사용자 입력
   - `01_architecture.md` — 아키텍처 설계
   - `02_api_spec.md` — API 명세
   - `03_db_schema.md` — DB 스키마
   - `04_test_plan.md` — 테스트 계획
   - `05_deploy_guide.md` — 배포 가이드
   - `06_review_report.md` — 리뷰 리포트

## 치환 규칙

| 원본 | 치환 | 비고 |
|-----|-----|-----|
| 하네스 이름 | 사용자 프로젝트명 | `16-fullstack-webapp` → `my-todo-app` |
| 기술 스택 (Next.js/Prisma 등) | 기본 유지 | 사용자가 명시한 경우만 교체 |
| 트리거 키워드 | 도메인 키워드 | "todo app" → 프로젝트 키워드 |
| `_workspace/NN_*.md` | 유지 | 번호 컨벤션 절대 변경 금지 |
| OWASP·SOLID·DORA 주입 | **절대 유지** | 도메인 전문성 핵심 |
| Scale Modes 표 | **유지** | Full/Reduced/Single 정의 보존 |
| `SendMessage` 프로토콜 | **유지** | 에이전트 간 통신 메커니즘 |

## Coding Agent Behavior Principles (Karpathy-inspired, 필수 삽입)

exemplar 복제 후 `.claude/CLAUDE.md` 끝부분에 **반드시** 아래 섹션을 추가한다 (치환 금지·보존 대상):

```markdown
## Coding Agent Behavior Principles (Karpathy-inspired)

모든 코딩 에이전트는 작업 시 아래 4원칙을 준수한다.
상세는 karpathy-guidelines 스킬 참조 (자동 트리거).

1. Think Before Coding — 가정 명시, 모호하면 질문, 대안 제시
2. Simplicity First — 요청한 만큼만. 사변적 추상화·기능 금지
3. Surgical Changes — 요청 라인만 변경. 주변 코드 개선 금지
4. Goal-Driven Execution — 검증 가능한 성공기준 → 루프 → 확인
```

Evaluator 경량 체크리스트에 "CLAUDE.md 내 Karpathy 4원칙 섹션 존재" 항목 추가.

## 치환 금지 목록

- 프레임워크명: OWASP Top 10, SOLID, DDD, Test Pyramid, DORA Metrics, CWE Top 25, Star/Snowflake Schema, SHAP/LIME, Great Expectations
- 프로토콜: SendMessage, TaskCreate, TaskUpdate
- 폴더 컨벤션: `_workspace/`, `src/`, 번호 접두사
- Scale Modes 정의
- 3 Test Scenarios 구조 (Normal / Existing / Error)
- bkit 자동 수정: Karpathy 4원칙, OWASP Top 10, DORA Metrics, Scale Modes는 bkit 에이전트(code-analyzer, pdca-iterator 등) 제안으로 수정 금지
- 루프 요소: 완료 기준(종료 조건), Reviewer(qa-engineer) 검토 순서, review_report의 판정 형식 — 치환·삭제 금지 (루프는 Goal+Check+종료 조건이 있어야 성립)

## 용어 평문화 (사용자 설명용)

| 원어 | 평문 |
|-----|------|
| architect | 설계자 |
| frontend-dev | 프론트 개발자 |
| backend-dev | 백엔드 개발자 |
| qa-engineer | 품질 검토자 |
| devops-engineer | 배포 담당자 |
| Dependency DAG | 작업 순서표 |
| Scale Mode | 팀 규모 |

내부 파일은 원어 유지, 사용자 대화만 평문.

---

# Phase 3: Evaluator — 경량 체크리스트

## 자동 체크 (10초)

- [ ] `.claude/CLAUDE.md` 존재
- [ ] `agents/` 파일 수가 Scale Mode와 일치 (Single=1, Reduced=3, Full=5)
- [ ] Reviewer 역할(qa-engineer) 포함됨
- [ ] `skills/<orchestrator>/skill.md` 존재
- [ ] agent-extending 스킬 최소 1개 (component-patterns 또는 api-security-checklist)
- [ ] `_workspace/` 폴더 + 번호 산출물 템플릿 생성됨
- [ ] OWASP·SOLID 등 프레임워크명 **보존** (grep으로 원본 개수 일치 확인)
- [ ] Trigger Boundaries `should-NOT` 섹션 존재
- [ ] Scale Modes 표 존재
- [ ] 3 Test Scenarios (Normal / Existing / Error) 섹션 존재
- [ ] 원본 exemplar 이름(예: `16-fullstack-webapp`) 잔존 **0건**
- [ ] (질문 4 yes 시) `05-flow-history/` 폴더 + `00-system/protocols/flow-change-protocol.md` 생성됨
- [ ] orchestrator skill.md에 체크 가능한 완료 기준(종료 조건) 존재
- [ ] Reviewer 산출물(review_report)이 통과/수정필요 판정을 포함하는 형식임

## 실패 시

- 치환 누락 → Planner 재질문
- 프레임워크 손실 → exemplar 재복제 후 치환
- 3회 실패 → `harness-designer-coding` 전문가용으로 전환 안내

---

# Phase 4: 완료 안내 (비개발자용 평문 리포트)

```
✅ 코딩 하네스가 준비됐어요!

📁 위치: /my-todo-app/.claude/
👥 개발 팀 (Reduced 모드, 3명):
   - 설계자(architect): DB·API 구조 설계
   - 백엔드 개발자: Next.js API + Prisma
   - 품질 검토자(qa): 테스트·코드리뷰

🛠️ 기본 스택: Next.js + Prisma + SQLite (교체 가능)

🚀 사용법:
   1. Claude Code에서 "투두앱 로그인 기능 만들어줘" 처럼 요청
   2. 팀이 순서대로 작업:
      설계자 → 백엔드 개발자 → 품질 검토자
   3. 결과물: _workspace/01_architecture.md ~ 06_review_report.md
   4. 소스 코드: src/ 폴더에 생성

🔒 보안·품질 기본 탑재:
   - OWASP Top 10 체크리스트 자동 적용
   - SOLID 원칙 기반 코드 리뷰
   - 3가지 테스트 시나리오 (정상·기존파일·에러)

🔄 팀이 일하는 방식 (루프):
   팀은 "목표(Goal) → 구현 → 검토(Check) → 통과 시 완료"의 루프로 돕니다.
   마지막 품질 검토자 리포트(06_review_report.md)가 검증 결과예요.
   결과가 마음에 안 들면 구체적으로 다시 요청하세요 —
   그 최종 판단이 당신의 역할(outer loop)입니다.

📘 다음 단계:
   - 팀을 5명으로 늘리고 싶다면 프론트·배포 담당자 추가 (Full 모드)
   - 고급 커스터마이징은 harness-designer-coding 스킬 사용
```

---

# 참고 자료

- [exemplar-index.md](./references/exemplar-index.md) — 27개 코딩 exemplar + Scale Modes + 프레임워크 인덱스
- 원본: https://github.com/revfactory/harness-100 (Apache-2.0)
- 전문가용 변형: `harness-designer-coding`
- 워크스페이스 변형: `harness-starter-workspace`
