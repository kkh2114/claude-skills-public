# /// script
# requires-python = ">=3.10"
# ///
"""notebook-research-builder 설치기 — 이 PC의 조건을 탐색하고 필요한 것을 설치한다.
원칙: 설치가 기본. 이미 있으면 「이미 설치됨 — 건너뜀」을 남기고 다음으로. 우회(설치 안 함)는 사용자가 --skip 으로 고를 때만.

  bash scripts/install.sh            (macOS·Linux·WSL — uv 확보 후 이 파일 실행)
  powershell -File scripts/install.ps1   (Windows)
  uv run scripts/setup.py [--check] [--skip a,b] [--login] [--agent claude|codex|both]

  --check   탐색만 (아무것도 설치하지 않음)
  --skip    사용자가 설치하지 않기로 고른 구성요소 (예: --skip libreoffice,aside)
  --login   NotebookLM 구글 로그인 창까지 띄움 (사람 차례)
사람 손이 필요한 단계(브라우저 앱·확장·계정 로그인·관리자 암호)는 정확한 할 일을 안내하고, 끝낸 뒤 다시 실행하면 이어서 진행한다."""
import argparse, glob, json, os, platform, shutil, subprocess, sys, pathlib

HOME = pathlib.Path.home()
NRB = HOME / ".nrb"                       # 이 스킬 전용 도구 폴더 (사용자 환경을 건드리지 않음)
VENV = NRB / "venv"
NODE = NRB / "node"
SKILL_DIR = pathlib.Path(__file__).resolve().parent.parent
OS = {"Darwin": "mac", "Linux": "linux", "Windows": "win"}.get(platform.system(), "other")
WSL = OS == "linux" and "microsoft" in platform.release().lower()
EXE = ".exe" if OS == "win" else ""
CHROME_EXT = "fcoeoabgfenejglbffodgkkbkcdhcgfn"   # Claude in Chrome
PY_LIBS = ["lxml", "defusedxml", "pillow", "python-docx", "python-pptx", "markitdown[all]"]
NPM_PKGS = ["docx", "pptxgenjs", "react", "react-dom", "react-icons", "sharp"]

results = []          # (이름, 상태, 메모)  상태: skip=이미 설치됨, done=설치함, human=사람 차례, fail=실패, off=사용자 제외
args = None


def run(cmd, timeout=1800, check=False, **kw):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, **kw)
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return 127, str(e)
    if check and r.returncode != 0:
        raise RuntimeError((r.stdout + r.stderr).strip()[-600:])
    return r.returncode, (r.stdout + r.stderr).strip()


def which(*names):
    extra = [str(HOME / ".local" / "bin"), str(HOME / ".cargo" / "bin"), "/opt/homebrew/bin", "/usr/local/bin"]
    path = os.pathsep.join([os.environ.get("PATH", "")] + extra)
    for n in names:
        p = shutil.which(n, path=path)
        if p: return p
    return None


def uv(): return which("uv")


def tool_bin():
    c, out = run([uv(), "tool", "dir", "--bin"]) if uv() else (1, "")
    return pathlib.Path(out.splitlines()[-1]) if c == 0 and out else HOME / ".local" / "bin"


def pkg_install(mac=None, cask=None, apt=None, win=None):
    """OS 패키지 관리자로 설치. 권한·관리자가 필요하면 사람 차례 명령을 돌려준다."""
    if OS == "mac":
        if not which("brew"):
            return "human", '먼저 Homebrew 설치: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"  (맥 로그인 암호 필요) → 끝나면 설치기를 다시 실행'
        cmd = ["brew", "install"] + (["--cask", cask] if cask else [mac])
        c, out = run([which("brew")] + cmd[1:], timeout=3600)
        return ("done", "") if c == 0 else ("fail", out[-300:])
    if OS == "linux":
        if not apt: return "human", "이 배포판용 설치 명령을 찾아 직접 설치"
        if not which("apt-get"):
            return "human", f"apt가 없는 배포판 — 패키지 관리자로 {apt} 설치"
        c, _ = run(["sudo", "-n", "true"])
        if c != 0:
            return "human", f"관리자 암호가 필요: sudo apt-get update && sudo apt-get install -y {apt}  → 끝나면 다시 실행"
        run(["sudo", "apt-get", "update"], timeout=1800)
        c, out = run(["sudo", "apt-get", "install", "-y"] + apt.split(), timeout=3600)
        return ("done", "") if c == 0 else ("fail", out[-300:])
    if OS == "win":
        if not which("winget"):
            return "human", f"winget(앱 설치 관리자)이 없음 — Microsoft Store에서 '앱 설치 관리자' 설치 후 다시 실행 (또는 {win} 직접 설치)"
        c, out = run([which("winget"), "install", "-e", "--id", win, "--silent", "--accept-package-agreements", "--accept-source-agreements"], timeout=3600)
        return ("done", "새 터미널을 열어야 PATH에 잡힐 수 있음") if c == 0 else ("fail", out[-300:])
    return "human", "지원하지 않는 OS — 직접 설치"


