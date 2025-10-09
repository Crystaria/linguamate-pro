@echo off
echo ========================================
echo Tesseract OCR 安装助手
echo ========================================
echo.

REM 检查PowerShell是否可用
powershell -Command "Get-Host" >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: PowerShell 不可用
    echo 请使用管理员权限运行此脚本
    pause
    exit /b 1
)

REM 运行PowerShell安装脚本
echo 正在启动安装程序...
powershell -ExecutionPolicy Bypass -File "scripts\install_tesseract.ps1"

echo.
echo 安装完成！按任意键退出...
pause >nul
