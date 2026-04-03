# Tesseract OCR 自动安装脚本
# 适用于Windows系统

Write-Host "=== Tesseract OCR 自动安装脚本 ===" -ForegroundColor Green
Write-Host ""

# 检查是否已安装Tesseract
try {
    $version = & tesseract --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Tesseract OCR 已安装: $($version[0])" -ForegroundColor Green
        Write-Host "当前可用语言包:" -ForegroundColor Yellow
        & tesseract --list-langs
        exit 0
    }
} catch {
    Write-Host "Tesseract OCR 未安装，开始安装过程..." -ForegroundColor Yellow
}

# 检查Chocolatey是否已安装
$chocoInstalled = $false
try {
    $chocoVersion = & choco --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Chocolatey 已安装: $chocoVersion" -ForegroundColor Green
        $chocoInstalled = $true
    }
} catch {
    Write-Host "Chocolatey 未安装" -ForegroundColor Yellow
}

# 如果Chocolatey未安装，询问是否安装
if (-not $chocoInstalled) {
    $installChoco = Read-Host "是否安装Chocolatey包管理器？(y/n)"
    if ($installChoco -eq "y" -or $installChoco -eq "Y") {
        Write-Host "正在安装Chocolatey..." -ForegroundColor Yellow
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        
        # 刷新环境变量
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        Write-Host "✓ Chocolatey 安装完成" -ForegroundColor Green
        $chocoInstalled = $true
    }
}

# 使用Chocolatey安装Tesseract
if ($chocoInstalled) {
    Write-Host "正在使用Chocolatey安装Tesseract OCR..." -ForegroundColor Yellow
    & choco install tesseract -y
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Tesseract OCR 安装完成" -ForegroundColor Green
    } else {
        Write-Host "✗ Tesseract OCR 安装失败" -ForegroundColor Red
        Write-Host "请手动安装，参考 TESSERACT_INSTALLATION_GUIDE.md" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "请手动安装Tesseract OCR:" -ForegroundColor Yellow
    Write-Host "1. 访问: https://github.com/UB-Mannheim/tesseract/wiki" -ForegroundColor Cyan
    Write-Host "2. 下载Windows安装包" -ForegroundColor Cyan
    Write-Host "3. 运行安装程序" -ForegroundColor Cyan
    Write-Host "4. 配置环境变量" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "详细说明请查看: TESSERACT_INSTALLATION_GUIDE.md" -ForegroundColor Yellow
    exit 1
}

# 验证安装
Write-Host ""
Write-Host "验证安装..." -ForegroundColor Yellow
try {
    $version = & tesseract --version
    Write-Host "✓ Tesseract OCR 安装成功!" -ForegroundColor Green
    Write-Host "版本: $($version[0])" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "可用语言包:" -ForegroundColor Yellow
    & tesseract --list-langs
    
    Write-Host ""
    Write-Host "=== 安装完成 ===" -ForegroundColor Green
    Write-Host "现在您可以重启Linguamate Pro后端服务器来使用真实的OCR功能!" -ForegroundColor Green
    Write-Host "运行命令: python backend\main_local.py" -ForegroundColor Cyan
    
} catch {
    Write-Host "✗ 验证失败，请检查安装" -ForegroundColor Red
    exit 1
}