def step(key, name, check, install=None, purpose="", already="이미 설치됨"):
    """check() -> (ok:bool, 메모)  install() -> (상태, 메모)"""
    label = name
    tail = f"  [{purpose}]" if purpose else ""
    ok, note = check()
    if ok:
        results.append((label, "skip", note)); print(f"✓ {label}: {already}{(' — ' + note) if note else ''} — 건너뜀{tail}"); return True
    if key in args.skip:
        results.append((label, "off", "사용자가 설치하지 않기로 선택")); print(f"– {label}: 사용자 선택으로 건너뜀"); return False
    if args.check or install is None:
        st = "missing" if args.check else "human"
        results.append((label, st, note)); print(f"✗ {label}: 없음{(' — ' + note) if note else ''}"); return False
    print(f"… {label}: 설치 중")
    try:
        st, msg = install()
    except Exception as e:
        st, msg = "fail", str(e)[-300:]
    if st == "done":
        ok, note2 = check()
        if not ok: st, msg = "fail", (msg + " / 설치 후에도 확인 안 됨 — 새 터미널에서 다시 실행").strip(" /")
    mark = {"done": "✓", "human": "⚠", "fail": "✗"}[st]
    word = {"done": "설치 완료", "human": "사람 차례", "fail": "설치 실패"}[st]
    print(f"{mark} {label}: {word}{(' — ' + msg) if msg else ''}")
    results.append((label, st, msg))
    return st == "done"


# ── 구성요소별 확인·설치 ─────────────────────────────────────────
def ck_uv():
    p = uv(); return (bool(p), run([p, "--version"])[1] if p else "")


def ck_python():
    # 이 설치기 자체가 uv가 고른 3.10+ 파이썬으로 돈다 → 그 버전을 보고하고, 이후 실행도 uv run이 같은 조건을 맞춘다
    return sys.version_info >= (3, 10), f"{platform.python_version()} (uv 관리)"


def in_python(): run([uv(), "python", "install", "3.12"], check=True); return "done", ""


def ck_uvtool(cmd):
    def f():
        p = which(cmd) or (tool_bin() / (cmd + EXE) if (tool_bin() / (cmd + EXE)).exists() else None)
        return (bool(p), run([str(p), "--version"])[1].splitlines()[0] if p else "")
    return f


def in_uvtool(pkg):
    def f():
        run([uv(), "tool", "install", "--upgrade", pkg], check=True)
        run([uv(), "tool", "update-shell"])
        return "done", f"실행 파일 위치 {tool_bin()}"
    return f


