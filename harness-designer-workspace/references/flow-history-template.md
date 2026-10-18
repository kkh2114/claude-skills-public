# Flow History Template — 재사용 스캐폴딩

> 새 하네스에 "플로우 변경 이력 추적" 기능을 탑재할 때 Generator가 **이 파일만 참조**하여 5개 파일을 생성한다.

## 언제 쓰이나

Planner 단계(Discovery)에서 다음 질문에 "예" 승인한 경우:

> **"향후 워크플로우가 개선되거나 변경될 때 이력을 남길까요?"**
>
> 이 이력은 회고·롤백·차기 유사 프로젝트 참고용으로 사용됩니다.
> **새 세션마다 읽는 용도가 아닙니다** — 플로우 수정·롤백·이식할 때만 참조합니다.
>
> - **예** → `05-flow-history/` 위키 + `flow-change-protocol.md` 생성
> - **아니오** → 생성하지 않음 (이후에도 수동으로 필요 시 이 템플릿으로 추가 가능)

## 생성 파일 5종

Generator는 아래 5개 파일을 생성한다. 대괄호 `[...]` 부분은 프로젝트별 치환.

### 파일 1: `05-flow-history/README.md`

```markdown
# Flow History Wiki

> [프로젝트명]의 워크플로우 변경 이력을 추적하는 전용 공간.
> **회고용·롤백용·차기 프로젝트 참고용**으로 설계되었다.

## 이 위키를 언제 열어보는가

- 이 프로젝트가 어떻게 개선되어 왔는지 **되돌아볼 때**
- 이전 버전으로 **롤백**하거나 그 내용·범위를 확인할 때
- 비슷한 프로젝트를 **새로 만들 때** 설계 참고
- A/B 비교 테스트 때 legacy 버전 실행 근거 확인

**일반 운영 작업 시에는 열 필요 없다.**

## 구성

\`\`\`
05-flow-history/
├── README.md           ← 이 파일 (위키 진입점)
├── CHANGELOG.md        ← 시간순 타임라인 (한 줄 인덱스)
├── changes/            ← 변경 단위별 상세 기록
│   └── NNNN-YYYY-MM-DD-slug.md
└── snapshots/          ← 버전별 전체 상태 포인터
    └── v[N].md
\`\`\`

## 네비게이션

| 목적 | 경로 |
|------|------|
| 최근 변경 한눈에 보기 | [CHANGELOG.md](CHANGELOG.md) |
| 특정 변경 상세 | [changes/](changes/) |
| 버전별 스냅샷 | [snapshots/](snapshots/) |
| Legacy 버전 실물 | `00-system/legacy/v[N-1]-system/` (Breaking 변경 시 생성) |

## 변경 레코드 템플릿

[changes/TEMPLATE.md](changes/TEMPLATE.md)

→ 상세 절차: [00-system/protocols/flow-change-protocol.md](../00-system/protocols/flow-change-protocol.md)
```

### 파일 2: `05-flow-history/CHANGELOG.md`

```markdown
# Flow Changelog — [프로젝트명] 워크플로우 변경 타임라인

> 시간순 인덱스 (최신이 위). 한 줄 요약만 기재. 상세는 `changes/` 참조.

## [현재연도]

- **YYYY-MM-DD** · v1 초기 빌드 — [프로젝트명] 하네스 생성. 상세: [changes/0001-YYYY-MM-DD-initial-harness.md](changes/0001-YYYY-MM-DD-initial-harness.md)

## 버전 인덱스

| 버전 | 도입일 | 핵심 특징 | 스냅샷 |
|------|--------|----------|--------|
| v1 (현재) | YYYY-MM-DD | 초기 하네스 빌드 | [snapshots/v1.md](snapshots/v1.md) |
```

Generator는 초기 빌드 자체를 change 0001로 기록한다 (실물 작성은 아래 파일 4 참조).

### 파일 3: `05-flow-history/changes/TEMPLATE.md`

```markdown
# [NNNN] [변경 제목]

## 메타
- **번호**: NNNN (4자리 순번)
- **일시**: YYYY-MM-DD
- **변경자**: [사용자명 또는 세션 ID]
- **영향 범위**: [major / breaking] (minor 문구 정정은 기록하지 않음)
- **이전 버전**: v[N-1]
- **새 버전**: v[N]

## 동기 (Why)

[무엇 때문에 이 변경이 필요했는가]

## 변경 내용 (What)

### 수정된 파일

| 파일 | 변경 요약 |
|------|----------|
| `path/to/file.md` | [변경 사항] |

### 변경 전 (v[N-1])

[핵심만 간결하게]

### 변경 후 (v[N])

[핵심만 간결하게]

## 기대 효과

- [구체적 개선점]

## 리스크 및 완화

| 리스크 | 완화 방안 |
|--------|----------|
| | |

## 롤백 방법

- [원상 복구 경로]

## 검증 방법

- [이 변경이 실제로 기대대로 동작하는지 확인 방법]

## 관련 자료

- 이전 버전 스냅샷: [snapshots/v[N-1].md](../snapshots/v[N-1].md)
- 새 버전 스냅샷: [snapshots/v[N].md](../snapshots/v[N].md)
```

