# Hook & Environment Catalog v1

> LLM이 Phase 3-6에서 이 파일을 읽고 프로젝트 tech stack에 맞는 항목을 선택한다.
> 버전 고정 목록이 아닌 **원칙 기반 카탈로그**다. 구체적 명령어는 LLM이 실행 시점 판단.

---

## 사용 방법 (LLM 지침)

1. Discovery에서 수집한 tech stack과 아래 매핑 테이블을 대조한다
2. 해당 스택의 권고 항목을 제안 목록에 포함한다
3. "모든 프로젝트 공통" 항목은 항상 포함 대상으로 검토한다
4. 프로젝트 규모·협업 여부에 따라 항목 취사선택 판단:
   - 개인 프로젝트·PoC → 훅 최소화 (C1만 권고)
   - 팀 협업·장기 운영 → 전체 권고
5. 이 카탈로그에 없는 스택은 동일 범주의 표준 도구를 추론하여 제안한다

---

## A. 가상환경 (Virtual Environment)

| 스택 | 권고 도구 | 생성 파일 | 판단 기준 |
|------|---------|---------|---------|
| Python | venv (단순) / poetry (의존성 복잡) | `.python-version`, `requirements.txt` 또는 `pyproject.toml` | 외부 패키지 3개 이상이면 poetry 권고 |
| Node.js | .nvmrc | `.nvmrc` | Node 버전 고정이 필요한 모든 프로젝트 |
| Ruby | rbenv | `.ruby-version` | Gemfile 존재 시 |
| Go | go.mod | (이미 포함) | go.mod가 있으면 가상환경 불필요, 스킵 |
| 복합 (Python + Node) | venv + .nvmrc 병행 | 두 파일 모두 | Makefile로 통합 setup 명령 추가 권고 |

**생성 시 포함 내용:**
- 언어 버전 명시 (`.python-version`: `3.11.0`)
- 패키지 목록 초기 파일 (비어 있어도 존재해야 함)
- `README.md`에 가상환경 활성화 명령 추가

---

## B. 환경변수 (.env.example)

**모든 프로젝트 공통 — 외부 서비스 연동이 하나라도 있으면 항상 권고**

### .env.example 구성 원칙

```bash
# ================================
# [프로젝트명] 환경변수 스키마
# 실제 값은 .env에 입력하세요 (.env는 .gitignore에 포함됨)
# ================================

# --- 서버 설정 ---
PORT=8000                    # 서버 포트 (기본값 제공 가능)
ENV=development              # development | staging | production

# --- 데이터베이스 ---
DATABASE_URL=                # 예: postgresql://user:pass@localhost:5432/dbname

# --- 외부 API ---
API_KEY=                     # [서비스명] API 키 (https://... 에서 발급)

# --- 인증 ---
SECRET_KEY=                  # JWT 서명 키 (랜덤 32자 이상 권장)
```

### 스택별 추가 키 제안

| 스택/프레임워크 | 추가 환경변수 예시 |
|-------------|----------------|
| FastAPI | `DATABASE_URL`, `REDIS_URL`, `CORS_ORIGINS` |
| Django | `SECRET_KEY`, `DATABASE_URL`, `ALLOWED_HOSTS`, `DEBUG` |
| Next.js | `NEXT_PUBLIC_API_URL`, `NEXTAUTH_SECRET` |
| Express | `PORT`, `JWT_SECRET`, `MONGODB_URI` |
| React (Vite) | `VITE_API_BASE_URL` (VITE_ 접두사 필수) |
| 공통 LLM 연동 | `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` |

**.gitignore 추가 규칙 (필수):**
```
.env
.env.local
.env.*.local
*.pem
```

---

## C. 훅 (Hook)

### C-1. Claude Code Hook (`.claude/settings.json`)

> 에이전트가 도구를 호출할 때 자동 실행되는 훅.
> **가장 추천** — Claude Code 사용 프로젝트에서 가장 효과적.

**훅 종류와 용도:**

| Hook 이벤트 | 실행 시점 | 권장 용도 |
|-----------|---------|---------|
| `PreToolUse` | 도구 호출 직전 | 위험 명령 차단, 파일 수정 전 백업 |
| `PostToolUse` | 도구 호출 직후 | 린터 자동 실행, 포맷 자동 적용 |
| `Stop` | Claude 응답 종료 시 | 세션 기록 저장, 상태 업데이트 확인 |

