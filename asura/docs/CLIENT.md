# Клиент WoW для AsuraCORE

Ядро собрано под **ретейл-клиент 12.1.0.69875** (Midnight).
Билд должен совпадать **точно**: клиент другого билда к серверу не подключится.

## 1. Получить клиент
1. Поставь Battle.net и установи World of Warcraft (Retail) в эту папку
   (`F:\AsuraCORE\client\World of Warcraft\`).
2. Проверь билд: `World of Warcraft\.build.info` → строка с `12.1.0.69875`.
   - Если Blizzard уже выпустила патч новее, придётся либо обновить ядро
     (`git merge upstream/master`, когда TrinityCore перейдёт на новый билд),
     либо скачать нужный билд через CDN-настройки лаунчера Arctium (см. `tools/launcher`).
3. Аккаунт Blizzard нужен только для скачивания, играть на своём сервере он не нужен.

## 2. Лаунчер (подключение к нашему серверу)
Официальный `Wow.exe` ходит на серверы Blizzard. Для своего сервера нужен
**Arctium Game Launcher**: https://arctium.io/wow/ (исходники: github.com/Burralis/Game-Launcher)

- Положи `Arctium Game Launcher.exe` в `World of Warcraft\_retail_\`.
- В `_retail_\WTF\Config.wtf` пропиши:
  ```
  SET portal "193.124.184.192"
  ```
- Запускай игру через Arctium, а не через Battle.net.
- Для своих файлов (модели, текстуры, карты) используется сборка `ReleaseCustomFiles`, см. `tools/launcher/README.md`.

## 3. Извлечение карт для сервера (maps / vmaps / mmaps / dbc)
Серверу нужны данные, извлечённые из клиента. Инструменты уже собраны на сервере
(`/opt/asuracore/server/bin/`). Пошагово это описано в `docs/SERVER.md` → «Извлечение данных».

Коротко: заливаешь клиент на сервер в `/opt/asuracore/client`, запускаешь
`/opt/asuracore/extract.sh`, и в `/opt/asuracore/data` появляются `dbc`, `maps`, `vmaps`, `mmaps`, `gt`, `cameras`.

> Папка `World of Warcraft\` в git не попадает (она весит 100+ ГБ).
