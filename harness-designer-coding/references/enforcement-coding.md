# 코딩 강제 규칙 패턴 참조 v1

> "불변량(invariants)을 강제하라, 구현을 마이크로매니지하지 말라." — OpenAI
> "한 번 인코딩하면, 모든 코드 라인에 적용된다."

## 3종 강제 수단

### 1. 구조 테스트 (Structural Tests)

아키텍처 규칙을 코드로 검증. CI에서 실행.

**레이어 의존성 검증 예시 (bash):**
```bash
#!/bin/bash
# scripts/lint-layers.sh
# UI 레이어가 Repo 레이어를 직접 import 하면 실패

VIOLATIONS=$(grep -rn "from.*repo" src/runtime/ui/ 2>/dev/null || true)
if [ -n "$VIOLATIONS" ]; then
  echo "❌ Layer violation: UI layer imports from Repo layer"
  echo "$VIOLATIONS"
  echo ""
  echo "FIX: Move this logic to a Service layer function."
  echo "     UI → Service → Repo (정방향만 허용)"
  echo "     See docs/architecture.md#layer-rules"
  exit 1
fi
echo "✅ Layer dependencies OK"
```

**모듈 경계 검증 예시:**
```bash
#!/bin/bash
# 도메인 간 직접 import 검사
for domain in src/domains/*/; do
  DOMAIN_NAME=$(basename "$domain")
  CROSS_IMPORTS=$(grep -rn "from.*domains/" "$domain" | grep -v "$DOMAIN_NAME" || true)
  if [ -n "$CROSS_IMPORTS" ]; then
    echo "❌ Cross-domain import in $DOMAIN_NAME:"
    echo "$CROSS_IMPORTS"
    echo "FIX: Use shared/ or providers/ for cross-domain communication."
    exit 1
  fi
done
echo "✅ Module boundaries OK"
```

### 2. 린터 규칙 (Custom Linters)

코딩 컨벤션을 기계적으로 강제. ESLint, Ruff, 커스텀 스크립트.

**핵심 규칙 예시:**
- 중복 유틸리티 감지: shared/에 이미 있는 기능 재구현 시 경고
- 경계 검증 누락: 외부 입력 처리 시 검증 코드 없으면 경고
- 금지 패턴: 직접 DB 쿼리 in UI, 하드코딩된 설정값

**에러 메시지 원칙:**
모든 에러는 에이전트가 **즉시 수정할 수 있도록** 작성:

```
❌ 나쁜: "Import violation"
✅ 좋은: "Import violation in src/runtime/ui/Dashboard.tsx:15
   'import { getUserById } from ../../domains/auth/repo'
   UI layer cannot import from Repo layer.
   → Create a Service function: src/domains/auth/service.ts
   → Import from Service: import { getUserById } from ../../domains/auth/service
   → Reference: docs/architecture.md#layer-rules"
```

### 3. CI 게이트 (Pipeline Gates)

PR이 머지되기 위해 통과해야 하는 검증 단계:

```yaml
# .github/workflows/ci.yml 골격
name: CI
on: [pull_request]
jobs:
  gate-1-lint:
    steps:
      - run: npm run lint          # 코드 스타일
      - run: npm run typecheck     # 타입 검사
      - run: bash scripts/lint-layers.sh  # 레이어 규칙
      - run: bash scripts/check-structure.sh  # 구조 검증

  gate-2-unit-test:
    needs: gate-1-lint
    steps:
      - run: npm test -- --coverage
      - run: bash scripts/check-coverage.sh  # 커버리지 기준

  gate-3-integration:
    needs: gate-2-unit-test
    steps:
      - run: npm run test:integration
      - run: npm run test:e2e  # (해당 시)
```

## "취향 불변량" (Taste Invariants)

정량적 규칙 외에, 코드 품질에 대한 "취향"도 인코딩 가능:

```markdown
# docs/conventions.md 에 포함

## 취향 규칙
- 공유 유틸 패키지를 선호, 도메인별 헬퍼 남발 금지
- 데이터 검증은 스키마 기반 (Zod, pydantic), 수동 if 문 금지
- 에러 메시지는 사용자 친화적 (내부 스택트레이스 노출 금지)
```

이런 규칙은 린터로 완벽히 강제하기 어렵지만,
코드 리뷰 루프에서 리뷰 에이전트가 체크한다.

---

## 금지 규칙 작성 원칙 — 반드시 대안 2개 세트

> "금지만 두면 AI가 오작동한다. 반드시 대안을 붙여야 한다." — Claude Design 시스템 프롬프트 분석

Generator가 docs/conventions.md, 린터 규칙, 에이전트 프롬프트에 금지 규칙을 작성할 때
**반드시 대안 2개를 함께 명시**한다. 대안 없는 금지는 작성 금지.

### 올바른 형식

```markdown
[금지] {금지 행동}
[대안1] {허용되는 첫 번째 방법}
[대안2] {허용되는 두 번째 방법}
```

### 코딩 도메인 예시

```markdown
❌ 잘못된 작성:
"UI 레이어에서 직접 DB 쿼리 금지"

✅ 올바른 작성:
[금지] UI 레이어에서 직접 DB 쿼리
[대안1] Service 레이어 함수 호출 (UI → Service → Repo)
[대안2] React Query / SWR 훅으로 fetch (Service 호출을 캡슐화)

❌ 잘못된 작성:
"any 타입 사용 금지"

✅ 올바른 작성:
[금지] any 타입 직접 사용
[대안1] unknown으로 받고 type guard로 좁히기
[대안2] 제네릭 <T>로 타입 매개변수화

❌ 잘못된 작성:
"하드코딩된 설정값 금지"

✅ 올바른 작성:
[금지] URL·키·임계값 등을 코드에 하드코딩
[대안1] 환경변수 (process.env / os.environ)로 주입
[대안2] config/ 모듈 통해 중앙 관리
```

### 린터 에러 메시지에도 적용

```
❌ "Forbidden: any type used"
✅ "any 타입 사용 금지 (src/api/handler.ts:42)
    [대안1] unknown으로 받고 type guard 적용
    [대안2] 제네릭 <T>로 매개변수화
    참조: docs/conventions.md#type-rules"
```

### Evaluator 검증 포인트

Evaluator는 docs/conventions.md, 린터 규칙 파일, 에이전트 프롬프트에서
대안 없는 금지 규칙이 있으면 **Mechanical Enforcement 기둥에서 PARTIAL 처리**한다.

---

## Generator가 해야 하는 것

1. docs/architecture.md에 레이어 규칙 정의
2. scripts/에 구조 테스트 스크립트 생성
3. 린터 설정 파일 생성 (.eslintrc / pyproject.toml 등)
4. CI 파이프라인 설정 생성
5. 모든 에러 메시지에 **수정 방법 + 참조 문서 경로** 포함
6. **모든 금지 규칙에 대안 2개 세트** 적용 확인
