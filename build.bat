@echo off
setlocal enabledelayedexpansion

REM --------------------------
REM 配置区（根据项目修改）
REM --------------------------
set SCRIPT=src\main.py
set NAME=最省钱强化方案
set ICON=assets\Akashi.ico
set DATA_DIR=data
set README=README.md
set HIDDEN_IMPORTS=openpyxl

REM --------------------------
REM 自动生成版本号
REM --------------------------
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "datetime=%%a"
set "VER=%datetime:~0,8%_%datetime:~8,4%"
set OUTPUT=dist\%NAME%_v%VER%

REM --------------------------
REM 清理旧文件
REM --------------------------
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
del /q *.spec 2>nul

REM --------------------------
REM 执行打包命令
REM --------------------------
echo 正在打包应用...
pyinstaller --noconfirm ^
    --name "%NAME%" ^
    --icon "%ICON%" ^
    --add-data "%DATA_DIR%\*.xlsx;%DATA_DIR%" ^
    --add-data "%README%;." ^
    --hidden-import %HIDDEN_IMPORTS% ^
    --onefile ^
    --clean ^
    --distpath "%OUTPUT%" ^
    "%SCRIPT%" 1>build.log 2>&1

REM --------------------------
REM 检查是否成功
REM --------------------------
if %errorlevel% neq 0 (
    echo 打包失败！错误日志已保存到 build.log
    pause
    exit /b 1
)

REM --------------------------
REM 打开输出目录
REM --------------------------
if exist "%OUTPUT%" explorer "%OUTPUT%"
echo 打包成功！输出目录：%OUTPUT%
pause