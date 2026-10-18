---
name: harness-designer-coding
description: |
  코딩 에이전트가 코드를 안정적으로 생성·테스트·배포할 수 있는 하네스 구조를 설계하는 메타 스킬.
  Layer 1(메타): Planner→Generator→Evaluator 순환으로 코딩 하네스를 설계·구축·검증한다.
  Layer 2(운영): 완성된 하네스 안에서 코딩 에이전트가 실제 개발을 수행한다.
  "코딩 하네스 만들어줘", "개발 워크스페이스 설계", "에이전트 코딩 환경 구축",
  "CLAUDE.md 코딩 프로젝트용", "CI 파이프라인 설계", "코드 리뷰 루프 구축",
  "자율 코딩 환경", "에이전트 개발 환경", "coding harness", "agent-first development",
  "build harness for coding", "dev workspace setup", "autonomous coding environment"
  표현 시 반드시 사용.
---

# Coding Harness Designer v1

> "에이전트가 못한 건 능력 부족이 아니라, 환경이 부족했기 때문이다." — OpenAI
> "생성자가 자기 작업을 평가하게 하지 마라." — Anthropic
> "에이전트가 실수하면, 그 실수를 다시는 하지 못하도록 엔지니어링하라." — Mitchell Hashimoto

## 이 스킬과 harness-designer의 관계

```
┌─────────────────────────────────────────────────────────────┐
│  공통 기반: 하네스 설계 5대 기둥                                │
│  Progressive Disclosure / Mechanical Enforcement /           │
│  Feedback Loop / Session Continuity / Entropy Management     │
├──────────────────────────┬──────────────────────────────────┤
│  harness-designer (기존)  │  coding-harness-designer (이것)  │
│  분석·의사결정 워크스페이스  │  코딩·개발 워크스페이스            │
│  에이전트 = 관점 역할       │  에이전트 = 코딩 작업자            │
│  산출물 = 보고서·결정       │  산출물 = 소스 코드·테스트          │
│  검증 = 체크리스트·토론     │  검증 = CI·린터·브라우저 테스트     │
│  "회의실 설계"             │  "공장 라인 설계"                  │
└──────────────────────────┴──────────────────────────────────┘
```

---

## 코딩 하네스 7대 기둥

기존 5대 기둥에 코딩 전용 2개를 추가한다:

| 기둥 | 핵심 질문 | 원칙 |
|------|----------|------|
| **Progressive Disclosure** | 에이전트가 필요한 것만 볼 수 있는가? | AGENTS.md ~100줄 목차 → docs/ |
| **Mechanical Enforcement** | 아키텍처가 기계적으로 강제되는가? | 린터·구조 테스트·CI |
| **Feedback Loop** | 실패 시 에이전트가 자체 수정하는가? | 에러 메시지가 수정법을 가르침 |
| **Session Continuity** | 세션 간 핸드오프가 깨끗한가? | progress + feature-status + git |
| **Entropy Management** | 시간이 지나도 코드 품질이 유지되는가? | 자동 스캔·리팩터링·품질 등급 |
| **Architectural Rigidity** ← 신규 | 모듈 경계가 강제되는가? | 레이어 규칙·의존성 방향 검증 |
| **Observable Runtime** ← 신규 | 에이전트가 실행 결과를 볼 수 있는가? | 로그·메트릭·DOM·스크린샷 접근 |

---

