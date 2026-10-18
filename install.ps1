# install.ps1 — 스코프 기반 선별 설치 (Windows PowerShell, skills-manifest.json 참조)
#
# 사용:
#   powershell -ExecutionPolicy Bypass -File install.ps1                 # scope=global 스킬만 ~/.claude/skills 에 설치 (권장)
#   powershell -ExecutionPolicy Bypass -File install.ps1 -List           # 스코프 표만 출력
#   powershell -ExecutionPolicy Bypass -File install.ps1 -Skill <이름>   # 특정 스킬 1개만
#   ... -To "$HOME\.codex\skills"                                        # 코덱스 등 다른 위치에 설치
#
# 원칙: scope=project 스킬은 전역에 깔지 않는다 (install.sh와 같은 규칙).
param([switch]$List, [switch]$All, [string]$Skill = "", [string]$To = "$HOME\.claude\skills")
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Manifest = (Get-Content "$Root\skills-manifest.json" -Raw -Encoding UTF8 | ConvertFrom-Json).skills
$Names = $Manifest.PSObject.Properties.Name

if ($List) {
  foreach ($n in $Names) {
    $m = $Manifest.$n
    "{0,-34} {1,-8} {2}" -f $n, $m.scope, $m.origin
    if ($m.dependsOn) { "{0,-43} └─ 의존(하드): {1}" -f "", ($m.dependsOn -join ", ") }
    if ($m.optionalDependsOn) { "{0,-43} └─ 권장(소프트): {1}" -f "", ($m.optionalDependsOn -join ", ") }
  }
  exit 0
}

if ($Skill) {
  if ($Names -notcontains $Skill) { Write-Host "매니페스트에 없는 스킬: $Skill"; exit 1 }
  $Targets = @($Skill)
} elseif ($All) { $Targets = @($Names) } else { $Targets = @($Names | Where-Object { $Manifest.$_.scope -eq "global" }) }

# dependsOn(하드) + optionalDependsOn(소프트) 자동 포함 (전이적)
$Queue = [System.Collections.Generic.List[string]]::new($Targets); $Seen = @{}; $Final = @()
while ($Queue.Count -gt 0) {
  $n = $Queue[0]; $Queue.RemoveAt(0)
  if ($Seen[$n]) { continue }; $Seen[$n] = $true; $Final += $n
  foreach ($d in @($Manifest.$n.dependsOn) + @($Manifest.$n.optionalDependsOn)) { if ($d -and -not $Seen[$d]) { $Queue.Add($d) } }
}

New-Item -ItemType Directory -Force -Path $To | Out-Null
$Posts = @()
foreach ($n in $Final) {
  $src = Join-Path $Root $n
  if (-not (Test-Path $src)) { Write-Host "  ⚠️  $n: 폴더 없음 — 건너뜀"; continue }
  Copy-Item -Recurse -Force $src (Join-Path $To $n)
  $tag = if ($Targets -contains $n) { "" } else { " [의존·권장 자동포함]" }
  Write-Host "  ✅ $n ($($Manifest.$n.scope))$tag"
  if ($Manifest.$n.postInstall) { $Posts += "  - ${n}: $($Manifest.$n.postInstall)" }
}
Write-Host "설치 완료 → $To"
if ($Posts.Count -gt 0) { Write-Host "`n▶ 설치 후 꼭 실행할 것 (이 저장소 위치에서):"; $Posts | ForEach-Object { Write-Host $_ } }