### 파일 4: `05-flow-history/changes/0001-YYYY-MM-DD-initial-harness.md`

Generator가 이 프로젝트 생성 직후 자동 기록.

```markdown
# [0001] 초기 하네스 빌드 (v1)

## 메타
- **번호**: 0001
- **일시**: [생성 일자]
- **변경자**: harness-designer 스킬
- **영향 범위**: major (초기 구축)
- **이전 버전**: N/A
- **새 버전**: v1

## 동기 (Why)

[프로젝트명] 하네스 초기 구축.
사용자 요구사항 요약: [Planner Discovery Stage 1~4 핵심]

## 변경 내용 (What)

### 생성된 구조

- `CLAUDE.md` — 워크스페이스 진입점 + 참조 라우팅
- `AGENTS.md` — 에이전트 페르소나 상세
- `WORKSPACE_TREE.md` — 폴더 구조
- `00-system/prompts/` — [에이전트 수]개 역할 파일
- `00-system/protocols/` — council, independence, analysis, data-pipeline, maintenance, flow-change 프로토콜
- `00-system/templates/` — [템플릿 수]개 아웃풋 구조
- `.claude/commands/` — [커맨드 수]개 슬래시 커맨드
- `05-flow-history/` — 이 위키 자체

## 설계 근거 (참고 보관)

Planner 답변 요지:
- **목적**: [Stage 1 W1]
- **사용자**: [Stage 1 W2]
- **성공 기준**: [Stage 1 W3]
- **가장 중요한 품질 속성**: [Stage 4 E1 상위 3개]
- **절대 타협 금지**: [Stage 4 E3]

평가 가중치:
- Progressive Disclosure: [%]
- Mechanical Enforcement: [%]
- Feedback Loop: [%]
- Session Continuity: [%]
- Entropy Management: [%]
- (Pattern Fidelity 사용 시) [%]

## 관련 자료

- 스냅샷: [snapshots/v1.md](../snapshots/v1.md)
- 플로우 변경 프로토콜: [flow-change-protocol.md](../../00-system/protocols/flow-change-protocol.md)
```

### 파일 5: `05-flow-history/snapshots/v1.md`

```markdown
# Snapshot — v1 (Initial Build)

- **도입일**: [생성 일자]
- **상태**: **Active**

## 핵심 특징

[Planner 설계안 요약 — 에이전트 수, 핵심 프로토콜, 주요 커맨드]

## 실물 위치

- 프롬프트: [00-system/prompts/](../../00-system/prompts/)
- 프로토콜: [00-system/protocols/](../../00-system/protocols/)
- 템플릿: [00-system/templates/](../../00-system/templates/)
- 커맨드: [.claude/commands/](../../.claude/commands/)

## 이 스냅샷으로 돌아가기

현재가 v1이므로 기본 상태 그대로 사용.
```

### 파일 6: `00-system/protocols/flow-change-protocol.md`

