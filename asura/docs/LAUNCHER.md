# Arctium Game Launcher

Скачать: https://arctium.io/wow/ · исходники: https://github.com/Burralis/Game-Launcher

Бинарники лежат не на GitHub, а на сайте. Кладём их сюда (`tools/launcher/`) и копируем в `World of Warcraft\_retail_\`.

## Свои файлы клиента (custom file loading)
Сборка **ReleaseCustomFiles** подгружает файлы с диска вместо CASC-архивов клиента.

```
_retail_\
  Arctium Game Launcher.exe
  mappings\asura.txt      <- строки вида  fileId;path/to/file.ext
  files\path\to\file.ext  <- сам файл
```

- `fileId` берётся из листфайла: `tools/listfile/community-listfile.csv` (формат `fileId;path`).
- Чтобы **заменить** существующий файл (модель, текстуру), бери его `fileId` из листфайла.
- Чтобы **добавить** новый файл, бери свободный `fileId` за пределами используемых
  (проверяй по `community-listfile.csv`) и ссылайся на него из DB2 или hotfix-ов.

Не используй лаунчер на официальных серверах: за это банят.
