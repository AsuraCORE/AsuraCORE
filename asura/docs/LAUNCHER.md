# AsuraCORE Launcher

Форк Burralis/Arctium Game Launcher (MIT): https://github.com/AsuraCORE/AsuraLauncher
- `src\`: исходники (git), `bin\AsuraCORE Launcher.exe`: готовая сборка.
- По умолчанию подключается к `193.124.184.192` (`src/src/Constants/Asura.cs`), другой адрес задаётся через `--portal host`.
- Сам создаёт `WTF\Config.wtf`, если его нет.

## Сборка (на сервере, .NET 10 уже стоит)
```bash
cd /opt/asuracore/tools/launcher/src/src   # предварительно залить свежие исходники
dotnet publish -r win-x64 -c Release -p:Platform=x64 --self-contained -p:PublishSingleFile=true -o ../../out
```
Потом `scp "asura:/opt/asuracore/tools/launcher/out/AsuraCORE Launcher.exe" F:\AsuraCORE\tools\launcher\bin\`

## Ограничения (важно)
1. **TLS.** Логин-сервер должен отдавать доверенный сертификат (Let's Encrypt) на тот адрес, что указан в portal.
   Самоподписанный сертификат TrinityCore не подойдёт.
2. **Своих файлов пока нет.** В open-source версии нет загрузчика модов.
   Старая реализация (`ModLoader.cs`, хук функции загрузки файла по сигнатуре) есть в
   github.com/brian8544/Arctium-Launcher. Чтобы перенести её на 12.1.0, нужно заново найти сигнатуру
   `CustomFileIdHook` в Wow.exe 12.1.0.69875 (IDA/Ghidra). Это следующий этап.
   Формат маппингов тот же: `custom\mappings\*.txt` со строками `fileId;path`, файлы в `custom\files\`.
3. Официально лаунчер проверен на ретейле до 12.0.5. Патчи в нём идут по сигнатурам, так что на 12.1.0
   он, скорее всего, заработает, но проверить можно только с клиентом.

## Пакет для игроков
`powershell -ExecutionPolicy Bypass -File F:\AsuraCORE\tools\pack-client.ps1` создаёт `dist\AsuraCORE-client-*.zip`
(лаунчер, Config.wtf и содержимое `custom\`).
