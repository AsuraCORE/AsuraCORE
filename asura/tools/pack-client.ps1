# Собирает пакет AsuraCORE для игроков: dist\AsuraCORE-client-<дата>.zip
# Игрок распаковывает его в папку "World of Warcraft" (ту, где лежит _retail_) и запускает
# "AsuraCORE Launcher.exe".
#
#   powershell -ExecutionPolicy Bypass -File F:\AsuraCORE\tools\pack-client.ps1
#   ... -Portal login.example.com      # другой адрес логин-сервера

param(
    [string]$Portal = "193.124.184.192",
    [string]$Build  = "12.1.0.69875"
)

$ErrorActionPreference = "Stop"
$root    = Split-Path -Parent $PSScriptRoot
$stage   = Join-Path $root "dist\stage"
$retail  = Join-Path $stage "_retail_"
$custom  = Join-Path $root "custom"          # custom\files\..., custom\mappings\*.txt
$launcher = Join-Path $root "tools\launcher\bin\AsuraCORE Launcher.exe"

if (-not (Test-Path $launcher)) { throw "Нет ${launcher}: сначала собери лаунчер (tools\launcher\README.md)" }

Remove-Item $stage -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force (Join-Path $retail "WTF") | Out-Null

Copy-Item $launcher $retail
Set-Content -Encoding ascii (Join-Path $retail "WTF\Config.wtf") "SET portal `"$Portal`""

foreach ($d in "files", "mappings") {
    $src = Join-Path $custom $d
    if (Test-Path $src) { Copy-Item $src (Join-Path $retail $d) -Recurse }
}

Set-Content -Encoding utf8 (Join-Path $stage "README.txt") @"
AsuraCORE: клиент $Build
1. Установи World of Warcraft через Battle.net и отключи в нём автообновление.
2. Распакуй этот архив в папку "World of Warcraft" с заменой файлов.
3. Запускай игру через _retail_\AsuraCORE Launcher.exe.
"@

$zip = Join-Path $root ("dist\AsuraCORE-client-" + (Get-Date -Format "yyyyMMdd-HHmm") + ".zip")
Compress-Archive -Path (Join-Path $stage "*") -DestinationPath $zip -Force
Remove-Item $stage -Recurse -Force
Write-Host "Готово: $zip"
