#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""notebook-research-builder 도우미 — 노트북 단일 원천 원칙을 기계적으로 지키게 한다.
모든 지식은 노트북으로(add), 모든 문장은 노트북 질의에서(query → check). 로컬 폴더는 기록일 뿐 원천이 아니다.

  (실행은 어디서나 `uv run <스킬>/scripts/nrb.py …` — 파이썬이 없어도 uv가 맞춰 준다)
  nrb.py env [--ps]                                        작업 셸 경로 (eval "$(uv run nrb.py env)")
  nrb.py tier                                              요금제·소스 한도 (nlm usage)
  nrb.py init  --title "<주제>" --preset courseware [--notebook-id <id>] [--dir .]
  nrb.py scope -P <프로젝트> --since 2026-07-18 --sites youtube,threads [--ratio 0.6]
  nrb.py add   -P <프로젝트> --url <URL> [--date YYYY-MM-DD] [--via agent|research|user]
  nrb.py add   -P <프로젝트> --text-file <본문.txt> --url <원문URL> --date YYYY-MM-DD [--author @id] [--hint 요지] --via chrome|aside
  nrb.py add   -P <프로젝트> --file <사용자 문서.pdf> --via user
  nrb.py ratio -P <프로젝트>                               기간·주요 사이트 비율 + 한도
  nrb.py date  -P <프로젝트> --source-id <id> --date YYYY-MM-DD|unknown   리서치로 들어온 소스의 게시일 등록
  nrb.py query -P <프로젝트> --name <짧은이름> --q "<질문>" [--note] [--source-ids a,b]
  nrb.py check -P <프로젝트> --draft <초안.md>             인용 없는 문장·없는 소스 인용 찾기 + refs.md
  nrb.py export -P <프로젝트> [초안.md …] [--name 파일명]   [qNN:n] → 각주, output/에 md·html (워드·PPT 스킬 재료)
  nrb.py gate  -P <프로젝트> <1-4> [--note "..."]           게이트 통과 기록
  nrb.py status -P <프로젝트>                              어디까지 됐나 (재개용)
