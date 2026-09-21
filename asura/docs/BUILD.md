# Сборка

## На сервере (основной вариант)
Всё уже установлено: GCC 13, CMake 4, Ninja, ccache, Boost 1.74, OpenSSL 3, MySQL 8.

```bash
ssh asura
/opt/asuracore/build.sh > /opt/asuracore/build.log 2>&1   # только сборка
/opt/asuracore/update.sh                                  # pull + сборка + рестарт
```
Параметры CMake (см. `/opt/asuracore/build.sh`):
`-DCMAKE_BUILD_TYPE=RelWithDebInfo -DTOOLS=1 -DSCRIPTS=static`, установка в `/opt/asuracore/server`.

Если меняешь только скрипты (боссы, подземелья), удобнее собирать с `-DSCRIPTS=dynamic`:
тогда скрипты перезагружаются без рестарта (`.reload scripts`, а при `Scripts.AutoReload` в worldserver.conf автоматически).

## На Windows (если хочется локально дебажить)
1. Visual Studio 2022 (workload «Desktop development with C++»), CMake ≥ 3.24, Git.
2. Boost ≥ 1.78 (prebuilt msvc-14.3 64-bit), затем задать переменную `BOOST_ROOT`.
3. OpenSSL 3.x Win64 (полный, не Light) и MySQL Server 8.x.
4. ```powershell
   cmake -S F:\AsuraCORE\core -B F:\AsuraCORE\build -G "Visual Studio 17 2022" -A x64 -DTOOLS=1 -DSCRIPTS=dynamic
   cmake --build F:\AsuraCORE\build --config RelWithDebInfo
   ```
Подробности: https://trinitycore.info/install/Core-Installation/windows-core-installation