## 두 레이어의 관계

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: 메타 (이 스킬의 역할)                                │
│                                                             │
│  Planner ──→ Generator ──→ Evaluator                        │
│     ↑         (단방향 순차, 역참조 금지)                      │
│     └──── 미흡 시 피드백 ─────────────────────────────┘      │
│                                                             │
│  목적: 코딩 하네스 구조를 설계·생성·검증                         │
└─────────────────────────┬───────────────────────────────────┘
                          │ 승인 후 하네스 완성
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 2: 운영 (완성된 코딩 하네스의 역할)                      │
│                                                             │
│  ┌ Initializer (첫 실행) ─→ 스캐폴드 + 환경 설정              │
│  │                                                          │
│  └ Coding Agent (반복 실행):                                 │
│    1. progress 읽기 → 다음 작업 선택                          │
│    2. 구현 (코드 생성)                                        │
│    3. 자체 검증 (테스트·린터·브라우저)                          │
│    4. 리뷰 요청 (에이전트 간 코드 리뷰)                        │
│    5. 피드백 반영 → 반복                                      │
│    6. clean state로 커밋                                     │
│                                                             │
│  목적: 실제 코드 작성·테스트·리팩터링·배포                       │
└─────────────────────────────────────────────────────────────┘
```

---

# LAYER 1: 메타 — 코딩 하네스 설계 프로세스

## L1 에이전트 3종 (단방향 순차, 역참조 금지)

### Planner (기획)
사용자 요구를 분석해서 코딩 하네스 구조를 설계한다.
- 인풋: 프로젝트 요구사항 (질문으로 수집)
- 아웃풋: 아키텍처 설계 + 폴더 구조 + 강제 규칙 + 평가 기준

### Generator (구축)
Planner 설계안을 실제 파일과 설정으로 만든다.
- 인풋: Planner 승인된 설계안
- 아웃풋: AGENTS.md, docs/, 린터 규칙, CI 설정, 테스트 구조

### Evaluator (검증)
Generator 산출물을 7대 기둥 기반으로 독립 검증한다.
- 인풋: Generator 생성 파일 + Planner 평가 기준
- 아웃풋: 기둥별 점수 + 기능적 검증 + 개선 피드백

---

## L1 Phase 0: Pattern Match — harness-100 참조 (신규 v1.1)

> "좋은 설계의 99%는 이미 누군가 만들어 놓았다. 찾아서 변형하라."

Discovery에 들어가기 **전에** harness-100(https://github.com/revfactory/harness-100, Apache-2.0)의 검증된 exemplar 중 가장 유사한 것을 찾아 참조 기준으로 삼는다. 비개발자는 `harness-starter-coding` 스킬로 전환 안내.

### 대상 exemplar (코딩 도메인 27개)
- Dev&DevOps #16–30: fullstack-webapp, mobile-app-builder, api-designer, database-architect, devops-pipeline, security-audit, performance-tuning, refactoring-squad, test-automation, monitoring-setup 등
- Data&AI/ML #31–42: ml-experiment, data-pipeline, rag-llm-app, nlp-processor, recommendation-engine, design-system 등

### Phase 0 절차
1. 사용자 1~2문장 요청에서 앱 유형 키워드 추출
2. 위 27개 중 상위 3개 후보 제시 + 사용자 확인
3. 선택된 exemplar 번호를 `_workspace/00_input.md`의 `reference_exemplar` 필드에 기록
4. 매칭 유사도 < 0.5 → **자유 설계 모드 폴백** (기존 Phase 1로 진행)

### Phase 0 결과를 이후 단계에 반영
- **Planner**: exemplar의 5인 에이전트 구성을 기본으로 하되, Scale Mode(Full/Reduced/Single)에 따라 조정
- **Generator**: exemplar 골격 스캐폴더 우선 사용, `_workspace/NN_*.md` 번호 컨벤션 강제
- **Evaluator**: exemplar의 Quality Standards 8항목(Agent Team Mode / Domain Expertise / Structured Outputs / Dependency DAG / Error Handling / Scale Modes / Test Scenarios / Trigger Boundaries)을 루브릭으로 사용

### Pattern Fidelity (정성 평가, Phase 0 한정)

> 7대 기둥 자동 채점에는 포함하지 않는다. Phase 0에서 exemplar 매칭 시 정성적으로 평가한다.

Phase 0에서 선택한 harness-100 exemplar의 8개 Quality Standards
(Agent Team Mode / Domain Expertise / Structured Outputs / Dependency DAG /
Error Handling / Scale Modes / Test Scenarios / Trigger Boundaries)를
Evaluator 채점과 별개로 점검한다.

- 적용 시점: Phase 0(exemplar 선택)에서 1회, Evaluator PASS 후 보고 시 1회
- 점수화 안 함: 7대 기둥 23항목 채점에 포함되지 않음
- pillar-weight: 7대 기둥의 가중치 조정만 가능. Pattern Fidelity는 가중치 대상 아님

### Trigger Boundaries (should + NOT)
Planner/Generator는 생성되는 orchestrator skill.md에 **반드시** `should-NOT trigger` 섹션을 포함한다. 예: "모바일 앱·엔터프라이즈 마이크로서비스·정적 웹사이트에는 사용 금지".

### Coding Agent Behavior Principles (Karpathy-inspired, 필수 주입)

Generator는 생성하는 `.claude/CLAUDE.md` 끝부분에 **반드시** 아래 섹션을 포함한다. 이 4원칙은 karpathy-guidelines 스킬(독립 설치됨)과 동기화되며, 하네스 내 모든 코딩 에이전트의 기본 행동 지침이 된다.

```markdown
## Coding Agent Behavior Principles (Karpathy-inspired)

모든 코딩 에이전트는 작업 시 아래 4원칙을 준수한다.
상세는 karpathy-guidelines 스킬 참조 (자동 트리거).

1. Think Before Coding — 가정 명시, 모호하면 질문, 대안 제시
2. Simplicity First — 요청한 만큼만. 사변적 추상화·기능 금지
3. Surgical Changes — 요청 라인만 변경. 주변 코드 개선 금지
4. Goal-Driven Execution — 검증 가능한 성공기준 → 루프 → 확인
```

Evaluator 체크리스트에 "CLAUDE.md 내 Karpathy 4원칙 섹션 존재 여부" 항목 추가.

### Scale Modes (운영층 기본값)
| 모드 | 에이전트 구성 |
|-----|------------|
| Full | architect + frontend + backend + qa + devops |
| Backend | architect + backend + qa |
| Frontend | architect + frontend + qa |
| Refactoring | architect + 관련 개발자 + qa |
| DevOps | devops 단독 |

---

## L1 Phase 1: Discovery — Planner 작동

Discovery는 4단계 질문으로 구성된다.
각 단계를 순서대로 진행하되, 사용자 답변에 따라 후속 질문이 분기된다.
**한 단계의 답변을 받은 후 다음 단계로 넘어간다.** 한꺼번에 묻지 않는다.

### 1-1. Stage 1 — 목적과 맥락 (WHY / WHO)

> 기술이 아닌, 이 프로젝트가 존재하는 이유를 파악한다.

```
P1. 이 프로젝트가 해결하려는 문제는 무엇인가?
    (어떤 불편함/비효율을 없애려 하는가?)

P2. 누가 사용하는가?
    (내부 직원 / 고객 / 개발자 / 불특정 다수)
    → 후속: 사용자 수는? IT 숙련도는?

P3. 이 프로젝트의 성공 기준은?
    (무엇이 되어야 "잘 만들었다"고 할 수 있는가?)

P4. 비슷한 기존 시스템이 있는가?
    (대체하는 것인가 / 새로 만드는 것인가)
    → 후속 [대체]: 기존 시스템의 가장 큰 문제점은?
    → 후속 [신규]: 벤치마크하는 서비스가 있는가?
```

**후속 질문 분기:**
- P2에서 "내부 직원" → "몇 명? 부서 구조가 있는가? 권한 체계가 필요한가?"
- P2에서 "고객" → "가입 방식은? 결제가 있는가? 개인정보 처리는?"
- P3에서 구체적 수치 언급 → "그 수치를 측정하는 방법은?"
- P3에서 모호한 답변 → "구체적으로 어떤 화면/기능이 동작하면 성공인가?"

### 1-2. Stage 2 — 기능과 내용 (WHAT)

> 무엇을 담는가, 핵심 기능은 무엇인가.

```
F1. 핵심 기능 3가지를 우선순위로 나열하면?
    (가장 먼저 동작해야 하는 것부터)

F2. 데이터의 성격은?
    (관계형 / 문서형 / 시계열 / 파일 / 복합)
    → 후속: 데이터 간 관계가 복잡한가? 집계/통계가 중요한가?