초안의 인용 표기: [qNN:n] = queries/NN-*.json 의 n번 인용 (예: [q03:2], 여러 개면 [q03:2][q05:1])"""
import argparse, datetime as dt, json, os, re, shutil, subprocess, sys, pathlib
from urllib.parse import urlparse

TODAY = dt.date.today().isoformat()
HOME = pathlib.Path.home()
WIN = os.name == "nt"
NRB_HOME = HOME / ".nrb"                  # setup.py가 만든 전용 도구 폴더


def _find_nlm():
    if os.environ.get("NLM_BIN"): return os.environ["NLM_BIN"]
    p = shutil.which("nlm")
    if p: return p
    for d in (HOME / ".local" / "bin", HOME / ".local" / "share" / "uv" / "tools" / "notebooklm-mcp-cli" / ("Scripts" if WIN else "bin")):
        c = d / ("nlm.exe" if WIN else "nlm")
        if c.exists(): return str(c)
    sys.exit("✗ nlm을 찾을 수 없음 — 먼저 설치기 실행: bash <스킬>/scripts/install.sh  (Windows: install.ps1)")


NLM = None   # 처음 쓸 때 찾는다 (env 명령은 nlm 없이도 돌아야 함)
SITES = [("youtube", ("youtube.com", "youtu.be")), ("threads", ("threads.com", "threads.net")),
         ("instagram", ("instagram.com",)), ("x", ("x.com", "twitter.com")), ("linkedin", ("linkedin.com",)),
         ("facebook", ("facebook.com",)), ("reddit", ("reddit.com",)), ("github", ("github.com",)),
         ("arxiv", ("arxiv.org",)), ("medium", ("medium.com",)), ("brunch", ("brunch.co.kr",)),
         ("naver-blog", ("blog.naver.com",)), ("tistory", ("tistory.com",)), ("velog", ("velog.io",))]
LIMITS = {"free": 50, "pro": 300}


def die(msg): sys.exit("✗ " + msg)


def nlm(*args, timeout=600):
    global NLM
    NLM = NLM or _find_nlm()
    # 산출물 기본 언어가 en이라 퀴즈 등이 영어로 나온다(퀴즈엔 --language 옵션 없음) → 기본 ko
    env = {**os.environ, "NOTEBOOKLM_HL": os.environ.get("NOTEBOOKLM_HL", "ko")}
    r = subprocess.run([NLM, *args], capture_output=True, text=True, timeout=timeout, env=env)
    return r.returncode, r.stdout, r.stderr


def nlm_json(*args, timeout=600):
    c, out, err = nlm(*args, "--json", timeout=timeout)
    i = min([x for x in (out.find("{"), out.find("[")) if x >= 0], default=-1)
    if c != 0 or i < 0:
        die(f"nlm {' '.join(args[:2])} 실패: {(err or out).strip()[-500:]}")
    return json.loads(out[i:])


def site_of(url):
    host = (urlparse(url).hostname or "").lower().removeprefix("www.").removeprefix("m.")
    for name, doms in SITES:
        if any(host == d or host.endswith("." + d) for d in doms): return name
    return host or "unknown"


def proj(p):
    d = pathlib.Path(p)
    if not (d / "state.json").exists(): die(f"{d} 에 state.json 없음 — 먼저 nrb.py init")
    return d, json.loads((d / "state.json").read_text())


def save_state(d, s): (d / "state.json").write_text(json.dumps(s, ensure_ascii=False, indent=2))


def ledger(d):
    f = d / "sources.jsonl"
    return [json.loads(l) for l in f.read_text().splitlines() if l.strip()] if f.exists() else []


def tier_info():
    c, out, err = nlm("usage", timeout=120)
    m = re.search(r"Plan:\s*(\S+)", out)
    plan = m.group(1) if m else "UNKNOWN"
    t = "pro" if any(k in plan.upper() for k in ("PRO", "ULTRA", "PLUS", "BUSINESS", "ENTERPRISE")) else ("free" if m else "unknown")
    return plan, t


def cmd_tier(a):
    plan, t = tier_info()
    print(f"요금제: {plan} → {t}")
    print(f"노트북당 소스 한도(대략): 무료 {LIMITS['free']}개 · 유료(Pro 등) {LIMITS['pro']}개 — 이 프로젝트 기준 {LIMITS.get(t, LIMITS['free'])}개")
    print("무료면: 소스를 30~40개로 압축해 모으고, 한도가 차면 뺄 소스를 고르거나 유료 전환을 판단한다.")


def cmd_init(a):
    slug = re.sub(r"[^\w가-힣-]+", "-", a.title).strip("-")[:40]
    d = pathlib.Path(a.dir) / f"{TODAY}_{slug}"
    if (d / "state.json").exists(): die(f"이미 있음: {d} (이어서 하려면 status)")
    for sub in ("queries", "draft", "output", "inbox"): (d / sub).mkdir(parents=True, exist_ok=True)
    nb = a.notebook_id
    if not nb:
        nb = nlm_json("notebook", "create", a.title)["notebook_id"]
    plan, t = tier_info()
    s = {"title": a.title, "preset": a.preset, "notebook_id": nb, "created": TODAY, "plan": plan, "tier": t,
         "limit": LIMITS.get(t, LIMITS["free"]), "scope": {}, "gates": {}, "queries": 0}
    save_state(d, s)
    (d / "sources.jsonl").touch()
    print(f"✓ 프로젝트 {d}\n✓ 노트북 {nb}  https://notebook.google.com/notebook/{nb}\n  요금제 {plan} ({t}) · 소스 한도 약 {s['limit']}개")
    print(f"PROJECT={d}\nNOTEBOOK_ID={nb}")


def cmd_scope(a):
    d, s = proj(a.P)
    s["scope"] = {"since": a.since, "sites": [x.strip() for x in a.sites.split(",") if x.strip()], "ratio": a.ratio}
    save_state(d, s)
    print(f"✓ 범위: {a.since} 이후 · 주요 사이트 {s['scope']['sites']} ≥ {int(a.ratio*100)}%")


def cmd_add(a):
    d, s = proj(a.P)
    nb = s["notebook_id"]
    rows = ledger(d)
    if a.url and not a.text_file and any(r.get("url") == a.url for r in rows):
        die(f"이미 넣은 URL: {a.url}")
    if len(rows) >= s["limit"]:
        die(f"소스 한도 {s['limit']}개 도달 — 뺄 소스를 고르거나 유료 전환 판단 (사람에게)")
    rec = {"added": TODAY, "via": a.via, "date": a.date, "url": a.url, "site": site_of(a.url) if a.url else "file"}
    if a.text_file:
        if not (a.url and a.date): die("텍스트 소스는 --url(원문)과 --date(게시일)가 필수 — 노트북이 출처·날짜를 알아야 한다")
        body = pathlib.Path(a.text_file).read_text().strip()
        if len(body) < 40: die("본문이 너무 짧음 — 추출 실패(로그인 화면·빈 페이지)인지 확인")
        if len(body) > 150_000: die("본문이 너무 김 — 나눠서 넣기")
        head = f"출처: {a.url}\n게시일: {a.date} | 사이트: {rec['site']}" + (f" | 작성자: {a.author}" if a.author else "") + \
               f" | 수집일: {TODAY} | 수집: {a.via}\n---\n"
        # 대괄호는 nlm 출력(rich)에서 사라져 보이므로 제목에 쓰지 않는다
        title = " ".join(x for x in (a.date, rec["site"], (a.author or "").lstrip("@"), a.hint or body[:30].replace("\n", " ")) if x)
        res = nlm_json("source", "add", nb, "--text", head + body, "--title", title, "--wait")
        rec.update(kind="text", author=a.author, title=title)
    elif a.file:
        res = nlm_json("source", "add", nb, "--file", a.file, "--wait")
        rec.update(kind="file", title=pathlib.Path(a.file).name, site="user-file")
    elif a.url:
        flag = "--youtube" if rec["site"] == "youtube" else "--url"
        res = nlm_json("source", "add", nb, flag, a.url, "--wait")
        rec.update(kind="url")
    else:
        die("--url / --text-file / --file 중 하나")
    src = res[0] if isinstance(res, list) else res
    rec["source_id"] = src.get("source_id") or src.get("id")
    rec["title"] = src.get("title") or rec.get("title")
    with open(d / "sources.jsonl", "a") as f: f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"✓ {rec['kind']} 넣음: {rec['title']} · {rec['site']} · 게시일 {rec['date'] or '미확인'} · {rec['source_id']}")


def cmd_ratio(a):
    d, s = proj(a.P)
    rows = ledger(d)
    live = nlm_json("source", "list", s["notebook_id"])
    known = {r["source_id"] for r in rows}
    extra = [x for x in live if x["id"] not in known]   # 리서치 import 등 장부에 없는 소스
    for x in extra:
        rows.append({"source_id": x["id"], "title": x["title"], "url": x.get("url"), "site": site_of(x["url"]) if x.get("url") else x.get("type"), "date": None, "via": "untracked"})
    live_ids = {x["id"] for x in live}
    rows = [r for r in rows if r["source_id"] in live_ids]   # 노트북에서 지워진 건 빼고
    sc = s.get("scope") or {}
    since, sites, need = sc.get("since"), set(sc.get("sites") or []), sc.get("ratio", 0.6)
    n = len(rows)
    in_win = [r for r in rows if r.get("date") and since and r["date"] >= since]
    no_date = [r for r in rows if not r.get("date") and r.get("via") != "user"]
    main = [r for r in rows if r.get("site") in sites]
    main_win = [r for r in main if r in in_win]
    print(f"소스 {n}개 / 한도 약 {s['limit']}개 (남은 칸 {s['limit'] - n})")
    if since: print(f"기간 {since} 이후: {len(in_win)}개 · 게시일 미확인 {len(no_date)}개")
    if sites:
        share = len(main_win) / n if n else 0
        print(f"주요 사이트 {sorted(sites)} & 기간 안: {len(main_win)}개 = {share:.0%} (목표 {need:.0%}) → {'✓ 충족' if share >= need else '✗ 미달'}")
    by = {}
    for r in rows: by[r.get("site")] = by.get(r.get("site"), 0) + 1
    print("사이트별:", ", ".join(f"{k} {v}" for k, v in sorted(by.items(), key=lambda kv: -kv[1])))
    if extra: print(f"장부에 없던 소스 {len(extra)}개(리서치 import 등) — 게시일 확인 필요:\n  " + "\n  ".join(x["title"][:70] for x in extra[:15]))


def cmd_query(a):
    d, s = proj(a.P)
    args = ["notebook", "query", s["notebook_id"], a.q, "--timeout", "300"]
    if a.source_ids: args += ["--source-ids", a.source_ids]
    res = nlm_json(*args, timeout=360)
    s["queries"] = s.get("queries", 0) + 1
    no = f"{s['queries']:02d}"
    name = re.sub(r"[^\w가-힣-]+", "-", a.name).strip("-")[:30]
    titles = {x["id"]: x["title"] for x in nlm_json("source", "list", s["notebook_id"])}
    res["citation_titles"] = {k: titles.get(v, v) for k, v in (res.get("citations") or {}).items()}
    (d / "queries" / f"{no}-{name}.json").write_text(json.dumps(res, ensure_ascii=False, indent=2))
    md = f"# q{no} {a.name}\n\n질문: {a.q}\n\n{res['answer']}\n\n## 인용\n" + \
         "\n".join(f"- [q{no}:{k}] {t}" for k, t in res["citation_titles"].items())
    (d / "queries" / f"{no}-{name}.md").write_text(md)
    save_state(d, s)
    if a.note:
        nlm("note", "create", s["notebook_id"], "--content", md, "--title", f"q{no} {a.name}", timeout=120)
    print(md)
    print(f"\n→ 초안에선 [{'q'+no}:n] 으로 인용. 저장: queries/{no}-{name}.json" + (" · 노트북 노트로도 저장" if a.note else ""))


def cmd_check(a):
    d, s = proj(a.P)
    text = pathlib.Path(a.draft).read_text()
    qs = {}
    for f in (d / "queries").glob("*.json"):
        qs[f.name[:2]] = json.loads(f.read_text())
    live = {x["id"]: x for x in nlm_json("source", "list", s["notebook_id"])}
    led = {r["source_id"]: r for r in ledger(d)}
    bad_lines, bad_refs, used = [], [], {}
    for i, line in enumerate(text.splitlines(), 1):
        t = line.strip()
        if not t or t.startswith(("#", "|---", "---", "```", "![", "<!--")) or re.fullmatch(r"[\W\d_]+", t): continue
        cites = re.findall(r"\[q(\d{2}):(\d+)\]", t)
        if not cites and len(re.sub(r"[\s*_`>|-]", "", t)) >= 15 and not t.startswith(("[출처 불필요]", "<!-- no-cite")):
            bad_lines.append((i, t[:80]))
        for q, n in cites:
            sid = (qs.get(q, {}).get("citations") or {}).get(n)
            if not sid: bad_refs.append((i, f"[q{q}:{n}] 질의 기록에 없음")); continue
            if sid not in live: bad_refs.append((i, f"[q{q}:{n}] 소스가 노트북에서 지워짐")); continue
            used[sid] = used.get(sid, 0) + 1
    refs = ["# 참고 소스 (노트북 기준)\n"]
    for sid, c in sorted(used.items(), key=lambda kv: -kv[1]):
        r, l = led.get(sid, {}), live[sid]
        refs.append(f"- {l['title']}" + (f" — {r.get('url') or l.get('url')}" if (r.get('url') or l.get('url')) else "") +
                    (f" (게시 {r['date']})" if r.get("date") else "") + f" · 인용 {c}회")
    (d / "draft" / "refs.md").write_text("\n".join(refs) + "\n")
    print(f"인용된 소스 {len(used)}개 / 노트북 소스 {len(live)}개 → draft/refs.md")
    if bad_lines: print(f"✗ 인용 없는 문장 {len(bad_lines)}개 (노트북에 질의해 근거를 달거나 지운다):\n  " + "\n  ".join(f"{i}: {t}" for i, t in bad_lines[:40]))
    if bad_refs: print(f"✗ 잘못된 인용 {len(bad_refs)}개:\n  " + "\n  ".join(f"{i}: {t}" for i, t in bad_refs[:40]))
    if not bad_lines and not bad_refs: print("✓ 모든 문장이 노트북 소스에 근거함")
    sys.exit(1 if bad_lines or bad_refs else 0)


def cmd_env(a):
    """작업 셸에 필요한 경로를 내보낸다: eval "$(uv run nrb.py env)"  (PowerShell: uv run nrb.py env --ps | iex)"""
    venv_bin = NRB_HOME / "venv" / ("Scripts" if WIN else "bin")
    paths = [str(HOME / ".local" / "bin"), str(venv_bin), str(NRB_HOME / "node" / "node_modules" / ".bin")]
    node_path = str(NRB_HOME / "node" / "node_modules")
    py = venv_bin / ("python.exe" if WIN else "python")
    if a.ps:
        print(f'$env:Path = "{";".join(paths)};$env:Path"; $env:NODE_PATH = "{node_path}"; $env:NOTEBOOKLM_HL = "ko"; $env:NRB_PY = "{py}"')
    else:
        print(f'export PATH="{":".join(paths)}:$PATH"; export NODE_PATH="{node_path}"; export NOTEBOOKLM_HL=ko; export NRB_PY="{py}"')


def cmd_export(a):
    """초안의 [qNN:n]을 각주 번호로 바꿔 output/에 md(워드·PPT 스킬 재료)와 html(웹)로 낸다. 새 내용은 넣지 않는다."""
    import html as H
    d, s = proj(a.P)
    qs = {f.name[:2]: json.loads(f.read_text()) for f in (d / "queries").glob("*.json")}
    led = {r["source_id"]: r for r in ledger(d)}
    live = {x["id"]: x for x in nlm_json("source", "list", s["notebook_id"])}   # 장부에 없는 소스의 URL 보충
    files = [pathlib.Path(x) for x in a.drafts] or sorted(p for p in (d / "draft").glob("*.md") if p.name != "refs.md")
    order, notes = {}, []

    def num(q, n):
        sid = (qs.get(q, {}).get("citations") or {}).get(n)
        if not sid: die(f"[q{q}:{n}] 질의 기록에 없음 — 먼저 nrb.py check")
        if sid not in order:
            order[sid] = len(order) + 1
            r = led.get(sid, {})
            notes.append((order[sid], qs[q]["citation_titles"].get(n, sid), r.get("url") or live.get(sid, {}).get("url"), r.get("date")))
        return order[sid]

    md_lines, html_lines = [], []
    for f in files:
        for line in f.read_text().splitlines():
            line = line.replace("[출처 불필요] ", "")
            md_lines.append(re.sub(r"\[q(\d{2}):(\d+)\]", lambda m: f"[^{num(m.group(1), m.group(2))}]", line))
            e = H.escape(line)
            e = re.sub(r"`([^`]+)`", r"<code>\1</code>", e)
            e = re.sub(r"\[q(\d{2}):(\d+)\]", lambda m: f'<sup><a href="#fn{num(m.group(1), m.group(2))}">{num(m.group(1), m.group(2))}</a></sup>', e)
            if e.startswith("# "): html_lines.append(f"<h1>{e[2:]}</h1>")
            elif e.startswith("## "): html_lines.append(f"<h2>{e[3:]}</h2>")
            elif e.startswith("### "): html_lines.append(f"<h3>{e[4:]}</h3>")
            elif e.startswith("- "): html_lines.append(f"<li>{e[2:]}</li>")
            elif e.strip(): html_lines.append(f"<p>{e}</p>")
        md_lines.append("")
    notes.sort()
    md_lines += ["## 참고 소스", ""] + [f"[^{i}]: {t}" + (f" — {u}" if u else "") + (f" (게시 {dt_})" if dt_ else "") for i, t, u, dt_ in notes]
    body = re.sub(r"((?:<li>.*?</li>\n?)+)", lambda m: "<ul>" + m.group(1) + "</ul>", "\n".join(html_lines))
    refs = "".join(f'<li id="fn{i}">{H.escape(t)}' + (f' — <a href="{H.escape(u)}">{H.escape(u)}</a>' if u else "") + (f" (게시 {dt_})" if dt_ else "") + "</li>" for i, t, u, dt_ in notes)
    css = (":root{--bg:#fff;--fg:#1d1d1f;--mut:#6e6e73;--ac:#0b6bcb}@media (prefers-color-scheme:dark){:root{--bg:#151517;--fg:#ececf0;--mut:#9a9aa2;--ac:#6fb1ff}}"
           "body{background:var(--bg);color:var(--fg);font:16px/1.7 -apple-system,'Apple SD Gothic Neo',sans-serif;max-width:760px;margin:0 auto;padding:24px 16px}"
           "code{background:rgba(127,127,127,.15);padding:1px 5px;border-radius:4px}a{color:var(--ac)}sup a{text-decoration:none}.refs{color:var(--mut);font-size:14px}")
    name = a.name or re.sub(r"[^\w가-힣-]+", "-", s["title"]).strip("-")
    (d / "output" / f"{name}.md").write_text("\n".join(md_lines) + "\n")
    (d / "output" / f"{name}.html").write_text(f'<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{H.escape(s["title"])}</title><style>{css}</style>{body}<h2>참고 소스</h2><ol class="refs">{refs}</ol></html>')
    print(f"✓ output/{name}.md · output/{name}.html (초안 {len(files)}개 · 각주 {len(notes)}개)")


def cmd_date(a):
    """리서치 import 등 장부에 없던 소스에 확인한 게시일을 등록한다 (게시일을 모르면 --date unknown)."""
    d, s = proj(a.P)
    live = {x["id"]: x for x in nlm_json("source", "list", s["notebook_id"])}
    if a.source_id not in live: die("노트북에 없는 source_id")
    rows = ledger(d)
    date = None if a.date == "unknown" else a.date
    for r in rows:
        if r["source_id"] == a.source_id:
            r["date"] = date
            if a.site: r["site"] = a.site
            break
    else:
        x = live[a.source_id]
        rows.append({"added": TODAY, "via": "research", "date": date, "url": x.get("url"),
                     "site": a.site or (site_of(x["url"]) if x.get("url") else x.get("type")), "kind": "url", "source_id": a.source_id, "title": x["title"]})
    (d / "sources.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    print(f"✓ {live[a.source_id]['title'][:60]} → 게시일 {date or '미확인'}")


def cmd_gate(a):
    d, s = proj(a.P)
    s.setdefault("gates", {})[str(a.n)] = {"at": dt.datetime.now().isoformat(timespec="minutes"), "note": a.note}
    save_state(d, s)
    print(f"✓ 게이트 {a.n} 통과 기록")


def cmd_status(a):
    d, s = proj(a.P)
    rows, g = ledger(d), s.get("gates", {})
    nq = len(list((d / "queries").glob("*.json")))
    drafts = [p.name for p in (d / "draft").glob("*.md") if p.name != "refs.md"]
    outs = [p.name for p in (d / "output").iterdir()] if (d / "output").exists() else []
    print(f"{s['title']} · 프리셋 {s['preset']} · 노트북 {s['notebook_id']} · 요금제 {s.get('tier')}")
    steps = [("범위 설정(scope)", bool(s.get("scope"))), ("게이트① 검색계획", "1" in g), (f"소스 수집 ({len(rows)}개 기록)", len(rows) > 0),
             ("게이트② 수집 보고", "2" in g), (f"커버리지 질의 ({nq}개)", nq > 0), ("게이트③ 목차", "3" in g),
             (f"초안 ({', '.join(drafts) or '없음'})", bool(drafts)), ("게이트④ 출력 형식", "4" in g), (f"출력 ({', '.join(outs) or '없음'})", bool(outs))]
    nxt = None
    for name, ok in steps:
        print(("✓ " if ok else "✗ ") + name)
        if not ok and nxt is None: nxt = name
    print("다음:", nxt or "완료 — 같은 노트북으로 다른 관점 산출물을 만들 수 있다")


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sp = ap.add_subparsers(dest="cmd", required=True)
sp.add_parser("tier").set_defaults(f=cmd_tier)
p = sp.add_parser("env"); p.add_argument("--ps", action="store_true", help="PowerShell 형식"); p.set_defaults(f=cmd_env)
p = sp.add_parser("init"); p.add_argument("--title", required=True); p.add_argument("--preset", default="courseware")
p.add_argument("--notebook-id"); p.add_argument("--dir", default="."); p.set_defaults(f=cmd_init)
p = sp.add_parser("scope"); p.add_argument("-P", required=True); p.add_argument("--since", required=True)
p.add_argument("--sites", default=""); p.add_argument("--ratio", type=float, default=0.6); p.set_defaults(f=cmd_scope)
p = sp.add_parser("add"); p.add_argument("-P", required=True); p.add_argument("--url"); p.add_argument("--text-file"); p.add_argument("--file")
p.add_argument("--date"); p.add_argument("--author"); p.add_argument("--hint")
p.add_argument("--via", default="agent", choices=["agent", "research", "user", "chrome", "aside"]); p.set_defaults(f=cmd_add)
p = sp.add_parser("ratio"); p.add_argument("-P", required=True); p.set_defaults(f=cmd_ratio)
p = sp.add_parser("query"); p.add_argument("-P", required=True); p.add_argument("--name", required=True); p.add_argument("--q", required=True)
p.add_argument("--note", action="store_true"); p.add_argument("--source-ids"); p.set_defaults(f=cmd_query)
p = sp.add_parser("check"); p.add_argument("-P", required=True); p.add_argument("--draft", required=True); p.set_defaults(f=cmd_check)
p = sp.add_parser("export"); p.add_argument("-P", required=True); p.add_argument("drafts", nargs="*", help="비우면 draft/*.md 전부(파일명 순)")
p.add_argument("--name"); p.set_defaults(f=cmd_export)
p = sp.add_parser("date"); p.add_argument("-P", required=True); p.add_argument("--source-id", required=True)
p.add_argument("--date", required=True, help="YYYY-MM-DD 또는 unknown"); p.add_argument("--site", help="URL 없는 소스의 사이트 (예: threads)")
p.set_defaults(f=cmd_date)
p = sp.add_parser("gate"); p.add_argument("-P", required=True); p.add_argument("n", type=int, choices=[1, 2, 3, 4]); p.add_argument("--note"); p.set_defaults(f=cmd_gate)
p = sp.add_parser("status"); p.add_argument("-P", required=True); p.set_defaults(f=cmd_status)
a = ap.parse_args(); a.f(a)
