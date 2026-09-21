# Извлекает dbc/maps/gt/cameras/vmaps из локального клиента и заливает их на сервер.
# mmaps генерируются уже на сервере (/opt/asuracore/gen-mmaps.sh): там 16 ядер.
#   powershell -ExecutionPolicy Bypass -File F:\AsuraCORE\tools\extract-local.ps1

$ErrorActionPreference = "Stop"
$root   = Split-Path -Parent $PSScriptRoot
$client = Join-Path $root "client\World of Warcraft"
$tools  = Join-Path $root "tools\extractors"
$out    = Join-Path $root "client\extracted"

New-Item -ItemType Directory -Force $out | Out-Null
Set-Location $out


& "$tools\mapextractor.exe" -i "$client" -o "$out"
if ($LASTEXITCODE -ne 0) { throw "mapextractor failed" }

& "$tools\vmap4extractor.exe" -d "$client"
if ($LASTEXITCODE -ne 0) { throw "vmap4extractor failed" }

New-Item -ItemType Directory -Force vmaps | Out-Null
& "$tools\vmap4assembler.exe" Buildings vmaps
if ($LASTEXITCODE -ne 0) { throw "vmap4assembler failed" }
Remove-Item Buildings -Recurse -Force

# Upload
tar -czf data.tgz dbc maps gt cameras vmaps
scp data.tgz asura:/opt/asuracore/data.tgz
ssh asura "cd /opt/asuracore/data && tar xzf ../data.tgz && rm ../data.tgz && ls"
Remove-Item data.tgz
Write-Host "EXTRACT_UPLOAD_OK"