F3. 인증/권한 요구사항이 있는가?
    (없음 / 단순 로그인 / 역할 기반 / 조직 계층 권한)
    → 후속 [역할 기반 이상]: 권한 레벨은 몇 단계? 데이터 격리가 필요한가?

F4. 외부 시스템 연동이 있는가?
    (없음 / API 연동 / 파일 import/export / 결제 / 알림)

F5. 오프라인 또는 모바일 지원이 필요한가?
```

**후속 질문 분기:**
- F1에서 3개 이상 기능 → "각 기능의 복잡도를 상/중/하로 평가하면?"
- F2에서 "복합" → "어떤 종류가 섞이는가? 저장소를 분리해야 하는가?"
- F3에서 "조직 계층" → "부서 추가/변경이 잦은가? 코드 변경 없이 확장 가능해야 하는가?"

### 1-3. Stage 3 — 기술과 구조 (HOW)

> 어떻게 만들 것인가. Stage 1~2의 답변을 반영하여 적합한 기술을 제안한다.

```
T1. 기술 스택 선호가 있는가?
    (있으면 명시 / 없으면 "추천해줘")
    → "보링 테크놀로지" 권장: 에이전트는 안정적이고 학습 데이터가
      풍부한 기술로 더 잘 작동한다 (OpenAI 원안)
    → Stage 1~2 답변 기반으로 적합한 스택을 제안한다

T2. 배포 환경은?
    (Vercel / AWS / 사내 서버 / 모름)

T3. 코딩 에이전트 도구는?
    (Claude Code / Codex / Cursor / 기타)
    → 도구에 따라 하네스 설정 방식이 다름

T4. 에이전트의 자율성 수준은?
    (사람이 리뷰 후 머지 / 에이전트 간 리뷰 후 자동 머지 / 완전 자율)

T5. 프로젝트 규모와 기간은?
    (프로토타입 1~2주 / 중규모 1~3개월 / 대규모 장기)

T6. 기존 코드베이스가 있는가?
    (신규 / 기존 코드에 하네스 적용)
    → 기존 코드라면 점진적 적용 전략 설계
```

**후속 질문 분기:**
- T1에서 "추천해줘" → Stage 1~2 답변 기반으로 2~3개 옵션 비교표 제시 후 선택
- T2에서 "모름" → 사용자 규모와 기능 기반으로 추천
- T5에서 "대규모" → "팀 규모는? 동시 작업하는 에이전트 수는?"

### 1-3.5. Stage 3.5 — 플로우 변경 이력 추적 (FLOW HISTORY) [선택]

> 장기 프로젝트 또는 여러 세션에 걸쳐 코딩 하네스가 진화할 가능성이 있을 때 권장.
> 1~2주 프로토타입에서는 스킵해도 무방.

```
F1. "향후 프롬프트·프로토콜·템플릿·API 스크립트·커맨드·CLAUDE.md가 변경될 때
     이력을 남길까요?"

    용도:
    - 프로젝트 개선 이력 회고 (왜 이렇게 바뀌었는가)
    - 이전 버전으로 롤백이 필요할 때 근거 확보
    - 차기 유사 코딩 하네스 설계 시 참고

    ※ 새 세션마다 읽는 용도가 아닙니다.
      플로우를 수정·롤백·이식할 때만 참조합니다.

    → "아니오" → 05-flow-history/ 불포함. Stage 4로.
    → "예" → F2로.

F2. "초기 빌드(v1)를 change 0001 레코드로 자동 기록할까요?"
    - 기본값: 예 (Planner Discovery 답변이 설계 근거로 보존됨)
    - 아니오 → CHANGELOG만 생성하고 첫 변경 시 수동 기록
```

**플로우 이력 관리 원칙 (생성 후 운영 기준):**
이 이력은 **워크플로우 시스템**(프롬프트·프로토콜·템플릿·API 스크립트·커맨드·CLAUDE.md)의
변화만 기록한다. 시스템이 만들어낸 **산출물**(코드·보고서·분석 결과)은 기록 대상이 아니다.
구별 기준: "이 변경이 없었더라면 다음에 실행하는 결과가 달라지는가?"
→ 달라진다 = 시스템 변경 = 기록 / 달라지지 않는다 = 산출물 = 기록 불필요
상세: `00-system/protocols/flow-change-protocol.md`

**Planner 출력에 추가 (flow-history 관련):**
- `flow_history_enabled: true/false`
- `flow_history_initial_record: true/false` (F2 답변)

### 1-4. Stage 4 — 품질과 평가 기준 (QUALITY / EVALUATE)

> 사용자가 중요하게 생각하는 가치를 파악하고, 평가 기준을 합의한다.

```
E1. 이 프로젝트에서 가장 중요한 품질 속성은? (상위 3개 선택)
    □ 보안 (권한, 데이터 격리, 인증)
    □ 성능 (응답 속도, 동시 접속)
    □ 확장성 (코드 변경 없이 규모 확장)
    □ 유지보수성 (다른 사람/에이전트가 쉽게 수정)
    □ 사용자 경험 (직관적 UI, 빠른 반응)
    □ 테스트 가능성 (자동 테스트로 품질 보증)
    □ 빠른 출시 (MVP 우선, 완성도는 나중에)
    □ 데이터 정합성 (정확한 기록, 누락 방지)

E2. 향후 확장 계획이 있는가?
    (없음 / 기능 추가 / 다른 시스템과 결합 / 사용자 규모 확장)
    → 후속: 구체적으로 어떤 확장? 시기는?

E3. 이 프로젝트에서 절대 타협하면 안 되는 것은?
    (예: "권한 격리가 깨지면 안 된다", "데이터가 유실되면 안 된다")

E4. 반대로, 초기에는 없어도 괜찮은 것은?
    (예: "모바일 대응은 나중에", "통계 대시보드는 2차에")
