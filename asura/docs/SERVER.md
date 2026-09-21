# Сервер AsuraCORE

| | |
|---|---|
| Хост | `193.124.184.192` (Ubuntu 22.04, 16 ядер, 62 ГБ RAM) |
| SSH | `ssh asura` (ключ `~/.ssh/asura_srv`, алиас в `~/.ssh/config`) |
| Клиент | 12.1.0.69875 (Midnight) |
| БД | MySQL 8.0: базы `auth`, `characters`, `world`, `hotfixes`, пользователь `asura`, пароль в `/root/.asuracore_dbpass` |

> ⚠ **SSD сервера деградирует** (SMART: переназначенные сектора, битые файлы уже находились).
> Держи код в git, а БД бэкапь (`/opt/asuracore/backup.sh`). Лучше попросить хостера заменить диск.

## Раскладка
```
/opt/asuracore/
  src/        клон github.com/AsuraCORE/AsuraCORE (ветка master)
  build/      CMake/Ninja build
  server/     установка: bin/ (bnetserver, worldserver, extractors), etc/ (*.conf)
  data/       dbc, maps, vmaps, mmaps, gt, cameras (извлекаются из клиента)
  client/     сюда заливается клиент для извлечения карт
  db/         TDB_full_*.sql
  build.sh    сборка:      /opt/asuracore/build.sh > /opt/asuracore/build.log
  update.sh   git pull + сборка + рестарт
  extract.sh  извлечение данных из клиента
  backup.sh   дамп баз в /opt/asuracore/backups
```

## Порты (открыты в ufw)
| Порт | Что |
|---|---|
| 1119 | bnetserver (логин Battle.net) |
| 8081 | bnetserver REST (логин клиента) |
| 8085 | worldserver |
| 8086 | instance server |

## Управление
```bash
systemctl start|stop|restart asura-bnetserver asura-worldserver
systemctl status asura-worldserver
screen -r worldserver        # консоль сервера (выйти не останавливая: Ctrl+A, D)
tail -f /opt/asuracore/server/bin/Server.log
```

### Создать аккаунт (в консоли worldserver)
```
bnetaccount create me@asura.local ПАРОЛЬ
account set gmlevel 1#1 3 -1       # GM-права на 1-й игровой аккаунт
```
В клиенте логин — это email (`me@asura.local`).

## Сборка / обновление
```bash
/opt/asuracore/update.sh      # pull из GitHub → сборка → install → рестарт
```
Первая сборка идёт ~30 мин, повторные быстрее: ccache + Ninja пересобирают только изменённое.

## Извлечение данных (один раз, и после смены билда клиента)
1. Залей клиент (папку, в которой лежат `.build.info` и `Data/`) на сервер:
   ```powershell
   scp -r "F:\AsuraCORE\client\World of Warcraft\*" asura:/opt/asuracore/client/
   ```
   (~100 ГБ; удобнее через WinSCP/rsync. Нужны только `.build.info`, `Data/`, `_retail_/`.)
2. `ssh asura /opt/asuracore/extract.sh`: сначала maps/dbc за минуты, потом mmaps за 1–3 часа.
3. `systemctl restart asura-worldserver`

## Обновление с upstream TrinityCore
```bash
# локально в F:\AsuraCORE\core
git remote add upstream https://github.com/TrinityCore/TrinityCore.git   # один раз
git fetch upstream && git merge upstream/master && git push
```
⚠ Если upstream перешёл на новый билд клиента, клиент тоже придётся обновить. Мерджи осознанно.