BROWSERS = {
    "mac": {"edge": "/Applications/Microsoft Edge.app", "brave": "/Applications/Brave Browser.app", "arc": "/Applications/Arc.app",
            "chromium": "/Applications/Chromium.app", "firefox": "/Applications/Firefox.app", "vivaldi": "/Applications/Vivaldi.app",
            "opera": "/Applications/Opera.app", "chrome": "/Applications/Google Chrome.app"},
    "win": {"edge": r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe", "brave": r"%ProgramFiles%\BraveSoftware\Brave-Browser\Application\brave.exe",
            "firefox": r"%ProgramFiles%\Mozilla Firefox\firefox.exe", "chrome": r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"},
    "linux": {"edge": "microsoft-edge", "brave": "brave-browser", "chromium": "chromium", "firefox": "firefox", "chrome": "google-chrome"},
}


def browsers():
    found = []
    for name, p in BROWSERS.get(OS, {}).items():
        if OS == "mac" and os.path.exists(p): found.append(name)
        elif OS == "win" and os.path.exists(os.path.expandvars(p)): found.append(name)
        elif OS == "linux" and (which(p) or which(p + "-browser") or (name == "chromium" and which("chromium-browser"))): found.append(name)
    return found


def ck_login_browser():
    b = [x for x in browsers() if x != "chrome"]   # 로그인은 크롬 밖에서 (크롬은 Claude in Chrome 용으로 비워 둠)
    nlm = nlm_bin()
    if b and os.path.exists(nlm) and not args.check:   # 탐색 모드에선 아무것도 바꾸지 않는다
        c, out = run([nlm, "config", "get", "auth.browser"])
        if b[0] not in out: run([nlm, "config", "set", "auth.browser", b[0]])
    return bool(b), (f"{b[0]} (nlm 로그인용으로 설정)" if b else "크롬 말고 지원 브라우저(Edge·Brave·Arc·Firefox 등)가 없음")


def in_login_browser():
    return pkg_install(cask="microsoft-edge", apt="firefox", win="Microsoft.Edge")


def nlm_bin(): return which("nlm") or str(tool_bin() / ("nlm" + EXE))


def ck_nlm_login():
    c, out = run([nlm_bin(), "login", "--check"], timeout=120)
    acct = next((l.split(":", 1)[1].strip() for l in out.splitlines() if "Account" in l), "")
    return c == 0 and "valid" in out.lower(), (f"계정 {acct}" if acct else "로그인 필요")


def in_nlm_login():
    if not args.login:
        return "human", "구글 로그인(본인만 가능): 설치기를 --login 으로 다시 실행하거나 `nlm login --storage protected` → 뜬 브라우저에서 NotebookLM 계정으로 로그인. 그 브라우저가 이미 떠 있으면 먼저 완전히 종료"
    subprocess.run([nlm_bin(), "login", "--storage", "protected"])
    return "done", ""


def ck_venv():
    py = VENV / ("Scripts/python.exe" if OS == "win" else "bin/python")
    if not py.exists(): return False, ""
    c, _ = run([str(py), "-c", "import lxml, defusedxml, PIL, docx, pptx, markitdown"])
    return c == 0, str(VENV)


def in_venv():
    run([uv(), "venv", "--python", "3.12", str(VENV)], check=True) if not VENV.exists() else None
    run([uv(), "pip", "install", "--python", str(VENV), *PY_LIBS], check=True, timeout=3600)
    return "done", f"{VENV} (docx·pptx 스킬 스크립트·markitdown 용)"


def ck_node():
    p = which("node")
    if not p: return False, ""
    v = run([p, "--version"])[1].lstrip("v")
    major = int(v.split(".")[0]) if v[:1].isdigit() else 0
    return major >= 18, f"v{v}" + ("" if major >= 18 else " — 18 이상 필요")


def in_node():
    if OS == "linux":
        return "human", "Node 18+ 설치(관리자 암호 필요): curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt-get install -y nodejs"
    return pkg_install(mac="node", win="OpenJS.NodeJS.LTS")


def ck_npm():
    nm = NODE / "node_modules"
    miss = [p for p in NPM_PKGS if not (nm / p).exists()]
    return not miss, (str(nm) if not miss else "없음: " + ", ".join(miss))


def in_npm():
    npm = which("npm")
    if not npm: return "fail", "npm이 없음 — Node 설치 확인"
    NODE.mkdir(parents=True, exist_ok=True)
    run([npm, "install", "--prefix", str(NODE), *NPM_PKGS], check=True, timeout=3600)
    return "done", f"{NODE / 'node_modules'} (NODE_PATH로 사용 — nrb.py env)"


def ck_cmd(*names):
    def f():
        p = which(*names)
        if not p and OS == "mac" and "soffice" in names and os.path.exists("/Applications/LibreOffice.app/Contents/MacOS/soffice"): p = "/Applications/LibreOffice.app"
        if not p and OS == "win" and "soffice" in names:
            for g in (r"%ProgramFiles%\LibreOffice\program\soffice.exe", r"%ProgramFiles(x86)%\LibreOffice\program\soffice.exe"):
                if os.path.exists(os.path.expandvars(g)): p = os.path.expandvars(g)
        return bool(p), p or ""
    return f


def ck_doc_skills():
    found = {}
    for agent, root in (("claude", HOME / ".claude"), ("codex", HOME / ".codex")):
        if agent not in args.agents: continue
        hits = {s: bool(glob.glob(str(root / "**" / s / "SKILL.md"), recursive=True)) for s in ("docx", "pptx")}
        if agent == "claude" and not all(hits.values()) and which("claude"):
            c, out = run([which("claude"), "plugin", "list"], timeout=120)
            if "document-skills" in out: hits = {"docx": True, "pptx": True}
        found[agent] = all(hits.values())
    miss = [a for a, ok in found.items() if not ok]
    return not miss, ("없음: " + ", ".join(miss)) if miss else ", ".join(found)


def in_doc_skills():
    notes = []
    if "claude" in args.agents:
        cl = which("claude")
        if not cl: notes.append("Claude Code CLI가 없음 — Claude Code에서 `/plugin marketplace add anthropics/skills` → `/plugin install document-skills@anthropic-agent-skills`")
        else:
            c, out = run([cl, "plugin", "marketplace", "list"], timeout=120)
            if "anthropic-agent-skills" not in out and "anthropics/skills" not in out:
                run([cl, "plugin", "marketplace", "add", "anthropics/skills"], check=True, timeout=600)
            run([cl, "plugin", "install", "-y", "document-skills@anthropic-agent-skills"], check=True, timeout=600)
    if "codex" in args.agents:
        src = NRB / "anthropic-skills"
        if not src.exists():
            if not which("git"): return "human", "git이 없음 — git 설치 후 다시 실행"
            run([which("git"), "clone", "--depth", "1", "https://github.com/anthropics/skills.git", str(src)], check=True, timeout=600)
        dst = HOME / ".codex" / "skills"; dst.mkdir(parents=True, exist_ok=True)
        for s in ("docx", "pptx", "pdf", "xlsx"):
            if not (dst / s).exists(): shutil.copytree(src / "skills" / s, dst / s)
    return ("human", " / ".join(notes)) if notes else ("done", "")


def chrome_profiles():
    base = {"mac": HOME / "Library/Application Support/Google/Chrome", "linux": HOME / ".config/google-chrome",
            "win": pathlib.Path(os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data"))}.get(OS)
    return base


def ck_chrome_ext():
    if "claude" not in args.agents: return True, "Claude Code 미사용 — 해당 없음"
    if "chrome" not in browsers(): return False, "크롬이 없음"
    base = chrome_profiles()
    hit = base and glob.glob(str(base / "*" / "Extensions" / CHROME_EXT))
    return bool(hit), ("확장 설치됨" if hit else "크롬은 있으나 Claude in Chrome 확장이 없음")


def in_chrome_ext():
    if "chrome" not in browsers():
        st, msg = pkg_install(cask="google-chrome", apt=None, win="Google.Chrome")
        if st != "done": return "human", "크롬 설치: https://www.google.com/chrome/ " + msg
    return "human", f"Claude in Chrome 확장 설치(사람): 크롬에서 https://chromewebstore.google.com/detail/{CHROME_EXT} → 「Chrome에 추가」 → 확장에서 Claude 계정 로그인 → Claude Code에서 /chrome 으로 연결 확인. 끝나면 다시 실행"


def ck_aside_cli():
    p = which("aside")
    return bool(p), run([p, "--version"])[1].splitlines()[0] if p else ""


def in_aside_cli():
    if OS == "win":
        return "human", "어사이드 CLI(Windows): https://docs.aside.com/help/developers 의 Windows 명령으로 설치 후 다시 실행"
    sh = which("bash"); cu = which("curl")
    if not (sh and cu): return "human", "curl·bash 필요 — https://docs.aside.com/help/developers"
    run([sh, "-c", "curl -fsSL https://releases.aside.com/install.sh | bash"], check=True, timeout=900)
    return "done", ""


def ck_aside_app():
    p = which("aside")
    if not p: return False, "CLI 먼저"
    c, out = run([p, "account", "status"], timeout=60)
    return c == 0 and "signed in" in out.lower(), ("로그인됨" if c == 0 and "signed in" in out.lower() else "어사이드 앱 설치·로그인 + CLI 로그인 필요")


def in_aside_app():
    return "human", "어사이드(사람): https://aside.com 에서 앱 설치·로그인 → 터미널 `aside login --email <메일>` 켜 둔 채 앱 Settings > Account > Devices에서 승인. 끝나면 다시 실행"


def ck_self():
    tgt = [d for a, d in (("claude", HOME / ".claude/skills"), ("codex", HOME / ".codex/skills")) if a in args.agents]
    miss = [str(d) for d in tgt if not (d / SKILL_DIR.name / "SKILL.md").exists()]
    return not miss, ("없음: " + ", ".join(miss)) if miss else "설치 위치: " + ", ".join(str(d) for d in tgt)


def in_self():
    for a, d in (("claude", HOME / ".claude/skills"), ("codex", HOME / ".codex/skills")):
        if a in args.agents and not (d / SKILL_DIR.name / "SKILL.md").exists():
            d.mkdir(parents=True, exist_ok=True)
            shutil.copytree(SKILL_DIR, d / SKILL_DIR.name, ignore=shutil.ignore_patterns("__pycache__", ".git"))
    return "done", ""


def main():
    global args
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true"); ap.add_argument("--login", action="store_true")
    ap.add_argument("--skip", default=""); ap.add_argument("--agent", choices=["claude", "codex", "both", "auto"], default="auto")
    args = ap.parse_args()
    args.skip = {x.strip() for x in args.skip.split(",") if x.strip()}
    if args.agent == "auto":
        args.agents = [a for a in ("claude", "codex") if (HOME / f".{a}").exists()] or ["claude"]
    else:
        args.agents = ["claude", "codex"] if args.agent == "both" else [args.agent]
    print(f"== notebook-research-builder 설치기 · OS {OS}{' (WSL)' if WSL else ''} · 에이전트 {', '.join(args.agents)} · {'탐색만' if args.check else '설치'}\n")
    NRB.mkdir(exist_ok=True)

    print("[필수 — 노트북·수집]")
    step("uv", "uv", ck_uv, None, purpose="파이썬·도구 관리자 — install.sh/ps1이 설치")
    step("python", "Python 3.10+", ck_python, in_python, purpose="스크립트 실행")
    step("nlm", "nlm (notebooklm-mcp-cli)", ck_uvtool("nlm"), in_uvtool("notebooklm-mcp-cli"), purpose="NotebookLM 조작")
    step("yt-dlp", "yt-dlp", ck_uvtool("yt-dlp"), in_uvtool("yt-dlp"), purpose="유튜브 검색·게시일")
    step("browser", "로그인용 브라우저", ck_login_browser, in_login_browser, purpose="nlm 구글 로그인")
    step("login", "NotebookLM 로그인", ck_nlm_login, in_nlm_login, purpose="사람 차례", already="이미 완료됨")
    print("\n[로그인 벽 사이트 수집 — 스레드·인스타 등]")
    step("chrome", "Claude in Chrome 확장", ck_chrome_ext, in_chrome_ext, purpose="Claude Code용 추출기")
    step("aside", "어사이드 CLI", ck_aside_cli, in_aside_cli, purpose="코덱스·대안 추출기")
    step("aside", "어사이드 앱·로그인", ck_aside_app, in_aside_app, purpose="사람 차례", already="이미 완료됨")
    print("\n[출력 — 워드·파워포인트]")
    step("docskills", "docx·pptx 스킬", ck_doc_skills, in_doc_skills, purpose="anthropics/skills")
    step("venv", "파이썬 문서 라이브러리", ck_venv, in_venv, purpose="lxml·python-docx·python-pptx·markitdown")
    step("node", "Node.js 18+", ck_node, in_node, purpose="docx·pptxgenjs")
    step("npm", "npm 패키지", ck_npm, in_npm, purpose=" ".join(NPM_PKGS))
    step("pandoc", "pandoc", ck_cmd("pandoc"), lambda: pkg_install(mac="pandoc", apt="pandoc", win="JohnMacFarlane.Pandoc"), purpose="문서 변환")
    step("libreoffice", "LibreOffice", ck_cmd("soffice", "libreoffice"), lambda: pkg_install(cask="libreoffice", apt="libreoffice", win="TheDocumentFoundation.LibreOffice"), purpose="PDF 렌더·QA (용량 큼)")
    step("poppler", "poppler (pdftoppm)", ck_cmd("pdftoppm"), lambda: pkg_install(mac="poppler", apt="poppler-utils", win="oschwartz10612.Poppler"), purpose="페이지 이미지 QA")
    print("\n[이 스킬]")
    step("self", "notebook-research-builder 스킬 배치", ck_self, in_self, purpose="에이전트 스킬 폴더")

    state = {"os": OS, "agents": args.agents, "results": [{"name": n, "status": s, "note": m} for n, s, m in results]}
    (NRB / "install-state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2))
    cnt = {k: sum(1 for _, s, _ in results if s == k) for k in ("skip", "done", "human", "fail", "off", "missing")}
    print(f"\n== 요약: 이미 설치 {cnt['skip']} · 새로 설치 {cnt['done']} · 사람 차례 {cnt['human']} · 실패 {cnt['fail']} · 사용자 제외 {cnt['off']}" + (f" · 없음 {cnt['missing']}" if args.check else ""))
    todo = [(n, m) for n, s, m in results if s in ("human", "fail")]
    if todo:
        print("\n남은 할 일 (끝내고 설치기를 다시 실행하면 이어서 진행):")
        for i, (n, m) in enumerate(todo, 1): print(f"  {i}. {n}: {m}")
    print(f"\n기록: {NRB / 'install-state.json'} · 사용 전 환경: eval \"$(uv run {SKILL_DIR / 'scripts' / 'nrb.py'} env)\"")
    sys.exit(0 if not todo and not cnt["missing"] else 2)


if __name__ == "__main__":
    main()