```

**후속 질문 분기:**
- E1에서 "보안" 선택 → "어떤 종류의 보안? 인증/권한/데이터 암호화/감사 로그?"
- E2에서 "다른 시스템과 결합" → "어떤 시스템? 데이터 형식은 호환되는가?"
- E3의 답변 → Evaluator 가중치의 핵심 입력으로 사용

### 1-5. 평가 가중치 합의 (Stage 4 완료 후)

Stage 1~4의 답변을 분석하여 **7대 기둥의 가중치를 제안**한다.
사용자와 합의하여 최종 확정한다.

```
[가중치 제안 프로세스]

STEP 1. Stage 1~4 답변에서 키워드 추출
  - "권한 격리" → Mechanical Enforcement, Architectural Rigidity ↑
  - "코드 변경 없이 확장" → Architectural Rigidity ↑
  - "빠른 출시" → Entropy Management ↓, Observable Runtime ↑
  - "데이터 정합성" → Feedback Loop ↑, Mechanical Enforcement ↑

STEP 2. 기본 가중치에서 조정하여 제안

  기본 가중치 (프로젝트 특성 반영 전):
  | 기둥 | 기본 | 조정 근거 | 제안 |
  |------|------|----------|------|
  | Progressive Disclosure | 15% | (변동 근거) | ?% |
  | Mechanical Enforcement | 20% | (변동 근거) | ?% |
  | Feedback Loop | 15% | (변동 근거) | ?% |
  | Session Continuity | 10% | (변동 근거) | ?% |
  | Entropy Management | 10% | (변동 근거) | ?% |
  | Architectural Rigidity | 20% | (변동 근거) | ?% |
  | Observable Runtime | 10% | (변동 근거) | ?% |

  "이 프로젝트에서는 [근거]를 고려하여
   [기둥]의 가중치를 [기본]% → [제안]%로 조정했습니다.
   의견이나 수정 사항이 있으시면 말씀해주세요."

STEP 3. 사용자 피드백 반영
  - 동의 → 확정
  - "보안을 더 높여줘" → 관련 기둥 가중치 상향, 다른 기둥 하향 후 재제안
  - "이 기둥은 필요 없어" → 0%로 설정, 나머지 재분배 후 재제안

STEP 4. 최종 승인
  "최종 가중치를 확정합니다. 이 가중치로 Evaluator가 채점합니다."
  → evaluator-protocol.md의 기본 가중치 대신 이 합의된 가중치를 사용
```

### 1-6. 아키텍처 패턴 자동 매핑

→ `references/architecture-patterns.md` 참조
→ Stage 2~3 답변 기반으로 가장 적합한 패턴을 제안한다

| 애플리케이션 유형 | 추천 레이어 구조 |
|-----------------|-----------------|
| 풀스택 웹앱 | Types→Config→Repo→Service→Runtime→UI |
| API 서비스 | Types→Config→Repo→Service→Runtime |
| CLI 도구 | Types→Config→Core→CLI |
| 라이브러리 | Types→Core→Public API |

### 1-7. Planner 산출물

**① 프로젝트 컨텍스트 요약** — 목적, 사용자, 성공 기준, 핵심 제약 (Stage 1~2 기반)
**② 아키텍처 설계안** — 레이어 구조, 모듈 경계, 의존성 방향
**③ 폴더 구조 초안** — references/coding-folder-patterns.md 기반
**④ 강제 규칙 설계** — 어떤 규칙을 린터/CI/구조 테스트로 강제하는가
**⑤ 테스트 전략** — 유닛/통합/E2E 범위와 커버리지 기준
**⑥ 에이전트 자율성 설계** — 리뷰 루프, 승인 게이트, 에스컬레이션 기준
**⑦ 확장 전략** — 향후 확장에 대비한 설계 결정 (Stage 4 E2 기반)
**⑧ 평가 기준 + 합의된 가중치** — 7대 기둥 체크리스트 + 가중치 테이블

```
[Planner 완료 — 사용자 승인 요청]
①~⑧을 검토 후 수정 사항 말씀해주세요.
승인되면 Generator가 구축을 시작합니다.
```

---

## L1 Phase 2: Build — Generator 작동

### 2-1. 핵심 산출물 생성 (순서대로)

| 순번 | 산출물 | 설명 |
|------|--------|------|
| 2-1a | 아키텍처 다이어그램 | Mermaid — 레이어·모듈·의존성 방향 |
| 2-1b | AGENTS.md (~100줄) | 목차 역할, 참조 라우팅 포함 |
| 2-1c | docs/ 디렉터리 | 아래 상세 |
| 2-1d | 아키텍처 강제 규칙 | 린터 규칙 + 구조 테스트 |
| 2-1e | CI/CD 파이프라인 설계 | 검증 게이트 정의 |
| 2-1f | 테스트 구조 | 테스트 디렉터리 + 기본 설정 |
| 2-1g | 세션 핸드오프 산출물 | progress.json + feature-status.json |
| 2-1h | 코드 리뷰 루프 설정 | 에이전트 간 리뷰 프로토콜 |
| 2-1i | 관찰 가능성 설정 | 로그·메트릭·DOM 접근 방법 |
| 2-1j | README.md | 개발자 가이드 |
| 2-1k | bkit 프로젝트 초기화 | T3에서 Claude Code + bkit 설치 감지 시 **사용자 opt-in 질문 후에만** 실행 (아래 상세) |
| 2-1l | 환경 설정 | 가상환경·환경변수·훅 — **강제 생성 안 함. Phase 3-7에서 LLM 제안 후 사용자 선택** |
| 2-1m | 플로우 변경 이력 위키 (선택) | Stage 3.5 F1=예일 때만. ~/.claude/skills/harness-designer-workspace/references/flow-history-template.md 참조하여 05-flow-history/ + 00-system/protocols/flow-change-protocol.md 생성. AGENTS.md에 라우팅 2행 + "플로우 변경 추적 (선별 기록)" 섹션 추가. **관리 원칙**: 시스템(규칙·절차·도구) 변화만 기록. 산출물(코드·보고서)은 기록 불필요. 구별 기준: "이 변경이 없었더라면 다음 실행 결과가 달라지는가?" |

### 2-1b. AGENTS.md 작성 규칙 (최중요)

→ `references/agents-md-template.md` 참조

OpenAI 원안의 핵심 교훈을 그대로 적용:

**~100줄 목차.** 백과사전이 아니다.
```markdown
# [프로젝트명]

