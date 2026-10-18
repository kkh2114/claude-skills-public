# notebook-research-builder 설치 시작점 (Windows PowerShell)
#   powershell -ExecutionPolicy Bypass -File scripts\install.ps1 [--check] [--skip a,b] [--login] [--agent claude|codex|both]
# uv(파이썬·도구 관리자)만 확보한 뒤, 나머지 탐색·설치는 setup.py가 한다. 파이썬이 없어도 uv가 받아 온다.
$ErrorActionPreference = "Stop"
$Dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

if (Get-Command uv -ErrorAction SilentlyContinue) {
  Write-Host "✓ uv: 이미 설치됨 ($(uv --version)) — 건너뜀"
} elseif ($args -contains "--check") {
  Write-Host "✗ uv: 없음 (탐색 모드라 설치하지 않음)"; exit 2
} else {
  Write-Host "… uv: 설치 중"
  if (Get-Command winget -ErrorAction SilentlyContinue) {
    winget install -e --id astral-sh.uv --silent --accept-package-agreements --accept-source-agreements
  } else {
    powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"
  }
  $env:Path = "$env:USERPROFILE\.local\bin;$env:LOCALAPPDATA\Microsoft\WinGet\Links;$env:Path"
  if (-not (Get-Command uv -ErrorAction SilentlyContinue)) { Write-Host "✗ uv 설치 후에도 찾을 수 없음 — 새 PowerShell 창에서 다시 실행"; exit 2 }
  Write-Host "✓ uv: 설치 완료 ($(uv --version))"
}

uv run --quiet --python ">=3.10" "$Dir\setup.py" @args
exit $LASTEXITCODE
