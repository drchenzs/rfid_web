@echo off
for /f "tokens=*" %%i in ('pip --version 2^>nul') do set "pip_output=%%i"
echo %pip_output%
pause