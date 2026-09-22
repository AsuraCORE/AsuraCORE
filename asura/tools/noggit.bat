@echo off
rem AsuraCORE: map editor (Noggit, retail 12.1). Loading the client takes about a minute.
cd /d "%~dp0tools\noggit\build\bin\RelWithDebInfo"
echo Starting Noggit, the window appears after the client is loaded (~1 min)...
noggit.exe
echo.
echo Noggit exited with code %errorlevel%
pause
