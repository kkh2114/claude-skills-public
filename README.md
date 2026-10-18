# claude-skills-public

강의에서 쓰는 **공개 에이전트 스킬 모음**입니다. Claude Code와 Codex에서 쓸 수 있습니다.
스킬은 에이전트에게 "이런 일은 이렇게 하라"는 절차를 담은 폴더입니다. 설치해 두면 관련된 말을 했을 때 에이전트가 알아서 꺼내 씁니다.

## 설치

### 1. 내려받기
```bash
git clone https://github.com/kkh2114/claude-skills-public.git
cd claude-skills-public
```
git이 없으면 이 페이지의 초록색 **Code → Download ZIP**으로 받아 압축을 풀고, 그 폴더에서 터미널을 엽니다.

### 2. 설치하기
**macOS · Linux**
```bash
bash install.sh                          # Claude Code (~/.claude/skills)
bash install.sh --to ~/.codex/skills     # Codex
```
**Windows (PowerShell)**
```powershell
powershell -ExecutionPolicy Bypass -File install.ps1                          # Claude Code
powershell -ExecutionPolicy Bypass -File install.ps1 -To "$HOME\.codex\skills"  # Codex
```
- 하나만 설치: `bash install.sh --skill <스킬 이름>` (Windows: `-Skill <스킬 이름>`)
- 목록만 보기: `bash install.sh --list` (Windows: `-List`)
- 함께 쓰면 좋은 스킬은 자동으로 같이 설치됩니다.

### 3. 설치 후 할 일이 있는 스킬
설치 화면 끝에 **「설치 후 꼭 실행할 것」**이 나오면 그대로 실행합니다. 지금은 `notebook-research-builder`가 해당합니다. 그 설치기가 필요한 도구를 PC에서 찾아보고 없는 것만 설치합니다.
```bash
bash notebook-research-builder/scripts/install.sh
```
```powershell
powershell -ExecutionPolicy Bypass -File notebook-research-builder\scripts\install.ps1
```

설치가 끝나면 Claude Code나 Codex를 **새로 열어야** 스킬이 보입니다.

## 스킬 목록

| 스킬 | 하는 일 | 이렇게 말하면 시작 |
|---|---|---|
| [harness-starter-workspace](./harness-starter-workspace) | 처음 쓰는 사람용. 검증된 템플릿을 복제해 분석·기획·문서·리서치 작업공간을 만든다 | "쉽게 하네스 만들어줘", "블로그 팀 만들어줘" |
| [harness-starter-coding](./harness-starter-coding) | 처음 쓰는 사람용. 웹앱·API·모바일·데이터 개발 작업공간을 템플릿으로 만든다 | "쉽게 코딩 하네스 만들어줘", "처음 앱 만들어봐" |
| [harness-designer-workspace](./harness-designer-workspace) | 숙련자용. 어떤 분야든 작업공간 구조를 설계·구축·검증한다 | "하네스 만들어줘", "워크스페이스 설계" |
| [harness-designer-coding](./harness-designer-coding) | 숙련자용. 코딩 에이전트가 안정적으로 개발·테스트·배포하는 구조를 설계한다 | "코딩 하네스 만들어줘", "개발 워크스페이스 설계" |
| [cartesian-review](./cartesian-review) | 데카르트 5렌즈(열거·명증·종합·분석·방법적 회의)로 문서·설계·계획을 검토한다. 하네스 설계 스킬이 검증 단계에서 함께 쓴다 | "데카르트 분석", "빠진 것 찾아줘" |
| [karpathy-guidelines](./karpathy-guidelines) | LLM이 코딩할 때 자주 하는 실수를 줄이는 행동 지침 | 코드 작성·리뷰·리팩터링 시 자동 |
| [notebook-research-builder](./notebook-research-builder) | NotebookLM 노트북 하나를 유일한 근거로 교안·시장조사·트렌드 리포트·논문 리뷰를 만든다(워드·PPT·웹·오디오·퀴즈). 자세한 설명은 폴더의 README | "교안 만들어줘", "노트북LM으로 조사해서 정리" |

어디서 시작할지 모르겠으면: 작업공간을 처음 만들면 **harness-starter-*** → 익숙해지면 **harness-designer-***.

## 업데이트
```bash
cd claude-skills-public
git pull
bash install.sh          # 다시 설치하면 새 버전으로 덮어씁니다
```
바뀐 내용은 [CHANGELOG.md](./CHANGELOG.md)에 있습니다.

## 이전 저장소
`harness-design-skills`, `harness-coding-skills`에 있던 스킬은 모두 이 저장소로 모였습니다. 앞으로는 이 저장소가 최신입니다.

## 출처
- `karpathy-guidelines` — [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) 기반, MIT License
- `harness-designer-*`, `harness-starter-*`는 [revfactory/harness-100](https://github.com/revfactory/harness-100) (Apache-2.0)의 exemplar를 참조 기준으로 사용
- `notebook-research-builder`는 [jacob-bd/gemini-notebook-mcp-cli](https://github.com/jacob-bd/gemini-notebook-mcp-cli) (MIT)의 `nlm` CLI를 사용
- 그 밖의 스킬 © kkh2114
