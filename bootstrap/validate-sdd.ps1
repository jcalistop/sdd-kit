# Valida coherencia documental de una instancia SDD.
# Uso: .\sdd-kit\bootstrap\validate-sdd.ps1 [-SddPath ".github/docs/sdd"]

param(
    [string]$SddPath = ".github/docs/sdd"
)

$ErrorActionPreference = "Continue"
$errors = 0
$warnings = 0

function Write-Err($msg) { Write-Host "ERROR: $msg" -ForegroundColor Red; $script:errors++ }
function Write-Warn($msg) { Write-Host "WARN:  $msg" -ForegroundColor Yellow; $script:warnings++ }
function Write-Ok($msg) { Write-Host "OK:    $msg" -ForegroundColor Green }

if (-not (Test-Path $SddPath)) {
    Write-Err "No existe el directorio SDD: $SddPath"
    exit 1
}

$backlogPath = Join-Path $SddPath "BACKLOG.md"
if (-not (Test-Path $backlogPath)) {
    Write-Err "Falta BACKLOG.md en $SddPath"
    exit 1
}

$backlogLines = Get-Content $backlogPath -Encoding UTF8
$backlogIds = @{}
$backlogSection = @{}
$currentSection = ""

foreach ($line in $backlogLines) {
    if ($line -match '^##\s+(Discovery|Draft|Ready|In Build|Validating|Released|Descartado)') {
        $currentSection = $Matches[1]
        continue
    }
    if ($line -notmatch '^\|') { continue }
    if ($line -match '^\|\s*[-:]') { continue }
    $cols = ($line.Trim('|').Split('|') | ForEach-Object { $_.Trim() })
    if ($cols.Count -lt 1) { continue }
    if ($cols[0] -notmatch '^(SDD-\d+[a-z]?)$') { continue }
    $id = $Matches[1]
    if ($backlogIds.ContainsKey($id) -and $backlogIds[$id] -ne $currentSection) {
        Write-Err "ID $id duplicado en BACKLOG (secciones: $($backlogIds[$id]) y $currentSection)"
    } else {
        $backlogIds[$id] = $currentSection
        $backlogSection[$id] = $currentSection
    }
}

$fileIds = @{}
$seenFiles = @{}

$specDirs = @(
    (Join-Path $SddPath "specs"),
    (Join-Path $SddPath "archive")
)

foreach ($dir in $specDirs) {
    if (-not (Test-Path $dir)) { continue }
    Get-ChildItem -Path $dir -Recurse -Filter "SDD-*.md" -File | ForEach-Object {
        if ($_.Name -match '^(SDD-\d+[a-z]?)') {
            $id = $Matches[1]
            $loc = if ($_.FullName -match [regex]::Escape("\specs\")) { "specs" } else { "archive" }
            if ($seenFiles.ContainsKey($id)) {
                Write-Err "ID $id aparece en mas de un archivo"
            }
            $seenFiles[$id] = $_.FullName
            $fileIds[$id] = $loc
        }
    }
}

foreach ($id in $fileIds.Keys) {
    $loc = $fileIds[$id]
    if ($loc -eq "specs") {
        if (-not $backlogIds.ContainsKey($id)) {
            Write-Err "Spec $id en specs/ sin entrada en BACKLOG.md"
        } elseif ($backlogSection[$id] -eq "Released") {
            Write-Err "Spec $id en specs/ pero BACKLOG dice Released (debe estar en archive/)"
        } elseif ($backlogSection[$id] -eq "Discovery") {
            Write-Warn "Spec $id en specs/ pero BACKLOG aun en Discovery (esperado Draft+)"
        } else {
            Write-Ok "Spec activo $id coherente con BACKLOG ($($backlogSection[$id]))"
        }
    }
    if ($loc -eq "archive") {
        if (-not $backlogIds.ContainsKey($id)) {
            Write-Err "Spec archivado $id sin entrada en BACKLOG.md"
        } elseif ($backlogSection[$id] -ne "Released") {
            Write-Err "Spec $id en archive/ pero BACKLOG no esta en Released (esta en $($backlogSection[$id]))"
        } else {
            Write-Ok "Spec archivado $id coherente con BACKLOG"
        }
    }
}

$activeSections = @("Draft", "Ready", "In Build", "Validating")
foreach ($id in $backlogIds.Keys) {
    $sec = $backlogSection[$id]
    if ($activeSections -contains $sec) {
        if ($fileIds[$id] -ne "specs") {
            Write-Err "BACKLOG: $id en $sec pero no hay archivo en specs/"
        }
    }
}

$nextLine = $backlogLines | Where-Object { $_ -match 'Pr[oó]ximo ID disponible' } | Select-Object -First 1
if ($nextLine -match 'SDD-(\d+)') {
    $nextNum = [int]$Matches[1]
    $maxNum = 0
    $allIds = @($backlogIds.Keys) + @($fileIds.Keys) | Select-Object -Unique
    foreach ($id in $allIds) {
        if ($id -match 'SDD-(\d+)') {
            $n = [int]$Matches[1]
            if ($n -gt $maxNum) { $maxNum = $n }
        }
    }
    $expected = $maxNum + 1
    if ($nextNum -lt $expected) {
        Write-Warn "Proximo ID SDD-$($nextNum.ToString('000')) parece bajo (max usado: SDD-$($maxNum.ToString('000')))"
    } else {
        Write-Ok "Proximo ID disponible coherente (max usado: SDD-$($maxNum.ToString('000')))"
    }
}

if (-not (Test-Path (Join-Path $SddPath "sdd.config.yaml"))) {
    Write-Warn "Falta sdd.config.yaml"
} else {
    Write-Ok "sdd.config.yaml presente"
}

Write-Host ""
Write-Host "Resumen: $errors error(es), $warnings advertencia(s)"
if ($errors -gt 0) { exit 1 }
exit 0
