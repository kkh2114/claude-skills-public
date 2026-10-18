# 0. 준비 — 설치기로 이 PC 조건을 맞춘다

원칙: **필요한 것은 설치가 기본.** 이미 있으면 「이미 설치됨 — 건너뜀」을 남기고 다음으로. 설치하지 않고 다른 길로 가는 것(우회)은 **사용자가 고를 때만**(`--skip`).

## 설치기 실행
```bash
bash <스킬>/scripts/install.sh                     # macOS · Linux · WSL
powershell -ExecutionPolicy Bypass -File <스킬>\scripts\install.ps1    # Windows
```
- 시작점은 uv(파이썬·도구 관리자)만 확보한다(공식 설치 스크립트). 파이썬이 없어도 uv가 받아 온다. 나머지는 `setup.py`가 탐색 → 설치.
- `--check` 탐색만 · `--login` NotebookLM 로그인 창까지 · `--agent claude|codex|both`(기본: 있는 것 자동) · `--skip a,b` 사용자가 고른 제외
  (제외 키: browser·login·chrome·aside·docskills·venv·node·npm·pandoc·libreoffice·poppler·self)
- 끝에 **「남은 할 일」**이 있으면 사람 차례다. 하나씩 안내하고(한 번에 하나), 끝나면 설치기를 다시 실행 → 된 것은 건너뛰고 이어서. 「남은 할 일」이 없어질 때까지.
- 기록: `~/.nrb/install-state.json`. 이 스킬 전용 도구는 `~/.nrb/`(venv·node 패키지)에 두어 사용자 환경을 건드리지 않는다. 지우려면 이 폴더와 `uv tool uninstall notebooklm-mcp-cli yt-dlp`.

## 설치기가 다루는 것
| 묶음 | 구성요소 | 설치 방법 | 사람 차례 |
|---|---|---|---|
| 필수 | uv · Python 3.10+ · nlm(notebooklm-mcp-cli) · yt-dlp | uv 공식 설치 → `uv python` · `uv tool install` | — |
| 필수 | 로그인용 브라우저(크롬 외 Edge·Brave·Arc·Firefox 등) | 없으면 Edge(맥 brew cask·Windows winget) / Firefox(apt) | — |
| 필수 | NotebookLM 로그인 | `nlm login --storage protected` | 구글 로그인(본인) |
| 로그인 벽 수집 | Claude in Chrome 확장 (Claude Code) | 크롬 없으면 설치 | 웹스토어에서 확장 추가·로그인, `/chrome` 연결 |
| 로그인 벽 수집 | 어사이드 CLI · 앱 (코덱스·대안) | CLI 공식 설치 스크립트 | 앱 설치·로그인, `aside login` 기기 승인 |
| 출력 | docx·pptx 스킬 (anthropics/skills) | Claude: `claude plugin install document-skills@anthropic-agent-skills` / Codex: `~/.codex/skills`에 복사 | Claude CLI 없으면 `/plugin` 명령 안내 |
| 출력 | 파이썬 문서 라이브러리(lxml·defusedxml·Pillow·python-docx·python-pptx·markitdown) | `~/.nrb/venv` | — |
| 출력 | Node.js 18+ · npm 패키지(docx·pptxgenjs·react·react-dom·react-icons·sharp) | brew·winget / Linux는 NodeSource · `~/.nrb/node` | Linux 관리자 암호 |
| 출력 | pandoc · LibreOffice · poppler | brew·apt·winget | Linux 관리자 암호, 맥은 Homebrew 없으면 설치 안내 |
| 이 스킬 | `~/.claude/skills`·`~/.codex/skills`에 배치 | 복사 | — |

## 작업 셸 환경 (매 세션 처음 한 번)
```bash
eval "$(uv run <스킬>/scripts/nrb.py env)"          # PowerShell: uv run <스킬>\scripts\nrb.py env --ps | iex
```
→ PATH(nlm·venv·node bin) · `NODE_PATH`(docx·pptxgenjs를 require) · `NOTEBOOKLM_HL=ko` · `NRB_PY`(docx·pptx 스킬의 파이썬 스크립트 실행용).

## 요금제·한도 — 사용자에게 설명하고 진행
```bash
uv run <스킬>/scripts/nrb.py tier
```
- `nlm usage`의 Plan으로 감지(예: `NOTEBOOKLM_TIER_PRO_CONSUMER_USER` → pro). 한 줄 설명:
  「노트북 하나에 소스를 무료는 약 50개, 유료(Pro)는 약 300개까지 넣을 수 있어요. 지금은 <감지값>이에요.」
- 무료면 30~40개로 압축해 모으고, 한도가 차면 **뺄 소스 선택 또는 유료 전환**을 묻는다(전환은 사용자 판단).
- Studio 생성·대량 질의 전에 `nlm usage`로 남은 % 확인. 한도 오류 뒤엔 1~2분 쉬고 재시도.
- 계정이 여러 개면 `nlm login profile list` — **NotebookLM에 쓸 계정인지** 한 줄 확인. 세션은 보통 자동 갱신, `expired`일 때만 다시 로그인(네트워크 실패를 만료로 오해하지 않기).

## 로그인 벽 추출기 고르기 (스레드·인스타·링크드인 등)
- Claude Code: **Claude in Chrome**(이 세션에 `mcp__claude-in-chrome__*` 도구가 보이고, 사용자 크롬에 대상 사이트 로그인). 코덱스: **어사이드**.
- 대상 사이트 로그인은 그 브라우저에서 사람이 한 번 — 수집 단계에서 「로그인 필요」가 나오면 안내.
- 쓸 수 없는 상태면 먼저 설치기를 다시 돌려 설치를 마친다. 사용자가 설치를 원하지 않을 때만(사용자 선택) 공개 검색 결과로 찾고 게이트 ②에서 보고.

## 알려진 함정
- `nlm login`은 로그인 브라우저를 **완전히 종료**한 상태여야 한다(맥 Cmd+Q, Windows 작업 표시줄에서 종료). 크롬은 Claude in Chrome용으로 비워 두려고 로그인은 다른 브라우저로 설정한다(설치기가 자동 설정).
- 로그인 보호 저장(protected)은 OS 비밀 저장소(맥 키체인·Windows 자격 증명 관리자·Linux SecretService)를 쓴다. 팝업이 뜨면 「항상 허용」.
- **원 저장소의 `nlm skill install`은 하지 않는다**(이 스킬과 트리거가 겹침). MCP 등록(`nlm setup`)도 불필요 — CLI만 쓴다.
- `aside exec`는 표준입력이 열려 있으면 멈춘다 → 항상 `</dev/null`. 옵션 `--permission`은 1.26부터 없음.
- `nlm` 표 출력은 `[threads]` 같은 대괄호를 먹는다 → 소스 제목에 대괄호를 쓰지 않는다(`nrb.py`가 처리). 기계 처리는 `--json`.
- `nlm chat start`(대화형)는 쓰지 않는다 → `nlm notebook query`. `nlm note create`는 `--content` 필수.
- 산출물 기본 언어가 영어 → `NOTEBOOKLM_HL=ko` (`nrb.py env`·`nrb.py`가 자동).
