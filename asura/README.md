# AsuraCORE: рабочая папка проекта

Кастомный WoW-сервер на базе **TrinityCore master** (клиент **12.1.0.69875**, Midnight).
Форк: https://github.com/AsuraCORE/AsuraCORE

```
F:\AsuraCORE\
  core\            исходники ядра (git-клон форка); здесь пишем код и отсюда пушим
  client\          сюда ставится клиент WoW       → client/README.md
  tools\
    listfile\      community-listfile.csv: fileId ↔ путь (для маппинга своих файлов)
    WoWDBDefs\     структуры всех DB2-таблиц по билдам
    launcher\      Arctium launcher               → tools/launcher/README.md
  docs\
    SERVER.md      сервер: раскладка, запуск, аккаунты, извлечение карт
    BUILD.md       как собирать (сервер и Windows)
    CUSTOM.md      как делать свой контент
```

## Цикл работы
1. Правишь код в `core\`, делаешь `git commit` и `git push`.
2. `ssh asura /opt/asuracore/update.sh`: сервер делает pull, пересобирает и перезапускается.
3. Заходишь клиентом через Arctium на `193.124.184.192`.

## Ссылки
- TrinityCore wiki: https://trinitycore.info/
- Форматы файлов: https://wowdev.wiki/
- DB2 и файлы клиента онлайн: https://wago.tools/
- Листфайлы: https://github.com/wowdev/wow-listfile
- Кастом-контент (модели, карты): https://model-changing.net/
