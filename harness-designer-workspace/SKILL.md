---
name: harness-designer-workspace
description: |
  어떤 도메인의 프로젝트든 하네스 구조로 설계·구축하는 메타 스킬.
  Layer 1(메타): Planner→Generator→Evaluator 순환으로 워크스페이스를 설계한다.
  Layer 2(운영): 완성된 구조 안에서 도메인 에이전트들이 실제 업무를 수행한다.
  두 레이어는 완전히 분리된다.
  Evaluator 90점+ PASS 후 cartesian-review 스킬을 자동 호출해
  데카르트 5렌즈(열거·명증·종합·분석·방법적 회의)로 추가 품질 검증을 수행한다.
  cartesian-review 스킬이 설치되어 있어야 이 단계가 활성화된다.
  "하네스 만들어줘", "워크스페이스 설계", "에이전트 시스템 구축",
  "CLAUDE.md 만들어줘", "프로젝트 구조 잡아줘", "Council 구조 만들어줘",
  "반복 가능한 시스템", "자동화 워크플로우", "멀티 에이전트", "독립 분석",
  "다각도 분석", "build a harness", "design workspace", "agent system"
  "~만들고 싶어" 수준의 막연한 아이디어(가치·범위 미검증)는 idea-to-spec 스킬이 있으면 그쪽이 먼저다 —
  이 스킬은 구조를 지을 때 쓰고,
  idea-to-spec의 spec-work/DEV_SPEC.md가 있으면 Discovery를 확인 모드로 시작한다.
  표현 시 반드시 사용.
---

# Harness Designer v4

> 원칙: "에이전트에게 지도를 줘라, 1000페이지 매뉴얼 말고." — OpenAI Harness Engineering
> 원칙: "생성자가 자기 작업을 평가하게 하지 마라." — Anthropic GAN-Inspired Harness

## 하네스 설계 5대 기둥

이 스킬이 생성하는 모든 워크스페이스는 다음 5가지 기둥을 충족해야 한다:

| 기둥 | 핵심 질문 | 원칙 |
|------|----------|------|
| **Progressive Disclosure** | 에이전트가 필요한 것만 볼 수 있는가? | 목차(~100줄) → 포인터 → 깊은 문서 |
| **Mechanical Enforcement** | 규칙이 기계적으로 강제되는가? | 문서화만으로는 일관성 유지 불가 |
| **Feedback Loop** | 실패 시 구조적 개선이 가능한가? | "더 열심히"가 아닌 "어떤 능력이 빠졌는가" |
| **Session Continuity** | 세션 간 핸드오프가 깨끗한가? | progress + feature-status + git |
| **Entropy Management** | 시간이 지나도 구조가 유지되는가? | 주기적 정리, 문서 신선도 검증 |

---

## 두 레이어의 관계

```
┌─────────────────────────────────────────────────────┐
│  LAYER 1: 메타 (이 스킬의 역할)                       │
│                                                     │
│  Planner ──→ Generator ──→ Evaluator                │
│     ↑         (단방향 순차, 역참조 금지)          │
│     └──── 미흡 시 피드백 ──────────────────────┘    │
│                                                     │
│  목적: 워크스페이스 구조 자체를 설계·생성·검증          │
└─────────────────────────┬───────────────────────────┘
                          │ 승인 후 구조 완성
                          ▼
┌─────────────────────────────────────────────────────┐
│  LAYER 2: 운영 (완성된 워크스페이스의 역할)             │
│                                                     │
│  ┌ Initializer (첫 실행 전용) ─→ 환경 설정           │
│  │                                                  │
│  └ Operating Agent (반복 실행):                      │
│    Agent-A ─┐                                       │
│    Agent-B ─┼──→ Chairman 종합 ──→ 최종 산출물       │
│    Agent-C ─┘  (독립 병렬, 서로 교류 없음)            │
│                                                     │
│  목적: 실제 업무 수행 (분석, 의사결정, 보고서 등)        │
└─────────────────────────────────────────────────────┘
```

---

# LAYER 1: 메타 — 하네스 설계 프로세스

## L1 에이전트 3종 (단방향 순차, 역참조 금지)

Planner → Generator → Evaluator 순으로 산출물이 전달된다.
각 에이전트는 이전 단계의 산출물만 받고, 다음 단계 결과를 미리 보지 않는다.

### Planner (기획 에이전트)
사용자 의도를 분석해서 하네스 구조를 설계한다.
- 인풋: 사용자 요구사항 (질문을 통해 수집)
- 아웃풋: 에이전트 구성안 + 폴더 구조 초안 + 평가 기준 제안
- 제약: Generator·Evaluator 결과를 보기 전에 설계한다

### Generator (구축 에이전트)
Planner 설계안을 실제 파일로 만든다.
- 인풋: Planner 승인된 설계안
- 아웃풋: 실제 .md/.json 파일들 (전체 산출물 목록은 Phase 2 참조)
- 제약: Evaluator 기준을 미리 보지 않고 구축한다

### Evaluator (평가 에이전트)
Generator 산출물을 독립적으로 검증한다.
- 인풋: Generator 생성 파일 + Planner 평가 기준
- 아웃풋: 5대 기둥 기반 점수 + 기능적 검증 결과 + 개선 피드백
- 제약: Generator 의도를 고려하지 않고 결과물만 본다

---

## L1 Phase 0: Pattern Match — harness-100 참조 (신규 v4.1)

> "좋은 설계의 99%는 이미 누군가 만들어 놓았다. 찾아서 변형하라."

