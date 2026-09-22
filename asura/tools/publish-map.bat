@echo off
rem AsuraCORE: publish the map edited in Noggit (Asura Sanctum island = plunderisle files, server map 9000)
rem 1) save in Noggit (Ctrl+S)  2) run this  3) restart the game via _retail_\AsuraCORE.bat
cd /d "%~dp0tools\mapkit"
python publish.py "%~dp0tools\noggit\build\bin\RelWithDebInfo\projects" plunderisle 9000 --deploy || goto :fail
ssh asura "systemctl restart asura-worldserver" || goto :fail
echo.
echo Done: client files and server terrain updated, worldserver restarted.
pause
exit /b 0
:fail
echo.
echo FAILED, see messages above.
pause
exit /b 1
