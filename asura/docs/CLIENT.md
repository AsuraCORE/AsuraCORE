# Клиент WoW для AsuraCORE

Ядро собрано под **ретейл-клиент 12.1.0.69875** (Midnight).
Билд должен совпадать **точно**: клиент другого билда к серверу не подключится.

## 1. Получить клиент
1. Поставь Battle.net и установи World of Warcraft (Retail) в эту папку
   (`F:\AsuraCORE\client\World of Warcraft\`).
2. Проверь билд: `World of Warcraft\.build.info` → строка с `12.1.0.69875`.
   - Если Blizzard уже выпустила патч новее, придётся либо обновить ядро
     (`git merge upstream/master`, когда TrinityCore перейдёт на новый билд),
     либо скачать нужный билд через CDN-настройки лаунчера Burralis (см. `tools/launcher`).
3. Аккаунт Blizzard нужен только для скачивания, играть на своём сервере он не нужен.

## 2. Лаунчер (подключение к нашему серверу)
Официальный `Wow.exe` ходит на серверы Blizzard. Для своего сервера нужен
**Burralis Game Launcher 1.6.1+** (закрытая сборка): https://burralis.io/downloads/. Open-source версия (наш AsuraLauncher) клиент 12.1 пока не поддерживает

- Положи `Burralis Game Launcher.exe` в `World of Warcraft\_retail_\`.
- В `_retail_\WTF\Config.wtf` пропиши:
  ```
  SET portal "193-124-184-192.sslip.io"
  ```
- Запускай игру через Burralis Game Launcher, а не через Battle.net.
- Свои файлы (модели, текстуры, карты) Burralis тоже умеет подгружать, см. https://burralis.io (раздел Usage).

## 3. Извлечение карт для сервера (maps / vmaps / mmaps / dbc)
Серверу нужны данные, извлечённые из клиента. Инструменты уже собраны на сервере
(`/opt/asuracore/server/bin/`). Пошагово это описано в `docs/SERVER.md` → «Извлечение данных».

Коротко: заливаешь клиент на сервер в `/opt/asuracore/client`, запускаешь
`/opt/asuracore/extract.sh`, и в `/opt/asuracore/data` появляются `dbc`, `maps`, `vmaps`, `mmaps`, `gt`, `cameras`.

> Папка `World of Warcraft\` в git не попадает (она весит 100+ ГБ).
