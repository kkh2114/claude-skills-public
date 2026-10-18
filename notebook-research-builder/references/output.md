# 7. 출력 — 형식만 바꾼다 (내용은 draft = 노트북 근거)

출력 전에 전 섹션 `nrb.py check` ✓. 출력은 `draft/*.md`를 재료로만 만든다(새 내용 추가 금지).
**먼저 각주판을 만든다**:
```bash
uv run <스킬>/scripts/nrb.py export -P <프로젝트> [draft/01-….md …]    # 비우면 draft 전부
```
→ `output/<주제>.md`(`[^n]` 각주 + 참고 소스 목록, 워드·PPT 스킬에 넘길 재료) · `output/<주제>.html`(라이트·다크 대응 단일 웹페이지, 바로 열람용).
슬라이드는 각주 대신 슬라이드 하단 짧은 출처 + 마지막 「참고 자료」 장.

| 형식 | 도구 | 메모 |
|---|---|---|
| 워드 (.docx) | `docx` 스킬 (anthropics/skills — 설치기가 설치) | 표지·목차·학습목표·본문·활동·참고 소스. 인쇄·배포용 |
| 파워포인트 (.pptx) | `pptx` 스킬 (anthropics/skills — 설치기가 설치) | 한 장 한 메시지. 본문 문장은 줄이되 근거 없는 문장 추가 금지. 발표자 노트에 상세 설명 |
| 웹 (HTML) | `nrb.py export`의 html | 그대로 `output/*.html`. 에이전트에 게시 도구(예: Claude의 Artifact)가 있고 공유 링크가 필요하면 게시 |
| NotebookLM Studio | `nlm` (아래) | 노트북 소스로 직접 생성 → 원칙에 가장 잘 맞는 보조 교재 |

**docx·pptx 스킬을 쓰기 전에** `eval "$(uv run <스킬>/scripts/nrb.py env)"` — 그 스킬들은 Anthropic 실행 환경에 「미리 깔려 있다」고 가정하므로, 일반 PC에선 이 환경이 필요하다:
- 스킬의 `require('docx')`·`require('pptxgenjs')` → `NODE_PATH`(= `~/.nrb/node/node_modules`)로 해결
- 스킬의 `python scripts/…` → **`"$NRB_PY" scripts/…`** 로 실행(lxml·defusedxml·Pillow·python-pptx가 든 `~/.nrb/venv`)
- `markitdown`·`pandoc`·`soffice`·`pdftoppm`은 PATH에서 바로
- 하나라도 없다는 오류가 나면 설치기를 다시 실행(`bash <스킬>/scripts/install.sh`) — 이미 된 건 건너뛴다

## NotebookLM Studio (보조 교재)
생성 전에 `nlm usage`(쿼터) 확인. 형식·스타일은 조용히 추론하고 한 줄로 알린 뒤 생성. 시네마틱 영상은 쿼터가 커서 꼭 먼저 묻는다.
**언어: 기본이 영어(`NOTEBOOKLM_HL=en`)다.** 퀴즈·플래시카드 등은 `--language` 옵션이 없고 `--focus`에 「한국어로」라고 써도 영어로 나왔다(시험 실행 실측) → 셸에서 먼저 `export NOTEBOOKLM_HL=ko` (`nrb.py`는 자동으로 ko).
```bash
export NOTEBOOKLM_HL=ko
nlm audio create <NB> --format deep_dive --length default --language ko --focus "<교안 목표·수준>" --confirm
nlm report create <NB> --format "Study Guide" --language ko --confirm
nlm quiz create <NB> --count 10 --difficulty 2 --focus "<차시 목표>" --confirm   # 기본은 2문항뿐 — --count 필수
nlm flashcards create <NB> --confirm
nlm mindmap create <NB> --confirm
nlm slides create <NB> --confirm               # NotebookLM 자체 슬라이드 (pptx 스킬과 별개)
nlm infographic create <NB> --confirm
nlm video create <NB> --confirm
nlm studio status <NB>                          # 완료 확인
nlm download <audio|slide-deck|report|quiz|flashcards|mind-map|infographic|video> <NB> --id <artifact> -o <프로젝트>/output/<파일명.확장자>
# 확장자를 붙인다(안 붙이면 확장자 없는 파일): quiz·flashcards·mind-map .json · report .md · audio .m4a · video .mp4 · infographic .png · slide-deck .pdf/.pptx
nlm slides revise …                             # 슬라이드 장별 수정 (nlm slides revise --help)
```
- 특정 섹션만: `--source-ids`로 그 섹션의 인용 소스만 지정(`queries/*.json`의 citations에서).
- 옵션 이름은 버전마다 바뀔 수 있다 → 실패하면 `nlm <종류> create --help`로 확인 후 다시.

## 같은 노트북으로 다른 관점 (재사용)
`nrb.py init --title "<새 산출물>" --preset <다른 프리셋> --notebook-id <기존 NB>` → 새 프로젝트 폴더, 같은 원천.
예: 교안 → 같은 노트북으로 「경영진용 트렌드 브리핑」, 「실습 퀴즈 세트」, 「시장 기회 리포트」.
