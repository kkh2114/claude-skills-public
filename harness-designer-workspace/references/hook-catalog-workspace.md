# Hook & Environment Catalog — Workspace v1

> LLM이 Phase 3-8에서 이 파일을 읽고 워크스페이스 도메인에 맞는 항목을 선택한다.
> 코딩 카탈로그와 다르게, **산출물 검증과 외부 API 연동**에 초점을 둔다.

---

## 사용 방법 (LLM 지침)

1. Discovery 답변(도메인·인풋 형태·외부 연동·산출물 유형)을 추출한다
2. 아래 매핑 테이블과 대조하여 해당 워크스페이스에 필요한 항목만 제안한다
3. 코딩 도메인 항목(Git Hook, pre-commit 프레임워크, 린터)은 **제안하지 않는다**
4. 워크스페이스 규모·외부 연동 여부에 따라 항목 취사선택:
   - 단발 분석·텍스트만 사용 → C1만 권고 (산출물 검증 훅)
   - LLM API 사용 → B (.env.example) 추가 권고
   - 데이터 파이프라인·스크래핑 → A (가상환경) + B + C 모두 권고
5. 이 카탈로그에 없는 도메인은 동일 범주의 표준 도구를 추론하여 제안한다

---

## A. 가상환경 (Virtual Environment)

> 워크스페이스에서는 데이터 가공·스크래핑·자동화 스크립트가 있을 때만 권고한다.
> Discovery Stage 2의 S5(인풋 형태) 또는 도메인 특성에서 명시적으로 식별될 때.

| 조건 | 권고 도구 | 생성 파일 | 판단 기준 |
|------|---------|---------|---------|
| Python 데이터 가공 (PDF 파싱·웹 스크래핑·텍스트 정제) | venv | `.python-version`, `requirements.txt` | 외부 패키지 3개 이하면 venv로 충분 |
| 복잡한 데이터 파이프라인 (LangChain·LlamaIndex·pandas 다수) | poetry | `pyproject.toml` | 의존성이 복잡해지면 poetry 권고 |
| 텍스트 분석만 (별도 스크립트 없음) | — | (불필요) | **이 경우 가상환경 제안 자체를 스킵** |
| Node.js 자동화 스크립트 | .nvmrc | `.nvmrc` | 드물지만 puppeteer 등 사용 시 |

**워크스페이스 가상환경의 특징:**
- 코딩 프로젝트와 달리, **워크스페이스 자체는 코드가 아니다**
- 가상환경은 워크스페이스 안에 있는 **보조 스크립트 실행 환경**용
- 따라서 일반적으로 가상환경 제안 빈도는 낮다

---

## B. 환경변수 (.env.example) — 외부 API 연동

> 워크스페이스에서 가장 흔히 필요한 항목.
> LLM API, 리서치 데이터 API, 시장 데이터 API 등 거의 모든 도메인에서 등장.

### .env.example 구성 원칙

```bash
# ================================
# [워크스페이스명] 환경변수 스키마
# 실제 값은 .env에 입력하세요 (.env는 .gitignore에 포함됨)
# ================================

# --- LLM API ---
ANTHROPIC_API_KEY=           # Claude API (https://console.anthropic.com)
OPENAI_API_KEY=              # GPT API (https://platform.openai.com)
GOOGLE_API_KEY=              # Gemini API (https://aistudio.google.com)

# --- 도메인별 API ---
# (도메인에 맞게 LLM이 선택하여 추가)
```

### 도메인별 API 키 권고

| 워크스페이스 도메인 | 추가 환경변수 후보 |
|----------------|----------------|
| 투자·금융 분석 | `ALPHA_VANTAGE_KEY`, `POLYGON_API_KEY`, `FRED_API_KEY` |
| 리서치·학술 | `SEMANTIC_SCHOLAR_KEY`, `PUBMED_API_KEY`, `ARXIV_USER_AGENT` |
| 콘텐츠 기획 | `YOUTUBE_DATA_API_KEY`, `REDDIT_CLIENT_ID`, `REDDIT_SECRET` |
| 법률 검토 | `LAWNB_API_KEY` 등 (한국 법률 API) |
| 시장 조사 | `SERPAPI_KEY`, `BRAVE_SEARCH_KEY`, `TAVILY_API_KEY` |
| 마케팅 분석 | `GA4_PROPERTY_ID`, `META_ACCESS_TOKEN` |
| 인사·HR | `LINKEDIN_API_KEY`, `WORKDAY_TOKEN` |
| 공공조달 (한국) | `NARA_OPENAPI_KEY`, `G2B_API_KEY` |
| 일반 데이터 수집 | `NEWS_API_KEY`, `WEATHER_API_KEY` |

**.gitignore 추가 규칙 (필수):**
```
.env
.env.local
.env.*.local
*.pem
30-analysis/sessions/*-secret.md   # 비밀 정보 포함 세션 (해당 시)
```