```markdown
# Flow Change Protocol — 플로우 변경 추적 프로토콜

## 목적

워크플로우 관련 파일이 변경될 때 **변경의 이유·범위·이전 상태·복구 경로**를 기록하여 다음 용도로 활용한다:

- **프로젝트 개선 이력 추적** — 플로우가 어떻게 진화했는지 회고
- **향후 유사 프로젝트 설계 참고** — 다른 워크스페이스를 만들 때 설계 근거 재활용
- **롤백 추적** — 이전 버전으로 되돌릴 때 근거 확보
- **A/B 비교 테스트 기반** — legacy 버전 병존으로 품질 비교 가능

> ※ 이 이력은 **회고·롤백·참고용**이다. 새 세션마다 읽을 필요 없다. 플로우 수정·롤백·이식할 때만 참조한다.

## 기록 트리거

**"주요 운영 시스템의 변화"만** 기록한다.

### 기록 대상 (운영 변경)

| 범주 | 기록 필요 예 |
|------|------------|
| 에이전트 행동 로직 변경 | 프롬프트에 새 규칙/축/금지 사항 추가·삭제 (`00-system/prompts/*.md`) |
| 프로토콜 규칙 변경 | 독립성/토론/분석 규칙 추가/삭제/수정 (`00-system/protocols/*.md`) |
| 템플릿 구조 변경 | 템플릿에 새 필드 추가·삭제 (`00-system/templates/*.md`) |
| API·도구 스크립트 변경 | 신규 연결, 재작성, 엔드포인트 교체 (`00-system/scripts/*.py`, 해당 시) |
| 커맨드 흐름 변경 | 절차 추가, 순서 변경, 트리거 변경 (`.claude/commands/*.md`) |
| 전역 라우팅 변경 | 참조 경로·커맨드 추가, 핵심 원칙 변경 (`CLAUDE.md`) |

### 기록 불필요 (운영 무관)

- 문구 정정·오타·포맷팅
- 주석·설명 추가 (규칙은 동일)
- 스크립트 내부 로깅·에러 메시지 개선
- 상위 문서류(README, WORKSPACE_TREE, AGENTS) 수정 — 참조 문서
- 05-flow-history/ 자체의 메타 문구 정정

### 추적 대상 아님 (카테고리 자체 제외)

- 운영 산출물 (`30-analysis/`, `50-reports/` 등)
- 어젠다·입력물 (`10-agendas/`, `_workspace/` 등)
- 레거시 보존 (`00-system/legacy/`, `.claude/commands/legacy/`)
- 파생 산출물 (`60-exports/`, 자동 생성물)

## 필수 절차 (기록 대상일 때)

### 1. 사전 판단
- **해당 없음** (문구·포맷): 기록 없이 수정
- **해당 — major** (규칙·흐름 변경): 변경 레코드 + CHANGELOG 엔트리
- **해당 — breaking** (하위 호환 깨짐): 변경 레코드 + 이전 버전 legacy 보존 + snapshot 문서 + CHANGELOG 엔트리

### 2. 변경 레코드 작성
`05-flow-history/changes/NNNN-YYYY-MM-DD-slug.md` 신규 파일.
- NNNN = 기존 최고 번호 + 1 (4자리 0 패딩)
- 템플릿: `changes/TEMPLATE.md`

### 3. CHANGELOG.md 업데이트
최상단에 한 줄 추가.

### 4. Breaking 변경 시 레거시 보존
- 이전 상태를 `00-system/legacy/v[N-1]-system/`에 복사
- 관련 커맨드 `.claude/commands/legacy/` 이동
- `snapshots/v[N-1].md` / `v[N].md` 문서 작성

### 5. 버전 인덱스 업데이트
CHANGELOG.md 하단 "버전 인덱스" 표에 새 버전 행.

## 위반 시 대응

| 위반 | 대응 |
|------|------|
| 운영 변경인데 레코드 없음 | 변경 롤백 또는 즉시 레코드 생성 |
| Breaking 변경인데 legacy 없음 | 세션 중단, 컨텍스트로 즉시 복원 |

## 예외

- **컨텍스트 손실로 이전 버전 복구 불가**: 사용자 보고 → 승인 후 재구성 또는 포기
- **긴급 핫픽스**: CHANGELOG 한 줄만 먼저, 상세는 24시간 내 작성

## 이 프로토콜 자체의 변경

규칙 자체 변경(트리거 기준, 절차 단계) → 기록 필수
문구 정정·명확화 → 기록 불필요

---

- **정본 위키 진입점**: [05-flow-history/README.md](../../05-flow-history/README.md)
```

## Generator 체크리스트 (이 템플릿 적용 시)

1. [ ] `05-flow-history/README.md` 생성 ([프로젝트명] 치환)
2. [ ] `05-flow-history/CHANGELOG.md` 생성 (현재 연도, 현재 일자)
3. [ ] `05-flow-history/changes/TEMPLATE.md` 생성
4. [ ] `05-flow-history/changes/0001-[YYYY-MM-DD]-initial-harness.md` 생성 (Planner 답변 요약 삽입)
5. [ ] `05-flow-history/snapshots/v1.md` 생성
6. [ ] `00-system/protocols/flow-change-protocol.md` 생성 (코딩 하네스면 "API·도구 스크립트" 행 유지, 워크스페이스면 선택 제거 가능)
7. [ ] `CLAUDE.md` 참조 라우팅 테이블에 다음 행 추가:
   ```
   | 플로우 변경 추적 규칙 | -> 00-system/protocols/flow-change-protocol.md |
   | 플로우 변경 이력 위키 | -> 05-flow-history/README.md |
   ```
8. [ ] `CLAUDE.md` 하단에 "플로우 변경 추적 (선별 기록)" 섹션 추가:
   ```markdown
   ## 플로우 변경 추적 (선별 기록)

   "주요 운영 시스템의 변화"가 있을 때만 기록한다.
   **기록 대상**: 에이전트 행동·프로토콜 규칙·템플릿 필드·커맨드 흐름·전역 라우팅 변경.
   **기록 불필요**: 문구 정정, 포맷팅, 로깅 개선, 상위 문서 수정.

   기록 절차 → [00-system/protocols/flow-change-protocol.md](00-system/protocols/flow-change-protocol.md)
   ```

## Evaluator 추가 체크 (opt-in 선택 시)

- [ ] `05-flow-history/README.md` 존재
- [ ] `05-flow-history/CHANGELOG.md` 존재 (최소 1줄 엔트리 포함)
- [ ] `05-flow-history/changes/TEMPLATE.md` 존재
- [ ] `05-flow-history/changes/0001-*-initial-harness.md` 존재
- [ ] `05-flow-history/snapshots/v1.md` 존재
- [ ] `00-system/protocols/flow-change-protocol.md` 존재 + "기록 트리거" 섹션 포함
- [ ] `CLAUDE.md`에 플로우 변경 추적 섹션 + 라우팅 엔트리 존재

## 미선택 시

생성하지 않는다. 단 `CLAUDE.md`에 아래 한 줄 주석으로 재활성화 안내:

```markdown
<!-- 플로우 변경 이력 추적을 추가하려면 harness-designer-workspace 스킬을 재호출하고
     flow-history-template 참조 파일을 복사 생성하도록 요청하세요. -->
```
