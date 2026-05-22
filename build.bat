@echo off
echo ========================================
echo   RFID管理系统 打包脚本
echo ========================================
echo.

echo 正在安装依赖...
call python.exe -m pip install -r requirements.txt
call python.exe -m pip install pyinstaller openpyxl

echo.
echo 正在打包，请稍候...
echo.

REM 使用PyInstaller打包
REM --onefile: 打包成单个exe文件
REM --windowed: 不显示命令行窗口
REM --add-data: 添加模板和静态文件
python.exe -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name "RFID管理系统" ^
    --add-data "templates;templates" ^
    --add-data "models;models" ^
    --add-data "generators;generators" ^
    --add-data "instance;instance" ^
    --hidden-import=flask ^
    --hidden-import=flask_sqlalchemy ^
    --hidden-import=sqlalchemy ^
    --hidden-import=jinja2 ^
    --hidden-import=werkzeug ^
    --hidden-import=openpyxl ^
    --hidden-import=click ^
    --hidden-import=blinker ^
    --hidden-import=itsdangerous ^
    --hidden-import=markupsafe ^
    app.py

echo.
echo ========================================
echo   打包完成！
echo   输出目录: dist\RFID管理系统.exe
echo ========================================
pause