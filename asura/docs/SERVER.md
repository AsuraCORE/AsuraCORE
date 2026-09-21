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
tail -f /opt/asuracore/logs/Server.log
```

### Аккаунты
Админ (GM 3): логин и пароль лежат на сервере в `/root/.asuracore_admin`.

Создать новый (в консоли worldserver):
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
Клиент русский, поэтому в `worldserver.conf` стоит `DBC.Locale = 8` (ruRU), а DBC лежат в `data/dbc/ruRU`.

**Основной способ (с ПК, без заливки клиента):** `powershell -ExecutionPolicy Bypass -File F:\AsuraCORE\tools\extract-local.ps1`
извлекает dbc/maps/vmaps из `client\World of Warcraft` экстракторами из `tools\extractors` (Windows-сборка из CI форка) и заливает на сервер.
Потом на сервере: `/opt/asuracore/gen-mmaps.sh` (1–3 ч), затем `systemctl restart asura-worldserver`.

> Клиент 12.1 хранит файлы в новом формате (TVFS-root). Штатная CascLib его не читает, в форке она пропатчена
> (`asura/casclib-wow-tvfs.patch`, коммит «WoW 12.1 TVFS root support»). Если клиент «неполный» (DB2 не извлекаются),
> сделай в Battle.net «Проверить и восстановить».

**Запасной способ (через сервер):**
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
