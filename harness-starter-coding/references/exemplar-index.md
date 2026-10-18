# harness-100 Exemplar Index (Coding Domain)

출처: https://github.com/revfactory/harness-100 (Apache-2.0)
본 인덱스는 **코딩·개발·데이터/AI** 성격의 하네스만 추립니다.
문서·분석·기획은 `harness-starter-workspace` 를 사용하세요.

## 2개 카테고리 (27개 exemplar)

| # | 카테고리 | 범위 | 대표 키워드 |
|---|---------|-----|-----------|
| 2 | Software Dev & DevOps | 16–30 | 풀스택, API, CI/CD, 보안감사, IaC |
| 3 | Data & AI/ML | 31–42 | ML실험, 데이터분석, LLM앱, 디자인시스템 |

## 전체 exemplar 목록

### Dev & DevOps (16–30)

| 번호 | exemplar 이름 | 설명 |
|-----|-------------|------|
| 16 | **fullstack-webapp** ⭐ | architect/frontend/backend/qa/devops 5인 표준 파이프라인 |
| 17 | **mobile-app-builder** | React Native/Flutter 모바일 앱 |
| 18 | **api-designer** | REST/GraphQL 설계 + OWASP |
| 19 | **database-architect** | 스키마·인덱스·마이그레이션 |
| 20 | **cicd-pipeline** | CI/CD, GitHub Actions, 자동화 |
| 21 | **code-reviewer** | 코드 리뷰·정적 분석·품질 게이트 |
| 22 | **legacy-modernizer** | 레거시 시스템 현대화·리팩터링 |
| 23 | **microservice-designer** | 마이크로서비스 아키텍처·DDD |
| 24 | **test-automation** | Test Pyramid, E2E, 자동화 |
| 25 | **incident-postmortem** | 인시던트 대응·사후분석·DORA |
| 26 | **infra-as-code** | Terraform, IaC, 클라우드 인프라 |
| 27 | **data-pipeline** | ETL, Star/Snowflake Schema |
| 28 | **security-audit** | OWASP Top 10, CWE, 침투테스트 |
| 29 | **performance-optimizer** | 프로파일링·병목 제거·최적화 |
| 30 | **open-source-launcher** | 오픈소스 프로젝트 론칭·문서화 |

### Data & AI/ML (31–42)

| 번호 | exemplar 이름 | 설명 |
|-----|-------------|------|
| 31 | **ml-experiment** | 실험설계·피처엔지니어링·SHAP/LIME |
| 32 | **data-analysis** | 탐색적 데이터 분석·시각화·인사이트 |
| 33 | **text-processor** | NLP 파이프라인·분류·감성분석·추출 |
| 34 | **data-migration** | 데이터 이전·변환·검증 |
| 35 | **api-client-generator** | API 클라이언트 자동 생성·SDK |
| 36 | **design-system** | shadcn/ui 기반 디자인 시스템 |
| 37 | **web-scraper** | 웹 크롤링·스크래핑·파싱 |
| 38 | **chatbot-builder** | 챗봇 설계·구현·테스트 |
| 39 | **changelog-generator** | 변경 이력 자동 생성·릴리즈 노트 |
| 40 | **cli-tool-builder** | CLI 도구 개발·배포 |
| 41 | **llm-app-builder** ⭐ | 프롬프트→RAG→평가→최적화→배포 풀 파이프라인 |
| 42 | **bi-dashboard** | BI 대시보드·지표 설계·시각화 |

## 임베디드 프레임워크 (도메인 주입)

| 도메인 | 프레임워크 |
|-------|----------|
| Development | SOLID, DDD, OWASP Top 10, Test Pyramid, DORA Metrics, CWE Top 25 |
| Data | Star/Snowflake Schema, Great Expectations, SHAP/LIME, Feature Engineering |

## 매칭 규칙 (Planner)

1. 사용자 요청에서 앱 유형·데이터 성격·인프라 요구 추출
2. Dev vs Data 카테고리 판정
3. exemplar 후보 1~3개 제시 → 선택
4. Scale Mode 자동 추천 (MVP=Reduced / 프로덕션=Full / 단일기능=Single)

## exemplar 구조 (복제 단위)

```
{NN}-{harness-name}/.claude/
├── CLAUDE.md
├── agents/
│   ├── architect.md           — 요구·아키텍처·DB·API 설계
│   ├── frontend-dev.md        — React/Next.js
│   ├── backend-dev.md         — API·DB·Auth·비즈니스로직
│   ├── qa-engineer.md         — 테스트·코드리뷰 (Reviewer 역할)
│   └── devops-engineer.md     — CI/CD·인프라·모니터링
└── skills/
    ├── {orchestrator}/skill.md
    ├── component-patterns/skill.md       — frontend 확장
    └── api-security-checklist/skill.md   — backend 확장
```

## Scale Modes (coding 전용 기본값)

| 모드 | 배치 에이전트 | 사용 시점 |
|-----|-------------|---------|
| **Full Pipeline** | architect + frontend + backend + qa + devops | 풀스택 신규 개발 |
| **Backend Mode** | architect + backend + qa | API만 구축 |
| **Frontend Mode** | architect + frontend + qa | 기존 API에 UI 추가 |
| **Refactoring Mode** | architect + 관련 개발자 + qa | 리팩터링 |
| **DevOps Mode** | devops | 배포 설정만 |

## 치환 대상 (Generator)

| 원본 | 치환 |
|-----|-----|
| 16-fullstack-webapp | 사용자 프로젝트명 |
| Next.js/Prisma/SQLite | 사용자 선택 스택 (없으면 기본값 유지) |
| _workspace/NN_*.md | 유지 |
| agents/ 5인 구성 | Scale Mode에 따라 축소 |
| OWASP·SOLID 임베드 | 유지 (도메인 주입) |