> [한 줄 설명]

## 아키텍처 개요
[레이어 구조 3줄 요약]
→ 상세: docs/architecture.md

## 참조 라우팅
| 상황 | 읽을 파일 |
|------|----------|
| 아키텍처 규칙 | → docs/architecture.md |
| 코딩 컨벤션 | → docs/conventions.md |
| 도메인 설계 | → docs/design/[domain].md |
| 실행 계획 | → docs/exec-plans/[plan].md |
| 품질 등급 | → docs/quality-grades.md |
| 기술 부채 | → docs/exec-plans/tech-debt-tracker.md |
| 세션 상태 | → progress.json |
| 기능 현황 | → feature-status.json |

## 핵심 규칙 (5가지 이내)
1. [불변 규칙 1 — 예: "모든 경계에서 데이터 형태를 검증"]
2. [불변 규칙 2 — 예: "레이어 역방향 의존 금지"]
3. [불변 규칙 3]

## 테스트 규칙
→ docs/testing-strategy.md

## 커맨드
| 커맨드 | 기능 |
|--------|------|
| /implement [기능] | 기능 구현 |
| /review | 코드 리뷰 실행 |
| /test | 테스트 실행 |
| /refactor [대상] | 리팩터링 |

## 최종 업데이트: YYYY-MM-DD
```

### 2-1c. docs/ 디렉터리 (System of Record)

→ `references/docs-structure.md` 참조

```
docs/
├── architecture.md         ← 레이어 구조, 모듈 경계, 의존성 규칙
├── conventions.md          ← 코딩 컨벤션, 네이밍, 파일 구조
├── quality-grades.md       ← 도메인/레이어별 품질 등급 (A~F)
├── testing-strategy.md     ← 테스트 유형, 커버리지 기준, 실행 방법
├── design/                 ← 도메인별 설계 문서
│   ├── [domain-a].md
│   └── [domain-b].md
├── exec-plans/             ← 실행 계획, 기술 부채 추적
│   ├── tech-debt-tracker.md
│   └── [plan-name].md
└── review-protocol.md      ← 에이전트 간 코드 리뷰 규칙
```

**핵심:** 이 디렉터리가 에이전트의 "유일한 진실의 원천(single source of truth)"이다.
Google Docs, Slack, 사람 머릿속에 있는 지식은 에이전트에게 존재하지 않는다.

### 2-1d. 아키텍처 강제 규칙

→ `references/enforcement-coding.md` 참조

문서화가 아닌 **기계적 강제**:

| 규칙 | 강제 수단 | 예시 |
|------|----------|------|
| 레이어 의존성 방향 | 구조 테스트 | UI가 Repo를 직접 import 하면 실패 |
| 경계 데이터 검증 | 린터 규칙 | 외부 입력은 반드시 스키마 검증 |
| 유틸리티 중앙화 | 린터 규칙 | 중복 헬퍼 함수 생성 시 경고 |
| 커밋 메시지 형식 | git hook | conventional commit 강제 |
| 테스트 커버리지 | CI 게이트 | 커버리지 미달 시 머지 차단 |

**에러 메시지 원칙:**
린터/테스트 에러 메시지는 **수정 방법을 가르쳐야** 한다.
에이전트가 에러를 보고 즉시 수정할 수 있도록:

```
❌ 나쁜 에러: "Layer violation detected"
✅ 좋은 에러: "Layer violation: UI layer cannot import from Repo layer.
   Move this logic to a Service layer function, then import from Service.
   See docs/architecture.md#layer-rules"
```

### 2-1e. CI/CD 파이프라인 설계

```
PR 생성
    │
    ▼
┌──────────────────────────────────────┐
│  Gate 1: 린트 + 타입 체크             │
│  (구조 테스트, import 규칙, 형식)      │
├──────────────────────────────────────┤
│  Gate 2: 유닛 테스트                  │
│  (커버리지 기준 충족 확인)             │
├──────────────────────────────────────┤
│  Gate 3: 통합/E2E 테스트              │
│  (브라우저 자동화, API 테스트)         │
├──────────────────────────────────────┤
│  Gate 4: 에이전트 코드 리뷰           │
│  (또는 사람 리뷰 — 자율성 수준에 따라)  │
└──────────────────────────────────────┘
    │
    ▼
  머지 승인
```

### 2-1f~g. 테스트 구조 + 세션 핸드오프

**테스트 구조:** Planner 설계 기반으로 테스트 디렉터리, 기본 설정, 실행 스크립트 생성
**세션 핸드오프:** progress.json + feature-status.json (harness-designer v4와 동일 스키마)

### 2-1h. 코드 리뷰 루프 (Ralph Wiggum Loop)

→ `references/review-loop.md` 참조

```
코딩 에이전트가 코드 작성
    │
    ▼
자체 로컬 리뷰 (린트, 테스트)
    │
    ▼
PR 생성
    │
    ▼
리뷰 에이전트(들)에게 리뷰 요청
    │
    ▼
피드백 수신 → 수정 반영
    │
    ▼
리뷰 통과까지 반복
    │
    ▼
[자율성 수준에 따라]
  ├─ 레벨 1: 사람이 최종 승인 후 머지
  ├─ 레벨 2: 에이전트 리뷰 통과 시 자동 머지
  └─ 레벨 3: 완전 자율 + 모니터링 알림