**스택별 PostToolUse 권고:**

| 스택 | 권고 명령 | 효과 |
|------|---------|------|
| Python | `ruff check . --fix && ruff format .` | 린트 + 포맷 자동 |
| Node.js / TS | `npx eslint . --fix && npx prettier --write .` | 린트 + 포맷 자동 |
| Go | `gofmt -w . && go vet ./...` | 포맷 + 정적 분석 |
| 공통 | `echo '[HOOK] 코드 변경 감지됨'` | 최소 로깅 (다른 훅 없을 때) |

**생성 예시 (Python):**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "ruff check . --fix && ruff format .",
            "description": "파일 수정 후 자동 린트·포맷"
          }
        ]
      }
    ]
  }
}
```

---

### C-2. Git Hook (`.git/hooks/`)

> `git commit` / `git push` 시 자동 실행.
> 팀 협업 프로젝트에 권고. 개인 PoC는 선택적.

**권고 훅 종류:**

| 훅 이름 | 실행 시점 | 권장 내용 |
|--------|---------|---------|
| `pre-commit` | 커밋 직전 | 테스트·린터 실행, 실패 시 커밋 차단 |
| `commit-msg` | 커밋 메시지 작성 후 | 커밋 메시지 형식 검증 (Conventional Commits) |
| `pre-push` | 푸시 직전 | 전체 테스트 스위트 실행 |

**스택별 pre-commit 내용:**

| 스택 | 권고 스크립트 |
|------|------------|
| Python | `python -m pytest tests/ -q && ruff check .` |
| Node.js | `npm run test -- --passWithNoTests && npm run lint` |
| Go | `go test ./... && go vet ./...` |
| 공통 | 커밋 메시지 형식 검사 (`feat:`, `fix:`, `docs:` 등) |

**생성 시 주의:**
- 스크립트 첫 줄 반드시 `#!/bin/sh`
- 실행 권한 부여 명령 포함: `chmod +x .git/hooks/pre-commit`
- 너무 오래 걸리면 개발자가 훅을 무력화함 → **30초 이내**로 설계

---

### C-3. pre-commit 프레임워크 (`.pre-commit-config.yaml`)

> `pip install pre-commit` + `pre-commit install`로 팀 전체에 일관 적용.
> Git Hook보다 관리가 쉬움. **팀 프로젝트에 강력 권고.**

**공통 권고 훅 (스택 무관):**

```yaml
repos:
  # 비밀 키 커밋 방지 (모든 프로젝트 권고)
  - repo: https://github.com/Yelp/detect-secrets
    hooks:
      - id: detect-secrets

  # 대용량 파일 커밋 방지
  - repo: https://github.com/pre-commit/pre-commit-hooks
    hooks:
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: end-of-file-fixer
      - id: trailing-whitespace
```

**스택별 추가 권고:**

| 스택 | 추가 repo / hook |
|------|---------------|
| Python | `black`, `ruff`, `mypy` (타입 검사) |
| Node.js / TS | `eslint`, `prettier` |
| 마크다운 포함 | `markdownlint` |
| YAML 파일 포함 | `check-yaml` |

---

## D. LLM 판단 가이드

Phase 3-6에서 이 카탈로그를 읽은 후 아래 기준으로 제안 범위를 결정한다.

| 조건 | 권고 범위 |
|------|---------|
| 개인 PoC, 단기 실험 | A(가상환경) + B(env) + C1(Claude Code Hook)만 |
| 개인 장기 프로젝트 | A + B + C1 + C2(Git Hook) |
| 팀 협업 프로젝트 | A + B + C1 + C2 + C3(pre-commit) 전체 |
| Claude Code 미사용 | C1 제외, C2 + C3 중심 |
| Go 프로젝트 | A 가상환경 불필요(스킵), B + C 진행 |

**판단 불확실 시 행동:**
- 확실하지 않은 항목은 제안하되 "(선택 사항)" 표시
- 상충하는 항목이 있으면 이유와 함께 둘 다 제시하고 사용자 선택 유도
- 이 카탈로그에 없는 스택은 동일 범주 표준 도구를 추론하여 "(추론)" 표시