---

## C. 훅 (Hook) — Claude Code Hook 중심

> 워크스페이스 훅의 주 용도는 **산출물 형식 강제**이다.
> Git Hook·pre-commit 프레임워크는 **사용하지 않는다** (코드 커밋 워크플로우 아님).

### C-1. PostToolUse — 산출물 형식 검증

> 에이전트가 파일 생성·수정 도구를 사용한 직후 검증 명령 실행.

**권고 사용 시나리오:**

| 상황 | 검증 명령 | 효과 |
|------|---------|------|
| 70-playbook/ 파일 생성 시 | CARL 4필드(Context/Action/Result/Learning) 존재 확인 | 형식 미준수 즉시 발견 |
| 50-reports/ 파일 생성 시 | source 필드 존재 확인 | 출처 누락 차단 |
| 30-analysis/sessions/ 파일 생성 시 | bias_check 필드 존재 확인 | 독립성 원칙 준수 |
| 45-wiki/ 파일 생성 시 | YAML frontmatter 존재 확인 | 그래프 빌드 가능성 보장 |

**생성 예시 (CARL 형식 검증):**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "for f in $(find 70-playbook -name '*.md' -newer .last-check 2>/dev/null); do grep -q '^## Context' \"$f\" && grep -q '^## Action' \"$f\" && grep -q '^## Result' \"$f\" && grep -q '^## Learning' \"$f\" || echo \"⚠️ CARL 형식 누락: $f\"; done; touch .last-check",
            "description": "playbook CARL 형식 자동 검증"
          }
        ]
      }
    ]
  }
}
```

### C-2. Stop — 세션 종료 시 상태 저장 검증

> Claude 응답 종료 시 progress.json 업데이트 누락을 경고.

**권고 사용 시나리오:**
- 장기 프로젝트(progress.json 사용)에서만 권고
- 단발 분석에서는 불필요

**생성 예시:**
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "if [ -f progress.json ]; then LAST_MOD=$(stat -f %m progress.json 2>/dev/null || stat -c %Y progress.json 2>/dev/null); NOW=$(date +%s); if [ $((NOW - LAST_MOD)) -gt 3600 ]; then echo '⚠️ progress.json이 1시간 이상 업데이트되지 않았습니다'; fi; fi",
            "description": "progress.json 업데이트 누락 경고"
          }
        ]
      }
    ]
  }
}
```

### C-3. PreToolUse — 위험 작업 차단 (선택)

> 50-reports/, 70-playbook/의 기존 파일 덮어쓰기를 사전 차단.

**권고 사용 시나리오:**
- 보고서·playbook 누적이 중요한 워크스페이스
- 실수로 덮어쓰기 발생 가능성을 줄이고 싶을 때

**일반적으로 워크스페이스에서는 C-1과 C-2로 충분하다. C-3은 선택 사항.**

---

## D. LLM 판단 가이드

Phase 3-8에서 이 카탈로그를 읽은 후 아래 기준으로 제안 범위를 결정한다.

| 워크스페이스 유형 | 권고 범위 |
|----------------|---------|
| 텍스트 기반 단발 분석 (외부 API 없음) | C1만 권고 (산출물 형식 검증) |
| LLM API 사용 (단순 호출) | B(.env) + C1 |
| LLM API + 외부 데이터 API | B(.env) + C1 + C2 |
| 데이터 가공 스크립트 포함 | A(가상환경) + B + C1 + C2 |
| 장기 누적형 워크스페이스 (40-knowledge-index, 70-playbook 활성) | B + C1 + C2 + C3 |

**판단 불확실 시 행동:**
- API 키가 필요한지 모호하면 사용자에게 직접 질문 ("이 워크스페이스가 LLM 또는 외부 API를 호출하나요?")
- 가상환경 항목은 **데이터 가공 스크립트가 명시적으로 없으면** 제안 자체를 스킵
- 코딩 카탈로그 항목(Git Hook 등)을 끌어오지 않는다

---

## E. 워크스페이스 vs 코딩 카탈로그 차이 요약

| 항목 | 워크스페이스 (이 파일) | 코딩 (hook-catalog.md) |
|------|------------------|--------------------|
| 가상환경 권고 빈도 | 낮음 (스크립트 있을 때만) | 높음 (대부분 필요) |
| Git Hook | 제안하지 않음 | 팀 협업 시 권고 |
| pre-commit 프레임워크 | 제안하지 않음 | 팀 협업 시 권고 |
| 훅 주 용도 | 산출물 형식 강제 (CARL, source) | 코드 품질 강제 (린터, 테스트) |
| .env 주 키 종류 | 외부 API 키 (LLM·데이터) | 서비스 설정 (DB, JWT, PORT) |