```

**사람 에스컬레이션 기준:**
- 새로운 아키텍처 결정
- 보안 관련 변경
- 제품 방향 판단이 필요한 경우
- 에이전트 간 의견 불일치

### 2-1i. 관찰 가능성 (Observable Runtime)

→ `references/observability.md` 참조

에이전트가 "자기가 만든 것이 실제로 동작하는지" 볼 수 있어야 한다:

| 관찰 수단 | 용도 | 설정 방법 |
|----------|------|----------|
| 브라우저 자동화 | UI 동작 확인 | Playwright/Puppeteer MCP |
| 로그 쿼리 | 에러/경고 확인 | 로컬 로그 파일 또는 LogQL |
| 메트릭 쿼리 | 성능 확인 | PromQL 또는 앱 내장 메트릭 |
| DOM 스냅샷 | UI 상태 확인 | Chrome DevTools Protocol |
| curl/httpie | API 동작 확인 | 직접 호출 |

### 2-1k. bkit 프로젝트 초기화 (Claude Code + bkit 설치 + 사용자 opt-in일 때만)

Discovery Stage 3의 T3에서 "Claude Code"이고 bkit 플러그인이 설치되어 있으면,
Generator가 하네스 구축의 마지막 단계로 **bkit 연동 여부를 사용자에게 질문**하고,
승인받은 경우에만 초기화를 실행한다. **자동 활성화 금지.**

**전제 (권한 관계):**
Layer 2 검증 루프는 bkit 없이 완결 작동한다 (`references/layer2-verification-loop.md`).
bkit은 검증기를 증강하는 선택 요소이며, 연동해도 하네스 강제 규칙(GATE·잠금 목록·
예산 상한)이 bkit 제안보다 항상 우선한다 (동 문서 §7 권한 서열).
과거 bkit 자동 트리거가 하네스 규칙과 권한 충돌을 일으킨 전례가 있어 opt-in으로 제한한다.

**실행 내용:**
```
1. bkit 설치 여부 확인
   → ~/.claude/skills/bkit-rules/SKILL.md 존재 확인 (Glob)
   → 없으면 스킵 (bkit 미설치 환경 — Layer 2는 자체 검증 루프로 완결 작동)

2. 사용자 opt-in 질문 (자동 활성화 금지)
   → "bkit이 설치되어 있습니다. Layer 2 검증에 bkit을 연동할까요?
      연동해도 하네스 강제 규칙이 bkit 제안보다 우선합니다."
   → 거절 시 스킵 (자체 검증 루프 사용)

3. 프로젝트 레벨 감지 결과를 CLAUDE.md에 공식 등록
   → "## Project Level: Dynamic" (또는 Starter/Enterprise)
   → bkit-rules가 이 선언을 읽고 레벨별 행동을 자동 적용

4. .bkit-memory.json 생성 (프로젝트 루트)
   {
     "level": "dynamic",
     "initialized": "YYYY-MM-DD",
     "harnessDesigned": true,
     "features": []
   }

5. CLAUDE.md에 bkit 연동 선언 추가 (이미 없는 경우)
   → "bkit PDCA 적용 (사용자 승인됨)"
   → 권한 서열 명시: "하네스 GATE·잠금 목록·예산 상한은 bkit 제안으로
      변경 불가 (references/layer2-verification-loop.md §7)"
   → 이식성 주석: "bkit 미설치 PC에서 이 선언은 no-op으로 무시"
```

**스킵 조건:**
- T3에서 "Claude Code"가 아닌 경우 → 스킵
- bkit-rules SKILL.md가 없는 경우 → 스킵
- 사용자가 opt-in을 거절한 경우 → 스킵
- .bkit-memory.json이 이미 존재하는 경우 → 스킵

### 2-1l. 환경 설정 (Phase 3-7에서 제안)

가상환경·환경변수·훅 설정은 **Generator 단계에서 강제 생성하지 않는다.**
Layer 1 완료(Evaluator PASS) 후 Phase 3-7에서 LLM이 프로젝트를 분석하여
사용자에게 제안하고, 사용자 선택 후 생성한다.

→ 상세 절차: Phase 3-7 (환경 설정 제안) 참조
→ 판단 기준: `references/hook-catalog.md` 참조

```
[GATE: Generator → Evaluator 강제 전환]
이 절차는 건너뛸 수 없다. Generator 완료 즉시 실행한다.

STEP 1. 산출물 존재 확인
  아래 10종 각각에 대해 Glob으로 존재 + Read로 비어있지 않음을 확인한다:
  □ AGENTS.md (또는 CLAUDE.md 내 동등 섹션)
  □ docs/architecture.md
  □ docs/conventions.md
  □ docs/design/ 내 도메인 설계 문서 1개 이상
  □ docs/testing-strategy.md
  □ docs/quality-grades.md
  □ docs/exec-plans/tech-debt-tracker.md
  □ progress.json
  □ feature-status.json
  □ 강제 규칙 파일 (린터 설정, CI 설계, 또는 구조 테스트 스크립트)
  □ bkit 초기화 (Claude Code + bkit 설치 + 사용자 opt-in일 때만):
    .bkit-memory.json 존재 + CLAUDE.md에 Level 선언 + 권한 서열 명시

  □ (Stage 3.5 F1=예) 05-flow-history/README.md, CHANGELOG.md, changes/TEMPLATE.md, snapshots/v1.md
  □ (Stage 3.5 F1=예) 00-system/protocols/flow-change-protocol.md
  □ (Stage 3.5 F1=예, F2=예) 05-flow-history/changes/0001-*-initial-harness.md

  → 미존재 파일이 있으면: Generator로 돌아가서 해당 파일만 생성
  → 모두 존재하면: STEP 2로 진행

STEP 2. Evaluator 프로토콜 실행
  → references/evaluator-protocol.md 를 읽고 그 절차를 그대로 실행한다
  → 7대 기둥 채점 (총 23항목, 기둥 2는 5항목·나머지 3항목씩)
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

→ `references/evaluator-protocol.md` 를 읽고 그대로 실행한다.

요약: 7대 기둥 총 23항목 (기둥 2는 5항목, 나머지 3항목씩)을 PASS/PARTIAL/FAIL로 채점.
가중치 적용 후 100점 만점으로 총점 산출. 결과를 보고 형식으로 출력.

### 3-2. 피드백 루프 (점수별 분기)

| 총점 | 판정 | 구체적 행동 |
|------|------|------------|
| 90점+ | **PASS** | Cartesian Review(3-5) → 경량화(3-6) → 환경 설정 제안(3-7) → Layer 2 전환 |
| 70~89점 | **REWORK** | FAIL/PARTIAL 항목별 피드백 생성 → Generator가 해당 파일만 수정 → Evaluator 재실행 |
| 70점 미만 | **REDESIGN** | 근본 원인 분석 → Planner의 어떤 설계 결정이 문제인지 식별 → Discovery 재시작 |

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

