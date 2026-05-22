@echo off

echo Restarting Flask Server...
echo.

:: Stop current server
echo Stopping current server...
call stop_server.bat

:: Wait for 2 seconds
echo Waiting for server to stop completely...
timeout /t 2 /nobreak >nul

echo.
:: Start new server
echo Starting new server...
call start_server.bat

pause