Discovery에 들어가기 **전에** harness-100(https://github.com/revfactory/harness-100, Apache-2.0)의 검증된 exemplar 중 가장 유사한 것을 찾아 참조 기준으로 삼는다. 비개발자는 `harness-starter-workspace` 스킬로 전환 안내.

### 대상 exemplar (워크스페이스 도메인 73개)
- Content #01–15, Business #43–55, Education #56–65, Legal #66–72, Lifestyle #73–80, Docs #81–88, Operations #89–95, Specialized #96–100

### Phase 0 절차
1. 사용자 1~2문장 요청에서 도메인 키워드 추출
2. 위 73개 중 상위 3개 후보 제시 + 사용자 확인
3. 선택된 exemplar 번호를 `_workspace/00_input.md`의 `reference_exemplar` 필드에 기록
4. 매칭 유사도 < 0.5 → **자유 설계 모드 폴백** (기존 Phase 1로 진행)

### Phase 0 결과를 이후 단계에 반영
- **Planner**: exemplar의 4~5인 specialist + Reviewer 구성을 기본으로 사용
- **Generator**: exemplar 골격 스캐폴더, `_workspace/NN_*.md` 번호 컨벤션 강제
- **Evaluator**: exemplar의 8개 Quality Standards(Agent Team Mode / Domain Expertise / Structured Outputs / Dependency DAG / Error Handling / Scale Modes / Test Scenarios / Trigger Boundaries)를 루브릭으로 사용

### Pattern Fidelity (정성 평가, Phase 0 한정)

> 5대 기둥 자동 채점에는 포함하지 않는다. Phase 0에서 exemplar 매칭 시 정성적으로 평가한다.

Phase 0에서 선택한 harness-100 exemplar의 8개 Quality Standards
(Agent Team Mode / Domain Expertise / Structured Outputs / Dependency DAG /
Error Handling / Scale Modes / Test Scenarios / Trigger Boundaries)를
Evaluator 채점과 별개로 점검한다.

- 적용 시점: Phase 0(exemplar 선택)에서 1회, Evaluator PASS 후 보고 시 1회
- 점수화 안 함: 5대 기둥 22항목 채점에 포함되지 않음
- pillar-weight: 5대 기둥의 가중치 조정만 가능. Pattern Fidelity는 가중치 대상 아님

### Reviewer 필수화

운영층에는 **반드시** Reviewer 에이전트(cross-validation 역할)를 포함한다. 기존 Chairman 종합 모델에 Reviewer 교차검증 단계 추가.

### Trigger Boundaries (should + NOT)

Planner/Generator는 생성되는 orchestrator skill.md에 **반드시** `should-NOT trigger` 섹션을 포함한다.

### 도메인 프레임워크 주입

카테고리별로 검증된 프레임워크를 자동 주입:
- Content: AIDA, Pattern Interrupt, CURVE formula
- Business: BMC, TAM/SAM/SOM, Porter's 5 Forces, RICE, Van Westendorp PSM
- Education: Bloom's Taxonomy, ADDIE, CEFR, SM-2, Toulmin Model
- Legal: IRAC, MQM, GDPR/PIPA, IPC/CPC
- Lifestyle: BMR/TDEE, ACSM Guidelines, Compound Interest
- Docs: Diataxis, PREP, STAR, MADR, SemVer
- Operations: SIPOC/RACI, 4C Framework, SMART, NPS/CSAT, BARS
- Specialized: GHG Protocol, Cap Rate/IRR, IMRaD, Georgia-Pacific, Double Materiality

---

## L1 Phase 1: Discovery — Planner 작동

Discovery는 4단계 질문으로 구성된다.
각 단계를 순서대로 진행하되, 사용자 답변에 따라 후속 질문이 분기된다.
**한 단계의 답변을 받은 후 다음 단계로 넘어간다.** 한꺼번에 묻지 않는다.

### 1-0. 확인 모드 — idea-to-spec 기획서가 있을 때

프로젝트에 `spec-work/DEV_SPEC.md`(idea-to-spec 산출물, WORKSPACE 유형)가 있으면 Discovery를 **확인 모드**로 진행한다. 쉬운 설명: "이미 받은 기획서에 적힌 건 다시 묻지 않고, 맞는지만 확인합니다."

- 대응표 정본: idea-to-spec `references/05-final-spec.md`의 "넘겨주기 매핑표"(WORKSPACE 표). idea-to-spec이 설치돼 있지 않으면 DEV_SPEC 섹션 번호로 직접 대응한다.
- W1~W4·S1~S6·H·E 중 대응 항목은 DEV_SPEC 내용을 요약해 보여 주고 **"맞나요? 바꿀 것만 말씀해 주세요"**로 한 번에 확인한다. 비어 있거나 서로 모순된 항목만 원래 질문으로 묻는다.
- 만들 가치·필요성은 다시 묻지 않는다 (idea-to-spec이 GO 판정함).
- DEV_SPEC의 **정책은 그대로 반영하고 다시 설계하지 않는다**: 12(훅·서브에이전트)·14(개입 등급 R0/R1/R2)·19(차단기 값)·20(보안)·24(개입 수준)는 Build 산출물에, 16 Checker 3단은 Evaluate 단계의 검증 프로토콜에 옮긴다. 정책을 바꿔야 할 이유가 보이면 바꾸지 말고 사용자에게 묻는다.
- Phase 0(harness-100 exemplar 매칭)과 Build·Evaluate는 이 스킬의 원래 절차대로 수행한다.
- 사용자가 "기획서 무시하고 처음부터"라고 하면 일반 Discovery로 진행한다.
- 확인 모드에서는 위 "한 단계씩, 한꺼번에 묻지 않는다" 규칙 대신 **대응 항목을 한 번에 확인**한다 (이미 답이 있으므로). 빈 항목 질문은 다시 한 단계씩.
- DEV_SPEC 16의 Tier 2(빌드 산출물을 다른 모델이 검토)는 이 스킬 Evaluate 단계의 검증 방식이다. 운영층 Council의 **Reviewer 에이전트**(업무 결과 교차검증)와는 다른 역할이니 섞지 않는다.

### 1-1. Stage 1 — 목적과 맥락 (WHY / WHO)

> 구조가 아닌, 이 워크스페이스가 존재하는 이유를 파악한다.

```
W1. 이 워크스페이스가 해결하려는 문제는 무엇인가?
    (어떤 의사결정/분석/판단이 지금 잘 안 되고 있는가?)

W2. 누가 사용하는가?
    (에이전트만 / 에이전트+사람 / 사람이 결과를 소비)
    → 후속: 사용자의 도메인 전문성 수준은?

W3. 이 워크스페이스의 성공 기준은?
    (어떤 결과가 나오면 "잘 만들었다"고 할 수 있는가?)

W4. 비슷한 기존 프로세스가 있는가?
    (대체하는 것인가 / 새로 만드는 것인가)
    → 후속 [대체]: 기존 프로세스의 가장 큰 문제점은?
    → 후속 [신규]: 벤치마크하는 시스템이 있는가?
```

**후속 질문 분기:**
- W2에서 "사람이 결과 소비" → "결과를 받는 사람의 직급/역할은? 어떤 형식을 선호?"
- W3에서 모호한 답변 → "구체적으로 어떤 산출물이 나오면 성공인가?"

### 1-2. Stage 2 — 산출물과 구조 (WHAT)

> 무엇을 만드는가, 어떤 관점이 필요한가.

```
S1. 최종 산출물은?
    (보고서 / 의사결정 기록 / 분석 리포트 / 기획안)

S2. 반복되는 핵심 작업 패턴은?
    (인풋 → 분석 → 의사결정 → 기록 → 지식 축적)

S3. 필요한 관점·역할은 몇 가지? 각각 어떤 성격?
    (예: 낙관/비관/데이터/경험/규제 — 서로 충돌·보완)
    → 후속: 관점 간 우선순위가 있는가? 동등한가?

S4. Chairman(종합 역할)이 필요한가?
    (메인 세션 담당 / 별도 에이전트 / 불필요)
    → 후속 [필요]: 에이전트 모델 구성은?
      → references/agent-archetypes.md 참조 후 제안

S5. 인풋 형태는?
    (텍스트 직접 입력 / 파일 업로드 / URL / 복합)

S6. 남아야 할 아웃풋은?
    (세션 파일 / 의사결정 기록 / 지식 축적 / deep-research)
```

**후속 질문 분기:**
- S3에서 5개 이상 관점 → "이 관점들을 그룹으로 묶을 수 있는가? 순차 vs 병렬?"
- S4에서 "별도 에이전트" → "Chairman의 판단 프레임워크는? Go/Pivot/No-Go?"

### 1-2.5. Stage 2.5 — 지식 관리 (KNOWLEDGE) [조건부]

> 멀티 어젠다 연구 워크스페이스에서 기존 연구를 체계적으로 참조하기 위한 wiki 옵션.
> 단일 어젠다 또는 비연구 워크스페이스에서는 스킵.

```
K1. "여러 어젠다(연구 주제)를 진행하며 기존 연구를 후속 연구에서 참조할 필요가 있습니까?"
    → "아니오" → wiki 불포함. Stage 3으로.
    → "예" → K2로.

K2. /graphify 스킬 설치 확인 (자동 감지)
    - ~/.claude/skills/graphify/ 또는 .claude/skills/graphify/ 존재 확인
    - 설치됨 → K3로.
    - 미설치 → 설명 제공:
      ┌─────────────────────────────────────────────────┐
      │ wiki는 /graphify 스킬로 생성됩니다.               │
      │ 이 스킬이 없으면 wiki를 생성할 수 없습니다.         │
      │                                                 │
      │ /graphify란?                                    │
      │ - 문서·보고서를 분석하여 지식 그래프 생성           │
      │ - 개념 간 연결을 자동 발견하고 시각화              │
      │ - 커뮤니티 기반 wiki 문서 자동 생성                │
      └─────────────────────────────────────────────────┘
      "graphify를 설치하시겠습니까?"
      - 전역 설치 (~/.claude/skills/) [모든 프로젝트에서 사용]
      - 프로젝트 설치 (.claude/skills/) [이 프로젝트에서만]
      - 설치하지 않음 → ⚠️ "wiki 기능은 비활성됩니다.
          45-wiki/ 폴더는 생성되지만 빈 상태입니다.
          나중에 /graphify 설치 후 /wiki-update로 생성 가능합니다."
        → wiki 구조만 포함, 비활성. Stage 3으로.

K3. "wiki 저장소를 어디에 둘까요?"
    - 프로젝트 내부 (45-wiki/) [기본]
    - 외부 경로 지정

K4. "새 리서치 시작 시 wiki를 자동 탐색할까요?"
    - 자동 탐색 + 사용자 승인 후 참조 [기본]
    - 수동 호출(/wiki-ref)만 허용
```

**Planner 출력에 추가 (wiki 관련):**
- `wiki_enabled: true/false`
- `wiki_location: "45-wiki/" 또는 사용자 지정 경로`
- `wiki_auto_ref: true/false`
- `graphify_installed: true/false`
- `graphify_scope: "global" | "project" | "none"`

**⚠️ wiki 참조의 독립성 보호:**
- Phase A(독립 리서치) 에이전트에 wiki 내용 주입 절대 금지
- Phase B(Creative Thinker) / Phase C(Chairman)에서만 사용자 승인 후 참조 허용
- 참조 시 결론이 아닌 프레임워크/방법론/데이터 포인트만 전달
- 산출물에 wiki_ref, ref_approved_by, ref_approval_date 기록 필수

### 1-2.6. Stage 2.6 — 플로우 변경 이력 추적 (FLOW HISTORY) [선택]

> 워크플로우가 시간에 따라 개선될 것으로 예상되는 프로젝트에 권장.
> 1회성 분석·단발 프로젝트에서는 스킵해도 무방.

```
F1. "향후 워크플로우가 개선되거나 변경될 때 이력을 남길까요?"

    용도:
    - 프로젝트 개선 이력 회고 (왜 이렇게 바뀌었는가)
    - 이전 버전으로 롤백이 필요할 때 근거 확보
    - 차기 유사 프로젝트 설계 시 참고

    ※ 새 세션마다 읽는 용도가 아닙니다.
      플로우를 수정·롤백·이식할 때만 참조합니다.

    → "아니오" → 05-flow-history/ 불포함. Stage 3으로.
    → "예" → F2로.

F2. "초기 빌드(v1)를 change 0001 레코드로 자동 기록할까요?"
    - 기본값: 예 (Planner Discovery 답변이 그대로 설계 근거로 보존됨)
    - 아니오 → CHANGELOG만 생성하고 첫 변경 시 수동 기록
```

**플로우 이력 관리 원칙 (생성 후 운영 기준):**
이 이력은 **워크플로우 시스템**(규칙·절차·도구·프롬프트·커맨드·스크립트·CLAUDE.md)의
변화만 기록한다. 시스템이 만들어낸 **산출물**(리서치 결과·보고서·분석·어젠다 등록)은
기록 대상이 아니다.
구별 기준: "이 변경이 없었더라면 다음에 실행하는 결과가 달라지는가?"
→ 달라진다 = 시스템 변경 = 기록 / 달라지지 않는다 = 산출물 = 기록 불필요
상세: `00-system/protocols/flow-change-protocol.md`

**Planner 출력에 추가 (flow-history 관련):**
- `flow_history_enabled: true/false`
- `flow_history_initial_record: true/false` (F2 답변)

### 1-3. Stage 3 — 환경과 도구 (HOW)

> 어떤 환경에서 어떻게 운영할 것인가.

```
H1. 사용하는 AI 도구는?
    (Claude Code / Desktop Claude / 기타)
    → 도구에 따라 하네스 설정 방식이 다름

H2. 세션 간 연속성이 필요한가?
    (단발 분석 / 장기 프로젝트 / 멀티 세션)
    → "장기"라면 세션 핸드오프 산출물 포함

H3. 에이전트 모델 구성은?
    → 웹 검색으로 현재 최신 Claude 모델을 확인 후 제안
    → 모델명을 하드코딩하지 않는다. 항상 사용자가 결정

H4. 에이전트의 자율성 수준은?
    (사람이 매번 확인 / 에이전트 자율 판단 + 보고 / 완전 자율)
```

**후속 질문 분기:**
- H2에서 "장기" → "예상 세션 수는? 지식 축적이 중요한가?"
- H4에서 "완전 자율" → "에스컬레이션 기준은? 어떤 상황에서 사람에게 물어야 하는가?"

### 1-4. Stage 4 — 품질과 평가 기준 (QUALITY / EVALUATE)

> 사용자가 중요하게 생각하는 가치를 파악하고, 평가 기준을 합의한다.

```
E1. 이 워크스페이스에서 가장 중요한 품질 속성은? (상위 3개 선택)
    □ 분석 깊이 (표면적이지 않은 통찰)
    □ 독립성 (에이전트 간 영향 없는 독립 분석)
    □ 출처 명시 (근거 기반 결론)
    □ 일관성 (세션 간 품질 유지)
    □ 빠른 반응 (짧은 처리 시간)
    □ 확장성 (에이전트/역할 추가 용이)
    □ 문서화 (과정과 결과의 추적 가능성)
    □ 사용자 접근성 (비전문가도 결과 이해)

E2. 향후 확장 계획이 있는가?
    (없음 / 관점 추가 / 다른 도메인 적용 / 자동화 강화)

E3. 이 워크스페이스에서 절대 타협하면 안 되는 것은?
    (예: "에이전트가 서로 영향을 주면 안 된다", "출처 없는 결론은 안 된다")

E4. 반대로, 초기에는 없어도 괜찮은 것은?
```

**후속 질문 분기:**
- E1에서 "독립성" → "어떤 수준? 결과 공유도 금지? 아니면 분석만 독립?"
- E3의 답변 → Evaluator 가중치의 핵심 입력으로 사용

### 1-5. 평가 가중치 합의 (Stage 4 완료 후)

Stage 1~4의 답변을 분석하여 **5대 기둥의 가중치를 제안**한다.
사용자와 합의하여 최종 확정한다.

```
[가중치 제안 프로세스]

STEP 1. Stage 1~4 답변에서 키워드 추출
  - "독립성 필수" → Mechanical Enforcement ↑
  - "장기 프로젝트" → Session Continuity ↑, Entropy Management ↑
  - "빠른 반응" → Progressive Disclosure ↑
  - "출처 명시" → Mechanical Enforcement ↑

STEP 2. 기본 가중치에서 조정하여 제안

  기본 가중치 (프로젝트 특성 반영 전):
  | 기둥 | 기본 | 조정 근거 | 제안 |
  |------|------|----------|------|
  | Progressive Disclosure | 20% | (변동 근거) | ?% |
  | Mechanical Enforcement | 25% | (변동 근거) | ?% |
  | Feedback Loop | 20% | (변동 근거) | ?% |
  | Session Continuity | 15% | (변동 근거) | ?% |
  | Entropy Management | 20% | (변동 근거) | ?% |

  "이 프로젝트에서는 [근거]를 고려하여
   [기둥]의 가중치를 [기본]% → [제안]%로 조정했습니다.
   의견이나 수정 사항이 있으시면 말씀해주세요."

STEP 3. 사용자 피드백 반영
  - 동의 → 확정
  - "독립성을 더 높여줘" → Mechanical Enforcement 상향, 다른 기둥 하향 후 재제안

STEP 4. 최종 승인
  → evaluator-protocol-workspace.md의 기본 가중치 대신 합의된 가중치를 사용
```

### 1-6. 패턴 자동 매핑

Stage 2 답변으로 폴더 패턴을 자동 추천한다:

| 사용자 답변 키워드 | 추천 패턴 | 참조 |
|------------------|----------|------|
| 분석, 투자, 의사결정, 판단 | 패턴 A (분석·의사결정형) | folder-patterns.md |
| 시공, 공정, 내역서, 건설 | 패턴 B (건설·프로젝트관리형) | folder-patterns.md |
| 리서치, 콘텐츠, 보고서 | 패턴 C (리서치·콘텐츠형) | folder-patterns.md |
| 장기 코딩, 자동화 빌드 | 패턴 D (장기 에이전트형) | folder-patterns.md |

### 1-7. Planner 산출물

**① 프로젝트 컨텍스트 요약** — 목적, 사용자, 성공 기준, 핵심 제약 (Stage 1~2 기반)
**② 에이전트 구성안** — 역할, 성격, 모델 배치
**③ 폴더 구조 초안** — 패턴 매핑 + 커스터마이징
**④ 세션 연속성 설계** — 핸드오프 방식 결정 (단발 / progress.json 사용)
**⑤ 확장 전략** — 향후 확장에 대비한 설계 결정 (Stage 4 E2 기반)
**⑥ 평가 기준 + 합의된 가중치** — 5대 기둥 체크리스트 + 가중치 테이블

```
[Planner 완료 — 사용자 승인 요청]
①~⑥을 검토 후 수정 사항 말씀해주세요.
승인되면 Generator가 구축을 시작합니다.
```

---

## L1 Phase 2: Build — Generator 작동

Planner 산출물 승인 후 아래 순서로 파일 생성.
Generator는 **폴더 구조 + 파일 내용물 모두** 생성한다.

### 2-1. 워크플로우 다이어그램 (Mermaid)

두 레이어를 모두 표현하는 다이어그램. Evaluator→Planner 재설계 루프 포함:

```mermaid
flowchart TD
    USER[사용자] -->|요구사항| P
    subgraph L1[Layer 1: 메타]
        P[Planner] --> G[Generator]
        G --> E[Evaluator]
        E -->|미흡 70~89%| G
        E -->|재설계 70%미만| P
        E -->|승인 90%+| DONE[구조 완성]
    end
    DONE --> INIT
    subgraph L2[Layer 2: 운영]
        INIT[Initializer\n첫 실행 전용] --> OP
        subgraph OP[Operating Agent 반복 실행]
            INPUT[인풋] --> SPLIT[ ]
            SPLIT --> A1[Agent-A]
            SPLIT --> A2[Agent-B]
            SPLIT --> A3[Agent-C]
            A1 --> CH[Chairman 종합]
            A2 --> CH
            A3 --> CH
            CH --> OUT[아웃풋 + 상태 저장]
        end
    end
```

### 2-2. 핵심 산출물 생성 (순서대로)

| 순번 | 산출물 | 참조 파일 | 비고 |
|------|--------|----------|------|
| 2-2a | WORKSPACE_TREE.md | folder-patterns.md | 폴더 구조 확정 |
| 2-2b | CLAUDE.md (~100줄) | claude-md-template.md | **목차 역할**, 참조 라우팅 테이블 필수 |
| 2-2c | AGENTS.md | (본 스킬 내 가이드) | 에이전트 운영 규칙 + model_config |
| 2-2d | 에이전트 역할 파일 | agent-archetypes.md | 00-system/prompts/*.md |
| 2-2e | 프로토콜 5종 | (본 스킬 내 가이드) | 00-system/protocols/ |
| 2-2f | 세션 핸드오프 산출물 | session-handoff.md | progress.json + feature-status.json |
| 2-2g | 강제 규칙 | enforcement-patterns.md | 구조 검증 가능한 규칙 |
| 2-2h | 슬래시 커맨드 | (Planner 설계 기반) | .claude/commands/*.md |
| 2-2i | README.md | (사용자 가이드) | 빠른 시작 + 커맨드 + 트러블슈팅 |
| 2-2j | 플로우 변경 이력 위키 (선택) | flow-history-template.md | Stage 2.6에서 F1=예일 때만 |

### 2-2b. CLAUDE.md 작성 규칙 (최중요)

→ `references/claude-md-template.md` 참조. **반드시 100줄 이내.**

CLAUDE.md는 에이전트의 **진입점(entry point)**이다.
너무 긴 instruction은 "비안내(non-guidance)"가 된다:
- 컨텍스트가 작업과 코드를 밀어낸다
- 에이전트가 의도적 탐색 대신 로컬 패턴 매칭에 빠진다
- 모놀리식 문서는 즉시 낡는다

**반드시 포함하는 것:**
- 워크스페이스 정체성 (3줄)
- 에이전트 구성 테이블
- **참조 라우팅 테이블** ← Progressive Disclosure 핵심
- 독립성 원칙 포인터
- 커맨드 목록

**참조 라우팅 테이블 형식:**
```markdown
## 참조 라우팅
| 상황 | 읽을 파일 |
|------|----------|
| 에이전트 역할 확인 | → 00-system/prompts/[role].md |
| 토론 진행 규칙 | → 00-system/protocols/council-protocol.md |
| 독립성 원칙 상세 | → 00-system/protocols/independence-protocol.md |
| 세션 상태 확인 | → progress.json |
| 기능 완료 현황 | → feature-status.json |
```

### 2-2c. AGENTS.md 작성 규칙

**반드시 포함:**
- Layer 2 에이전트 목록 테이블 (역할 / 모델 / 활성화 조건)
- model_config 섹션 (사용자 선택 모델 + 재검토 트리거)
- Chairman 종합 방식 + 결정 프레임워크 (Go/Pivot/No-Go)
- 독립성 원칙 요약
- 컨텍스트 관리 규칙

### 2-2d. 에이전트 역할 파일

각 `00-system/prompts/[role].md`:
→ `references/agent-archetypes.md` 참조
- 정체성, 독립성 선언(포인터), 관점, 분석 프로세스, 절대 금지

> **아웃풋 형식 정본 규칙 (Source of Truth)**:
> - `00-system/templates/*.md`가 아웃풋 구조의 **정본(source of truth)**이다.
> - 에이전트 프롬프트(`prompts/*.md`)에는 아웃풋 형식을 **인라인하지 않는다**.
>   대신 `아웃풋 형식: → 00-system/templates/[해당-template].md 참조` 포인터를 둔다.
> - 에이전트별로 템플릿 필드가 다른 경우, 범용 템플릿 대신 에이전트별 템플릿을 분리한다.
>   (예: research-template.md를 academic/trend/product별로 분리)
> - **이유**: 프롬프트와 템플릿 양쪽에 동일 구조를 두면 수정 시 drift가 발생한다.

### 2-2e. 프로토콜 5종

```
00-system/protocols/
├── council-protocol.md        ← 에이전트 소집·진행·종합 규칙
├── independence-protocol.md   ← 독립성 보장 규칙 (필수)
├── analysis-protocol.md       ← 분석 표준 절차
├── data-pipeline-architecture.md ← 데이터 흐름 설계
└── maintenance-protocol.md    ← 엔트로피 관리 (v4 신규)
```

**maintenance-protocol.md 필수 내용:**
- 문서 신선도 검증 주기 (N회 세션마다 / 새 에이전트 추가 시)
- CLAUDE.md ↔ WORKSPACE_TREE.md 동기화 체크
- 오래된 세션 파일의 아카이브 기준 (90-archive/ 이동 조건)
- 하네스 경량화 검토 (아래 참조)

### 2-2f. 세션 핸드오프 산출물

→ `references/session-handoff.md` 참조

장기 프로젝트 시 Generator가 생성해야 하는 운영 상태 파일:

**progress.json** — 현재 작업 상태
```json
{
  "last_session": "2026-03-29T10:00:00",
  "last_completed": "지역 분석 — 수원 영통구",
  "next_todo": "비교 분석 — 동탄 vs 광교",
  "open_issues": [],
  "session_count": 5
}
```

**feature-status.json** — 기능 완료 현황 (JSON, Markdown 아님)
```json
[
  {"id": "F001", "description": "Council 5인 독립 토론", "passes": true},
  {"id": "F002", "description": "비교 분석 자동 저장", "passes": false},
  {"id": "F003", "description": "인사이트 CARL 형식 축적", "passes": false}
]
```

JSON을 사용하는 이유: 에이전트가 Markdown보다 JSON을 부적절하게 편집할 가능성이 낮다 (Anthropic 원안).

### 2-2g. 강제 규칙 (Mechanical Enforcement)

→ `references/enforcement-patterns.md` 참조

문서화만으로는 일관성 유지 불가. Generator는 규칙을 **검증 가능한 형태**로 만든다:

| 규칙 유형 | 문서만 | 강제 가능 (v4) |
|----------|--------|---------------|
| 독립성 원칙 | "동조 금지" 선언 | 세션 기록에 `bias_check` 필드 포함 |
| 출처 필수 | "출처 없는 주장 금지" | 아웃풋 템플릿에 `source` 필드 필수 |
| 파일 구조 | WORKSPACE_TREE.md | 구조 검증 스크립트 (선택) |
| 세션 상태 | 없음 | progress.json 업데이트 의무 |

### 2-2h~i. 슬래시 커맨드 + README.md

**커맨드:** Planner 설계에서 도출된 주요 워크플로우를 .claude/commands/*.md로 생성
**README.md:** 사용자 가이드 — 빠른 시작, 핵심 기능, 커맨드 레퍼런스, 트러블슈팅

### 2-2j. 플로우 변경 이력 위키 (Stage 2.6 F1=예일 때만)

> **관리 원칙**: 시스템(규칙·절차·도구·CLAUDE.md) 변화만 기록. 산출물(리서치 결과·보고서·분석)은 기록 불필요.
> 구별 기준: "이 변경이 없었더라면 다음 실행 결과가 달라지는가?" → 달라지면 기록, 아니면 불필요.
> 상세: `00-system/protocols/flow-change-protocol.md`

→ `references/flow-history-template.md` 를 읽고 그대로 실행한다.

생성할 파일 5+1종:
1. `05-flow-history/README.md` — 위키 진입점 ([프로젝트명] 치환)
2. `05-flow-history/CHANGELOG.md` — 시간순 타임라인
3. `05-flow-history/changes/TEMPLATE.md` — 변경 레코드 템플릿
4. `05-flow-history/changes/0001-[YYYY-MM-DD]-initial-harness.md` — 초기 빌드 기록 (F2=예일 때)
5. `05-flow-history/snapshots/v1.md` — v1 스냅샷
6. `00-system/protocols/flow-change-protocol.md` — 변경 추적 프로토콜

CLAUDE.md 업데이트 (2-2b에서 함께 반영):
- 참조 라우팅 테이블에 2행 추가 (flow-change-protocol, flow-history README)
- "플로우 변경 추적 (선별 기록)" 섹션 추가 (기록 대상/불필요 명시)

```
[GATE: Generator → Evaluator 강제 전환]
이 절차는 건너뛸 수 없다. Generator 완료 즉시 실행한다.

STEP 1. 산출물 존재 확인
  아래 각각에 대해 Glob으로 존재 + Read로 비어있지 않음을 확인한다:
  □ CLAUDE.md (~100줄)
  □ AGENTS.md
  □ WORKSPACE_TREE.md
  □ 00-system/prompts/ 내 에이전트 역할 파일 1개 이상
  □ 00-system/protocols/council-protocol.md
  □ 00-system/protocols/independence-protocol.md
  □ 00-system/protocols/maintenance-protocol.md
  □ .claude/commands/ 내 커맨드 파일 1개 이상
  □ README.md
  □ (장기 프로젝트) progress.json + feature-status.json
  □ (Stage 2.6 F1=예) 05-flow-history/README.md, CHANGELOG.md, changes/TEMPLATE.md, snapshots/v1.md
  □ (Stage 2.6 F1=예) 00-system/protocols/flow-change-protocol.md
  □ (Stage 2.6 F1=예, F2=예) 05-flow-history/changes/0001-*-initial-harness.md

  → 미존재 파일이 있으면: Generator로 돌아가서 해당 파일만 생성
  → 모두 존재하면: STEP 2로 진행

STEP 2. Evaluator 프로토콜 실행
  → references/evaluator-protocol-workspace.md 를 읽고 그 절차를 그대로 실행한다
  → 5대 기둥 채점 (총 22항목, 기둥 2는 10항목·나머지 3항목씩)
  → 가중치 적용 → 총점 산출
  → 결과를 보고 형식으로 사용자에게 출력

STEP 3. 점수별 분기
  → 90점 이상: STEP 4 (Cartesian Review) 실행
  → 70~89점: Generator 재작업
  → 70점 미만: Planner 재설계 (Phase 1로 복귀)

STEP 4. Cartesian Review (90점 이상일 때만)
  → cartesian-review 스킬 설치 여부 확인
     설치됨  → Phase 3-5 절차 실행 (데카르트 5렌즈 검토)
     미설치  → "cartesian-review 스킬 미감지, 건너뜁니다" 안내 후 Layer 2 승인 진행

이 GATE를 통과하지 않으면 Layer 2로 진행할 수 없다.
```

---

## L1 Phase 3: Evaluate — Evaluator 작동

> 이 단계는 GATE에 의해 자동으로 진입한다. 생략할 수 없다.

### 3-1. 검증 실행

→ `references/evaluator-protocol-workspace.md` 를 읽고 그대로 실행한다.

요약: 5대 기둥 총 22항목 (기둥 2는 10항목, 나머지 3항목씩)을 PASS/PARTIAL/FAIL로 채점.
가중치 적용 후 100점 만점으로 총점 산출. 결과를 보고 형식으로 출력.

### 3-2. 피드백 루프 (점수별 분기)

| 총점 | 판정 | 구체적 행동 |
|------|------|------------|
| 90점+ | **PASS** | Layer 2 구조 토론 → 사용자 최종 승인 → 구조 확정 |
| 70~89점 | **REWORK** | FAIL/PARTIAL 항목별 피드백 → Generator 재작업 → Evaluator 재실행 |
| 70점 미만 | **REDESIGN** | 근본 원인 분석 → Planner 재설계 |

### 3-3. 재검증 규칙

1. Generator 재작업 후 **Evaluator 전체 재실행** (부분 검증 금지)
2. 최대 **3회 반복**. 초과 시 사용자에게 에스컬레이션
3. 매 반복마다 점수 변화 테이블 보고
4. 3회 연속 점수 개선 없으면 → 즉시 사용자 에스컬레이션 (무한 루프 방지)

### 3-4. REWORK 피드백 형식

각 FAIL/PARTIAL 항목에 대해:

```
❌ [기둥명] 항목 [번호]: [FAIL/PARTIAL]
   문제: [무엇이 부족한지 1줄]
   수정: [구체적으로 어떤 파일에 무엇을 추가/변경할지]
```

이 피드백은 Generator가 그대로 따라 실행할 수 있는 수준이어야 한다.

### 3-5. Cartesian Review 자동 실행 (PASS 판정 후)

> 이 단계는 cartesian-review 스킬이 설치된 경우에만 활성화된다.
> 미설치 시 이 단계를 건너뛰고 3-6으로 진행한다.

**설치 확인**
```
~/.claude/skills/cartesian-review/ 또는 .claude/skills/cartesian-review/ 존재 여부 확인
```

**설치된 경우 — 자동 실행**

5대 기둥 채점이 PASS(90점+)여도 놓칠 수 있는 실용적 결함을 데카르트 5렌즈로 추가 검토한다.

```
[cartesian-review 호출 파라미터]
검토 대상:    Generator 산출물 전체 (CLAUDE.md + AGENTS.md + 프로토콜)
L5 관점:      자동 고정 →
              "이 하네스를 처음 받아서 CLAUDE.md만 읽고 바로 작업해야 하는 에이전트.
               무엇이 막히는가? 무엇이 모호한가? 무엇을 잘못 이해할 수 있는가?"
L5 의심 범위: A (과정 한정) — 자동 고정. STEP 0.5 사용자 질문은 생략한다.
              (이유: 검증 대상은 Generator 산출물이지 사용자 어젠다가 아니다)
```

**cartesian-review 결과 처리**

| 결과 | 처리 |
|---|---|
| L1 높음 항목 발견 | Generator 재작업 대상에 추가 → 3-2로 복귀 |
| L4 높음 항목 발견 | Generator 불필요 요소 제거 → 3-2로 복귀 |
| L2·L3만 발견 | 사용자에게 보고 후 승인 받고 진행 |
| "사용자 확인 필요 가정" 발견 | 사용자에게 보고 후 답변 받고 진행 (Generator 재작업 아님) |
| 발견 없음 | 즉시 3-6으로 진행 |

**미설치 안내 (건너뛸 경우)**
```
⚠️ cartesian-review 스킬이 감지되지 않았습니다.
   데카르트 5렌즈 추가 검증을 건너뜁니다.
   설치 후 재실행하면 더 정밀한 품질 검증이 가능합니다.
   설치: ~/.claude/skills/ 또는 .claude/skills/ 에 cartesian-review 폴더 배치
```

### 3-6. Layer 2 구조 최종 토론 (PASS 판정 후)

Evaluator 통과 후, 완성된 구조를 Layer 2 에이전트들이 검토·토론.
각 에이전트가 자신의 관점에서 구조를 평가한 뒤, Chairman이 종합.

### 3-7. 하네스 경량화 검토 (PASS 판정 후)

```
[경량화 체크리스트]
- [ ] 이 프로토콜 중 현재 모델이 자체 처리할 수 있는 것은?
- [ ] 프로토콜 5종 중 이 도메인에 불필요한 것은?
- [ ] 에이전트 수가 과잉이지 않은가? (8개 초과 비권장)
- [ ] 세션 핸드오프가 불필요한 단발 프로젝트인데 추가되지 않았는가?
```

> 원칙: 모델이 좋아질수록 하네스는 단순해져야 한다. (Anthropic)

---

### 3-8. 환경 설정 제안 (PASS 판정 후 실행, 선택 사항)

> "강제하지 않는다. 판단하고 제안한다. 선택은 사용자가 한다."

워크스페이스 하네스도 데이터 가공·LLM API·리서치 데이터 API 연동이 흔하다.
Discovery 답변에서 수집한 인풋 형태·산출물 유형·도메인을 기반으로
`references/hook-catalog-workspace.md`를 읽어 아래 3가지 영역을 분석하고 제안한다.

**이 단계는 자동 생성하지 않는다.**
제안만 하고, 사용자가 선택한 항목만 이후 프롬프트로 생성한다.

#### 실행 절차

**STEP 1. 워크스페이스 컨텍스트 요약**

Discovery 답변에서 아래를 추출한다:
```
- 워크스페이스 도메인: (예: 투자 분석 / 콘텐츠 기획 / 법률 검토)
- 인풋 형태: (예: 텍스트 / 파일 업로드 / URL / 외부 API)
- 데이터 가공 필요성: (예: PDF 파싱, 웹 스크래핑, 데이터 정제 — Stage 2 S5)
- 외부 서비스 연동: (예: LLM API, 검색 API, 시장 데이터 API)
- 산출물 검증 강제 수단 필요성: (예: CARL 형식, source 필드 필수)
```

**STEP 2. hook-catalog-workspace.md 조회**

→ `references/hook-catalog-workspace.md`를 읽고 도메인 특성에 해당하는 항목을 필터링한다.
→ 필요 없다고 판단되는 항목은 제안 목록에서 제외한다 (이유 포함).

**STEP 3. 제안 출력**

아래 형식으로 사용자에게 출력한다:

```
## 🛠 환경 설정 제안 (워크스페이스)

워크스페이스: [프로젝트명] | 도메인: [도메인 분류] | 외부 연동: [LLM API / 데이터 API / 없음]

---

### A. 가상환경 (데이터 가공 스크립트가 있을 때만)

| # | 도구 | 생성 파일 | 이유 |
|---|------|---------|------|
| A1 | [예: python venv] | `.python-version`, `requirements.txt` | [PDF 파싱·웹 스크래핑 등 스크립트 실행 시 필요] |

---

### B. 환경변수 (외부 API 키)

| # | 항목 | 생성 파일 | 포함 키 예시 |
|---|------|---------|------------|
| B1 | API 키 스키마 | `.env.example`, `.gitignore` 추가 | ANTHROPIC_API_KEY, OPENAI_API_KEY, [도메인별 API] |

---

### C. 훅 (Claude Code Hook 중심)

| # | 종류 | 실행 시점 | 내용 | 생성 파일 |
|---|------|---------|------|---------|
| C1 | Claude Code Hook | PostToolUse | 산출물 검증 (CARL 형식 / source 필드 / 세션 파일 저장 확인) | `.claude/settings.json` |
| C2 | Claude Code Hook | Stop | 세션 종료 시 progress.json 업데이트 누락 경고 | `.claude/settings.json` |

---

원하는 항목 번호를 알려주세요. (예: "B1, C1 만들어줘")
전부 건너뛰려면 "건너뛰기"라고 하시면 Layer 2로 바로 이동합니다.
```

**STEP 4. 사용자 선택 처리**

| 사용자 응답 | 처리 방법 |
|-----------|---------|
| 항목 번호 지정 ("B1, C1") | 해당 파일만 즉시 생성 후 Layer 2 전환 |
| "전부" / "다" | 전체 항목 생성 후 Layer 2 전환 |
| "건너뛰기" / "스킵" | 생성 없이 Layer 2 바로 전환 |
| 번호 없이 질문 | 해당 항목 추가 설명 후 재선택 대기 |

**워크스페이스 vs 코딩 차이점 (반드시 인지):**
- Git Hook·pre-commit 프레임워크는 제안하지 않는다 (코드 커밋 워크플로우가 아님)
- 가상환경은 데이터 가공 스크립트가 명시적으로 있을 때만 제안한다
- 훅의 주 용도는 산출물 형식 강제 (CARL, source) — 코드 린팅이 아니다

**생성 시 원칙:**
- `.env.example`은 키 이름과 설명만 포함, 실제 값은 절대 기입하지 않는다
- `.env`는 생성하지 않는다 (사람이 직접 생성)
- 훅 명령은 워크스페이스 산출물(50-reports/, 70-playbook/)을 검증하는 형태로 작성한다
- 생성된 파일 목록을 CLAUDE.md 참조 라우팅 테이블에 추가한다

---

사용자 최종 승인 후 구조 확정:
```
[Layer 1 완료 — 구조 확정]
이 시점부터 워크스페이스는 Layer 2로 전환됩니다.
이후 모든 작업은 완성된 하네스 안에서 도메인 에이전트들이 수행합니다.
```

---

# LAYER 2: 운영 — 완성된 워크스페이스

Layer 1이 완료된 이후의 동작 방식.
이 스킬은 Layer 2를 직접 실행하지 않는다.
Layer 2는 생성된 CLAUDE.md + AGENTS.md가 정의한다.

## 에이전트 행동 강제 규칙 (Layer 2 전체 적용)

> 이 규칙은 Layer 2의 모든 단계에 적용된다. 예외 없음.

1. **검증 생략은 에이전트가 결정할 수 없다.**
2. 스킬에 정의된 단계를 건너뛰고 싶으면, **반드시 한국어로 사용자에게**:
   - 스킬에서 요구하는 단계가 무엇인지 설명
   - 왜 건너뛰어도 되는지 이유를 제시
   - 사용자의 **명시적 승인**을 받은 후에만 건너뛰기
3. 사용자가 "빨리 해", "진행해", "계속해" 등 속도를 요구해도,
   **이것은 검증 생략 승인이 아니다.**
   검증 생략은 "검증 건너뛰어", "평가 안 해도 돼" 등
   **명시적으로 검증을 언급**해야만 승인으로 간주한다.
4. 이 규칙을 위반하면 즉시 사용자에게 보고하고 되돌린다.
5. **"간단한 작업이라 검증이 필요 없다"는 에이전트의 자율 판단은 금지**한다.

## Initializer / Operating Agent 분리 (v4 핵심)

→ `references/session-handoff.md` 참조

**Initializer (첫 실행 전용):**
- 개발 서버 시작 스크립트 설정 (해당 시)
- progress.json 초기화
- feature-status.json 생성 (기능 목록 전개)
- 초기 git commit
- 기본 동작 테스트

**Operating Agent (매 세션 반복):**
```
1. progress.json 읽기 → 현재 상태 파악
2. feature-status.json 확인 → 다음 작업 선택
3. 작업 하나 수행 (점진적 진행)
```

```
[GATE: 검증 — 이 단계는 건너뛸 수 없다]
Layer 1의 Generator→Evaluator GATE와 동일한 강제력을 가진다.
사용자가 명시적으로 "검증 건너뛰어"라고 한 경우에만 생략 가능.

4. 결과 검증 — 수행 주체는 **Reviewer 에이전트** (Chairman 자가채점 금지.
   종합한 자가 승인하면 판정이 후해진다. 검증자는 생성/종합과 분리한다):

   각 항목을 통과/실패로 판정한다 (정성 서술로 대체 금지):
   a. [ ] 독립성 증거: 각 에이전트 산출물에 타 에이전트 결과 참조 0건
   b. [ ] Chairman 판정 존재: Go/Pivot/No-Go가 근거 문장과 연결됨
          (수집 결과를 합산만 하고 판정 없이 끝나면 실패)
   c. [ ] CARL 교훈 1건 이상 기록됨 (70-playbook/ — 매 바퀴 남는 것이 있어야 루프다)
   d. [ ] 산출물이 설계 문서(docs/)와 일치 + 세션 파일·progress.json 저장 완료
   e. 항목별 통과/실패를 사용자에게 한국어로 보고
   → 절차 상세: references/session-handoff.md "Reviewer 게이트"

   실패 항목이 있으면 해당 항목만 보완 후 재판정한다.
   이 GATE를 통과하지 않으면 상태 저장/커밋할 수 없다.

4-1. 실패 출구 (수렴 실패 시 사람에게):
   Chairman이 "추가 분석" 판정을 2회 연속 내리면 자동 반복을 중단하고,
   미해결 쟁점·에이전트 간 불일치 요약 리포트와 함께 사람에게 에스컬레이션한다.
   (판정 이력은 progress.json verdicts로 추적 — session-handoff.md 참조)
   판정이 애매한 세션은 cartesian-review 스킬(설치 시)의 5렌즈로 보조 채점할 수 있다.

5. clean state로 저장:
   - progress.json 업데이트
   - feature-status.json 상태 변경
   - git commit (해당 시)
   - 세션 기록 저장 (30-analysis/sessions/)
```

## Layer 2 기본 흐름 (Council 모드)

```
사용자 인풋
    │
    ▼
[독립 에이전트들 — 서로 교류 없음, 병렬 실행]
  Agent-A → 관점 A 분석
  Agent-B → 관점 B 분석
  Agent-C → 관점 C 분석
    │
    ▼
[Chairman — 메인 세션]
  모든 결과 수집 → 종합 → 판정
  (Go / Pivot / No-Go / 추가 분석)
    │
    ▼
[아웃풋 + 상태 저장]
  세션 파일 → 30-analysis/sessions/
  의사결정  → 50-decisions/
  교훈 축적 → 70-playbook/ (CARL 형식)
  지식 발견 → 40-knowledge-index/
  진행 상태 → progress.json 업데이트
```

## Layer 2 지식 순환 (CARL 형식)

→ `references/carl-format.md` 참조

```
[현재 케이스 분석]
        ↓
[세션 파일 저장]
        ↓
[교훈 추출 → 70-playbook/ CARL 형식]
  Context: 어떤 상황이었나
  Action: 무슨 판단/행동을 했나
  Result: 결과가 어떠했나
  Learning: 무엇을 배웠나
        ↓
[다음 케이스에서 자동 참조]
```

---

## 참조 파일

| 파일 | 언제 읽는가 |
|------|-----------|
| `references/agent-archetypes.md` | Phase 1에서 에이전트 구성 설계 시 |
| `references/folder-patterns.md` | Phase 1에서 폴더 구조 선택 시 |
| `references/claude-md-template.md` | Phase 2에서 CLAUDE.md 생성 시 |
| `references/session-handoff.md` | Phase 2에서 세션 핸드오프 설계 시 |
| `references/enforcement-patterns.md` | Phase 2에서 강제 규칙 설계 시 |
| `references/carl-format.md` | Phase 2에서 playbook 구조 설계 시 |
| `references/evaluator-protocol-workspace.md` | **Phase 3 GATE에서 자동 로드** — 5대 기둥 채점 실행 |
| `references/hook-catalog-workspace.md` | **Phase 3-8에서 자동 로드** — 환경 설정 제안 판단 기준 |
| `references/flow-history-template.md` | Stage 2.6에서 F1=예일 때 Generator가 읽어 05-flow-history/ + flow-change-protocol 생성 |