7대 기둥 채점이 PASS(90점+)여도 놓칠 수 있는 실용적 결함을 데카르트 5렌즈로 추가 검토한다.

```
[cartesian-review 호출 파라미터]
검토 대상:    Generator 산출물 전체 (AGENTS.md + docs/ + 강제 규칙 파일 + CI 설계)
L5 관점:      자동 고정 →
              "이 코딩 하네스를 처음 받아서 AGENTS.md만 읽고 바로 코드를 작성해야 하는 에이전트.
               무엇이 막히는가? 무엇이 모호한가? 무엇을 잘못 이해할 수 있는가?
               CI/린터 에러 메시지가 수정 방법을 알려주는가?"
L5 의심 범위: A (과정 한정) — 자동 고정. STEP 0.5 사용자 질문은 생략한다.
              (이유: 검증 대상은 Generator 산출물이지 사용자 어젠다가 아니다)
```

**cartesian-review 결과 처리**

| 결과 | 처리 |
|---|---|
| L1 높음 항목 발견 | Generator 재작업 대상에 추가 → 3-2로 복귀 |
| L4 높음 항목 발견 | Generator 불필요 요소 제거 → 3-2로 복귀 |
| L2·L3만 발견 | 사용자에게 보고 후 승인 받고 3-6으로 진행 |
| "사용자 확인 필요 가정" 발견 | 사용자에게 보고 후 답변 받고 3-6으로 진행 (Generator 재작업 아님) |
| 발견 없음 | 즉시 3-6으로 진행 |

**미설치 안내 (건너뛸 경우)**
```
⚠️ cartesian-review 스킬이 감지되지 않았습니다.
   데카르트 5렌즈 추가 검증을 건너뜁니다.
   설치 후 재실행하면 더 정밀한 품질 검증이 가능합니다.
   설치: ~/.claude/skills/ 또는 .claude/skills/ 에 cartesian-review 폴더 배치
```

### 3-6. 하네스 경량화 검토 (PASS 판정 후 실행)

```
[경량화 체크리스트]
- [ ] 이 규칙 중 현재 모델이 자체 준수할 수 있는 것은?
- [ ] CI 게이트 중 과잉인 것은?
- [ ] 에이전트 자율성을 높여도 되는 영역은?
- [ ] 프로젝트 규모에 비해 과도한 구조는?
```

> "모델이 좋아질수록 하네스는 단순해져야 한다." — Anthropic

---

### 3-7. 환경 설정 제안 (PASS 판정 후 실행, 선택 사항)

> "강제하지 않는다. 판단하고 제안한다. 선택은 사용자가 한다."

Evaluator PASS 직후, Layer 2 전환 전에 실행한다.
Discovery 답변에서 수집한 tech stack·프로젝트 유형을 기반으로
`references/hook-catalog.md`를 읽어 아래 3가지 영역을 분석하고 제안한다.

**이 단계는 자동 생성하지 않는다.**
제안만 하고, 사용자가 선택한 항목만 이후 프롬프트로 생성한다.

#### 실행 절차

**STEP 1. 프로젝트 컨텍스트 요약**

Discovery 답변에서 아래를 추출한다:
```
- 주요 언어/런타임: (예: Python 3.11, Node 20)
- 프레임워크: (예: FastAPI, React)
- 패키지 매니저: (예: pip, npm, poetry)
- 프로젝트 유형: (예: API 서버, 풀스택 웹앱, CLI 도구)
- 협업 여부: (예: 개인 / 팀)
```

**STEP 2. hook-catalog.md 조회**

→ `references/hook-catalog.md`를 읽고 tech stack에 해당하는 항목을 필터링한다.
→ 필요 없다고 판단되는 항목은 제안 목록에서 제외한다 (이유 포함).

**STEP 3. 제안 출력**

아래 형식으로 사용자에게 출력한다:

```
## 🛠 환경 설정 제안

프로젝트: [프로젝트명] | 스택: [주요 언어/프레임워크]

---

### A. 가상환경

| # | 도구 | 생성 파일 | 이유 |
|---|------|---------|------|
| A1 | [예: python venv] | `.python-version`, `requirements.txt` | [판단 근거] |

---

### B. 환경변수

| # | 항목 | 생성 파일 | 포함 키 예시 |
|---|------|---------|------------|
| B1 | .env 스키마 | `.env.example`, `.gitignore` 추가 | DATABASE_URL, API_KEY, PORT |

---

### C. 훅 (Hook)

| # | 종류 | 실행 시점 | 내용 | 생성 파일 |
|---|------|---------|------|---------|
| C1 | Claude Code Hook | PostToolUse | 코드 수정 후 린터 자동 실행 | `.claude/settings.json` |
| C2 | Git Hook | pre-commit | 커밋 전 포맷 + 테스트 | `.git/hooks/pre-commit` |
| C3 | pre-commit 프레임워크 | git commit 시 | secret 탐지, 코드 품질 | `.pre-commit-config.yaml` |

---

원하는 항목 번호를 알려주세요. (예: "A1, C1, C2 만들어줘")
전부 건너뛰려면 "건너뛰기"라고 하시면 Layer 2로 바로 이동합니다.
```

**STEP 4. 사용자 선택 처리**

| 사용자 응답 | 처리 방법 |
|-----------|---------|
| 항목 번호 지정 ("A1, C1") | 해당 파일만 즉시 생성 후 Layer 2 전환 |
| "전부" / "다" | 전체 항목 생성 후 Layer 2 전환 |
| "건너뛰기" / "스킵" | 생성 없이 Layer 2 바로 전환 |
| 번호 없이 질문 | 해당 항목 추가 설명 후 재선택 대기 |

**생성 시 원칙:**
- `.env.example`은 키 이름과 설명만 포함, 실제 값은 절대 기입하지 않는다
- `.env`는 생성하지 않는다 (사람이 직접 생성)
- 훅 스크립트는 실행 가능한 완전한 코드로 생성한다
- 생성된 파일 목록을 CLAUDE.md 참조 라우팅 테이블에 추가한다

