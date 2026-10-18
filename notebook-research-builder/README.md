# notebook-research-builder

NotebookLM 노트북 하나를 **유일한 지식 원천**으로 삼아 교안·시장조사·트렌드 리포트·논문 리뷰를 만드는 에이전트 스킬입니다.
목표와 키워드를 주면 기간·주요 사이트 조건에 맞는 자료를 찾아 노트북에 넣고, 노트북 질의 결과로만 문서를 씁니다. 결과물은 워드·파워포인트·웹·NotebookLM Studio(오디오·퀴즈 등)로 냅니다.

- 지원 에이전트: Claude Code, Codex
- 지원 OS: macOS, Windows, Linux(WSL 포함)
- 필요한 계정: Google 계정(NotebookLM). 로그인 벽 사이트(스레드 등)를 수집하려면 Claude in Chrome 또는 Aside 계정

## 설치

스킬 폴더를 받은 뒤, 그 폴더에서 설치기를 실행합니다. 설치기는 PC 상태를 먼저 살펴보고 **없는 것만 설치**합니다. 이미 있는 것은 「이미 설치됨 — 건너뜀」으로 표시합니다.

**macOS · Linux · WSL**
```bash
bash notebook-research-builder/scripts/install.sh
```

**Windows (PowerShell)**
```powershell
powershell -ExecutionPolicy Bypass -File notebook-research-builder\scripts\install.ps1
```

설치기가 끝에 **「남은 할 일」**을 보여 주면, 그건 본인이 직접 해야 하는 단계입니다(아래 표). 끝낸 뒤 설치기를 다시 실행하면 된 것은 건너뛰고 이어서 진행합니다. 「남은 할 일」이 없어지면 설치 완료입니다.

| 직접 해야 하는 단계 | 언제 |
|---|---|
| Google 로그인 (NotebookLM) | 처음 한 번. 설치기를 `--login`으로 다시 실행하면 로그인 창이 뜹니다 |
| Claude in Chrome 확장 설치·로그인 | Claude Code를 쓰는 경우 |
| Aside 앱 설치·로그인, `aside login` 기기 승인 | 로그인 벽 사이트를 Aside로 수집하는 경우 |
| 관리자 암호 입력 | Linux 패키지 설치, macOS에 Homebrew가 없을 때 |

### 설치기 옵션
| 옵션 | 뜻 |
|---|---|
| `--check` | 설치하지 않고 상태만 확인 |
| `--login` | NotebookLM 로그인 창까지 띄움 |
| `--agent claude\|codex\|both` | 대상 에이전트 (기본: PC에 있는 것 자동 감지) |
| `--skip a,b` | 설치하지 않을 구성요소를 직접 고름 (예: `--skip libreoffice,aside`) |

### 설치되는 것
- **필수**: uv, Python 3.10+, `nlm`(notebooklm-mcp-cli), `yt-dlp`, 로그인용 브라우저(크롬 외 하나)
- **로그인 벽 수집**: Claude in Chrome 확장 안내, Aside CLI
- **워드·파워포인트 출력**: anthropics/skills의 docx·pptx 스킬, Node.js 18+와 npm 패키지, Python 문서 라이브러리, pandoc, LibreOffice, poppler
- **스킬 배치**: `~/.claude/skills/`, `~/.codex/skills/`

이 스킬 전용 도구(파이썬 가상환경, npm 패키지)는 `~/.nrb/`에만 설치되어 기존 환경을 바꾸지 않습니다.

## 사용

에이전트에게 이렇게 말하면 시작합니다: 「교안 만들어줘」, 「노트북LM으로 조사해서 정리해줘」, 「시장조사 리포트 만들어줘」.
에이전트가 한 번에 하나씩 묻고, 검색계획 → 수집 결과 → 목차 → 초안 네 지점에서 확인을 받습니다.

## 제거
```bash
uv tool uninstall notebooklm-mcp-cli yt-dlp
rm -rf ~/.nrb ~/.claude/skills/notebook-research-builder ~/.codex/skills/notebook-research-builder
```
docx·pptx 스킬, Node.js, pandoc, LibreOffice 등은 다른 프로그램도 쓸 수 있어 자동으로 지우지 않습니다.

## 라이선스·출처
- NotebookLM 조작: [jacob-bd/gemini-notebook-mcp-cli](https://github.com/jacob-bd/gemini-notebook-mcp-cli) (MIT). NotebookLM의 비공식 내부 API를 쓰므로 Google 쪽 변경으로 일시적으로 동작하지 않을 수 있습니다.
- docx·pptx 스킬: [anthropics/skills](https://github.com/anthropics/skills)
