# 3. 수집·주입 (혼합, 자동)

목표: 노트북에 **조건(기간·주요 사이트 ≥60%)을 지킨 원천 지식**을 채운다. 검색 도구는 후보 URL을 찾는 데만 쓰고, 지식은 주입된 소스만이다.

## 순서
1. 사용자 문서(1단계에서 이미 주입)
2. **주요 사이트 × 기간** 몫 — 에이전트 검색 + 날짜 확인 + 주입 (목표 개수의 60% 이상)
3. **보충** 몫 — `nlm research` 후보 → 확인 → 골라서 import
4. `nrb.py ratio`로 확인 → 미달이면 2로 (키워드 변형·검색어 언어 바꾸기), 그래도 미달이면 게이트 ②에서 선택지 제시

## 후보 찾기 (키워드 변형 3~6개 × 사이트)
| 사이트 | 찾기 | 게시일 확인 |
|---|---|---|
| 유튜브 | yt-dlp: `yt-dlp "ytsearch10:<키워드>" --skip-download --no-warnings --print "%(upload_date)s\|%(webpage_url)s\|%(title).70s"` → `upload_date`로 기간 거르기 (`ytsearchdate`는 2026.08 버전에서 미지원) · 한글·영문 키워드 둘 다 | `upload_date` |
| 스레드·인스타·X·링크드인 | **크롬**: 사이트 검색 페이지(최신순)에서 목록 추출 → 없으면 어사이드 | 페이지의 `time[datetime]` |
| 블로그·뉴스·문서 | 에이전트 웹검색 도구(Claude WebSearch·Codex 웹검색 등, 기간 키워드 포함) | 페이지 본문·메타(`article:published_time`) |
| 논문 | arXiv·Semantic Scholar·Google Scholar 검색 | 제출일/출판일 |
- **관련성 필터**: 넣기 전에 제목·본문 첫 부분에 목표·키워드가 실제로 다뤄지는지 본다. 스레드 검색은 관련성이 낮다(실측: 「Claude Code 스킬」 검색 첫 결과가 무관한 글) → 키워드 여러 변형 + 걸러내기.
- 날짜를 확인 못 한 후보는 주요 사이트 몫으로 세지 않는다(보충 몫으로만).
- **게시일을 추측해 적지 않는다.** 페이지에서 확인 못 하면 `--date` 없이 넣거나 `nrb.py date … --date unknown`. 공식 문서는 게시일이 없는 경우가 많다(시험 실행 때 추측값을 넣었다가 고침).
- 셸(zsh)에서 URL은 **반드시 따옴표**로(`?`가 패턴으로 해석돼 실패). 여러 개를 넣을 땐 함수로: `add(){ uv run <스킬>/scripts/nrb.py add -P "$P" --url "$1" --date "$2"; }`

## 주입 — 종류별
```bash
# 공개 페이지·유튜브 → URL (유튜브는 자동으로 --youtube)
uv run <스킬>/scripts/nrb.py add -P <프로젝트> --url <URL> --date <YYYY-MM-DD> --via agent
# 로그인 벽 → 본문 추출 후 텍스트 (머리말: 출처·게시일·사이트·작성자·수집일·수집방법 자동)
uv run <스킬>/scripts/nrb.py add -P <프로젝트> --text-file <본문.txt> --url <원문 URL> --date <YYYY-MM-DD> --author @id --hint "<요지 몇 단어>" --via chrome
```
- 본문 파일은 프로젝트 `inbox/`에 두고 주입 뒤엔 남겨도 된다(기록). 본문은 **원문 그대로**(요약 금지), 화면 잔여물(답글창·버튼 글자)만 뺀다.
- URL 주입 결과가 로그인 화면·빈 내용이면(제목이 「로그인」류, `nlm source content`가 짧음) → 그 소스를 지울지 묻지 말고 **텍스트 추출로 다시 넣은 뒤**, 빈 소스 삭제는 게이트 ②에서 함께 묻는다.
- 같은 URL 두 번 넣기는 `nrb.py`가 막는다. 한도 도달도 막고 사람에게 넘긴다.