---

# LAYER 2: 운영 — 완성된 코딩 하네스

## 에이전트 행동 강제 규칙 (Layer 2 전체 적용)

> 이 규칙은 Layer 2의 모든 단계에 적용된다. 예외 없음.

1. **검증 생략은 에이전트가 결정할 수 없다.**
2. 스킬에 정의된 단계를 건너뛰고 싶으면, **반드시 한국어로 사용자에게**:
   - 스킬에서 요구하는 단계가 무엇인지 설명
   - 왜 건너뛰어도 되는지 이유를 제시
   - 사용자의 **명시적 승인**을 받은 후에만 건너뛰기
3. 사용자가 "빨리 해", "진행해", "계속해" 등 속도를 요구해도,
   **이것은 검증 생략 승인이 아니다.**
   검증 생략은 "검증 건너뛰어", "검증 안 해도 돼", "검증 루프 안 돌려도 돼" 등
   **명시적으로 검증을 언급**해야만 승인으로 간주한다.
4. 이 규칙을 위반하면 즉시 사용자에게 보고하고 되돌린다.
5. **"간단한 변경이라 검증이 필요 없다"는 에이전트의 자율 판단은 금지**한다.
   간단한지 여부도 사용자가 판단한다.

---

## Initializer / Coding Agent 분리

### Initializer (첫 실행 1회만)

```
1. 프로젝트 스캐폴드 생성 (패키지 매니저, 프레임워크 초기화)
2. CI 설정 파일 생성
3. 린터/포매터 설정
4. 테스트 프레임워크 설정
5. progress.json 초기화
6. feature-status.json 생성 (사용자 요구사항 → 200+ 기능 분해)
7. init.sh 작성 (개발 서버 시작, 기본 테스트)
8. 초기 git commit
```

### Coding Agent (매 세션 반복)

```
1. pwd 확인
2. progress.json 읽기 → 현재 상태 파악
3. feature-status.json 확인 → 다음 작업 선택
4. git log --oneline -20 → 최근 변경 이력
5. init.sh 실행 → 기본 동작 테스트
   (깨진 상태면 먼저 수정)
6. 기능 하나 구현:
   a. 코드 작성
   b. 테스트 작성
   c. 린터 통과 확인
   d. 브라우저/API 테스트로 E2E 확인
```

```
[GATE: 검증 — 이 단계는 건너뛸 수 없다]
이 GATE는 Layer 1의 Generator→Evaluator GATE와 동일한 강제력을 가진다.
사용자가 명시적으로 "검증 건너뛰어"라고 한 경우에만 생략 가능.

7. [검증 루프] — references/layer2-verification-loop.md 자동 로드
   a. 기계 검증: 전체 테스트 통과 + 린터 에러 0
   b. 검증 서브에이전트(생성 에이전트와 분리, 자가채점 금지)가
      review-loop.md 6항목 체크리스트로 검증 → Critical 0개 확인 후 통과
   c. bkit 설치 + 사용자 opt-in 시에만: code-analyzer/gap-detector가
      b의 검증 서브에이전트 역할 수행 (matchRate ≥ 90% 기준,
      권한 서열·잠금 목록은 layer2-verification-loop.md §7)
   d. 실패 출구: 검증 반복 예산(기본 5회, progress.json 기록) 소진 또는
      같은 오류 시그니처 3회 연속 → 무한 재시도 금지,
      진단 리포트 생성 후 사람 에스컬레이션

   이 GATE를 통과하지 않으면 커밋할 수 없다.
   검증 결과를 사용자에게 한국어로 보고한 후 커밋 진행.

8. feature-status.json 업데이트 (검증 통과 후에만 passes: true)
9. progress.json 업데이트
10. git commit (설명적 메시지)
```

## 엔트로피 관리 (지속적 품질 유지)

```
[주기적 자동 스캔 — 배경 에이전트 또는 수동 트리거]
    │
    ▼
docs/quality-grades.md 업데이트
    │ (각 도메인/레이어별 A~F 등급)
    │
    ▼
docs/exec-plans/tech-debt-tracker.md 업데이트
    │ (부채 항목 + 우선순위)
    │
    ▼
리팩터링 PR 생성
    │ (소량씩, 매일)
    │
    ▼
"기술 부채는 고이자 대출. 매일 소액 상환이 몰아서 하는 것보다 낫다."
```

---

## 보링 테크놀로지 원칙

에이전트는 다음 조건의 기술로 더 잘 작동한다:
- 학습 데이터가 풍부 (Stack Overflow 답변 다수)
- API가 안정적 (버전 간 호환)
- 구성 가능하고 조합 가능 (composable)
- 불투명한 동작이 적음

최신 프레임워크보다 "지루한" 기술이 에이전트에게는 더 좋은 기반이다.
때로는 외부 라이브러리를 가져오는 것보다
기능의 부분 집합을 직접 구현하는 것이 더 저렴하다.

---

## 참조 파일

| 파일 | 언제 읽는가 |
|------|-----------|
| `references/architecture-patterns.md` | Phase 1에서 아키텍처 설계 시 |
| `references/coding-folder-patterns.md` | Phase 1에서 폴더 구조 선택 시 |
| `references/agents-md-template.md` | Phase 2에서 AGENTS.md 생성 시 |
| `references/docs-structure.md` | Phase 2에서 docs/ 디렉터리 설계 시 |
| `references/enforcement-coding.md` | Phase 2에서 린터/CI 규칙 설계 시 |
| `references/review-loop.md` | Phase 2에서 코드 리뷰 루프 설계 시 |
| `references/observability.md` | Phase 2에서 관찰 가능성 설정 시 |
| `references/evaluator-protocol.md` | **Phase 3 GATE에서 자동 로드** — 7대 기둥 채점 실행 |
| `references/layer2-verification-loop.md` | **Layer 2 GATE에서 자동 로드** — 검증 루프·실패 출구·예산 상한·bkit 권한 서열 |
