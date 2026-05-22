@echo off

echo Stopping Flask Server...
echo.

:: Find and kill Python process running Flask application
taskkill /f /im "python.exe" /fi "windowtitle eq *Flask*" 2>nul

:: If above command fails, try alternative method
if %ERRORLEVEL% neq 0 (
    echo Trying alternative method to stop server...
    taskkill /f /im "python.exe" /fi "commandline eq *app.py*" 2>nul
    if %ERRORLEVEL% neq 0 (
        echo Warning: No running Flask server found.
    ) else (
        echo Flask Server stopped successfully.
    )
) else (
    echo Flask Server stopped successfully.
)

echo.
echo Done.

pause