## 크롬 추출 (Claude in Chrome) — 실측된 방법
1. `tabs_context_mcp` → `tabs_create_mcp`로 새 탭(사용자 탭 재사용 금지)
2. 검색 목록 (스레드 예): `https://www.threads.com/search?q=<키워드>&serp_type=default&filter=recent` 로 이동 후 `javascript_tool`:
```js
await new Promise(r=>setTimeout(r,3000));
const loggedIn=!document.body.innerText.includes('Instagram으로 계속하기');
const seen=new Set(), out=[];
for (const t of document.querySelectorAll('time[datetime]')) { const a=t.closest('a[href*="/post/"]'); if(!a) continue;
  const href=new URL(a.getAttribute('href'),location.origin).href.split('?')[0]; if(seen.has(href)) continue; seen.add(href);
  out.push({url:href, date:t.getAttribute('datetime').slice(0,10)}); }
JSON.stringify({loggedIn, posts:out})
```
   필요하면 스크롤(`computer` scroll) 후 다시 실행해 더 모은다.
3. 게시물 페이지로 이동 → 본문:
```js
await new Promise(r=>setTimeout(r,3000));
const t=document.querySelector('time[datetime]'); const m=document.querySelector('[data-pressable-container]')||document.querySelector('main');
JSON.stringify({url:location.href.split('?')[0], date:t&&t.getAttribute('datetime'), title:document.title.replace(/^\(\d+\)\s*/,''), text:m.innerText})
```
   - 본문은 **`title`(페이지 제목)을 우선** 쓴다 — 스레드는 제목에 글 전체가 링크까지 온전히 들어 있고, `innerText`는 링크가 `github.com/obra…`처럼 잘린다. `innerText`는 제목이 잘렸을 때 보충용.
4. 본문을 `inbox/<사이트>-<id>.txt`로 저장 → `nrb.py add --text-file …`. 끝나면 만든 탭을 닫는다.
- 읽기만 한다(좋아요·댓글·팔로우 금지). 한 번에 수십 페이지를 빠르게 넘기지 않는다(개인 계정 보호 — 게시물 사이 2~3초).
- `loggedIn:false`면 멈추고 사람에게: 「크롬에서 <사이트>에 로그인해 주세요」(사람 차례). 크롬 도구 자체가 없으면 설치기를 다시 실행해 Claude in Chrome 설치를 안내.

## 어사이드 추출 (코덱스 등 Claude in Chrome이 없는 에이전트)
```bash
aside --host local exec "[규칙] 읽기만 해. 글쓰기·좋아요·팔로우·댓글 금지. 이미지·캡처를 화면에 띄우지 마. 로그인·캡차가 필요하면 멈추고 '로그인 필요'만 답해.
작업: <사이트>에서 '<키워드>'를 검색해 <since> 이후 게시물 <N>개를 골라 각 게시물 페이지를 열어 확인해 줘.
마지막 답은 각 게시물마다 아래 형식 그대로만:
=== POST
URL: <고유 URL>
게시일: <YYYY-MM-DD, 페이지의 실제 시간 정보로>
작성자: <@아이디>
본문:
<원문 그대로, 요약 금지>
=== END" </dev/null > <프로젝트>/inbox/aside-<키워드>.txt 2>&1
```
- **`</dev/null` 필수**(없으면 멈춤). 출력엔 도구 기록이 섞이므로 `=== POST`~`=== END` 사이만 잘라 게시물별 파일로 → `nrb.py add --via aside`.
- 마지막 줄이 `로그인 필요`면 사람에게 어사이드 브라우저에서 그 사이트 로그인을 안내(사람 차례). 사용자가 원하지 않으면 크롬으로 또는 건너뛰고 보고(사용자 선택). 오래 걸리면(10분+) 백그라운드로 돌리고 다른 수집을 계속.

## NotebookLM 리서치 (보충)
```bash
nlm research start "<영문/한글 검색어>" --notebook-id <NB>            # fast ~30초·~10개 / --mode deep ~5분·~40개
nlm research status <NB> --full                                        # 후보 목록(제목·URL)
nlm research import <NB> <task-id> --indices 0,2,5                     # 관련 있는 것만
uv run <스킬>/scripts/nrb.py ratio -P <프로젝트>                       # 장부에 없던 소스로 잡힘
uv run <스킬>/scripts/nrb.py date -P <프로젝트> --source-id <id> --date <YYYY-MM-DD|unknown>
```
- 리서치는 기간·사이트를 지정할 수 없다 → 검색어에 연도·월을 넣고, import 전에 후보를 걸러 낸다. `--auto-import`는 쓰지 않는다.

## 게이트 ② 보고 형식
소스 N개(한도 대비) · 기간 안 N개 · 주요 사이트×기간 비율(목표 대비 ✓/✗) · 사이트별 개수 · 날짜 미확인 N개 · 실패/건너뜀 목록(이유).
미달이면: 「①기간을 <제안>까지 넓히기 ②<사이트> 추가 ③이대로 진행 — 어떻게 할까요?」
