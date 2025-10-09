@echo off
echo ========================================
echo LinguaMate AI - GitHub Upload Script
echo ========================================
echo.

echo Trying to find Git installation...

REM Try common Git installation paths
set "GIT_PATH="

if exist "C:\Program Files\Git\bin\git.exe" (
    set "GIT_PATH=C:\Program Files\Git\bin\git.exe"
    echo Found Git at: %GIT_PATH%
) else if exist "C:\Program Files (x86)\Git\bin\git.exe" (
    set "GIT_PATH=C:\Program Files (x86)\Git\bin\git.exe"
    echo Found Git at: %GIT_PATH%
) else if exist "%USERPROFILE%\AppData\Local\Programs\Git\bin\git.exe" (
    set "GIT_PATH=%USERPROFILE%\AppData\Local\Programs\Git\bin\git.exe"
    echo Found Git at: %GIT_PATH%
) else (
    echo Git not found in common locations.
    echo Please install Git for Windows from: https://git-scm.com/download/win
    echo Make sure to select "Add Git to PATH" during installation.
    pause
    exit /b 1
)

echo.
echo Git found! Proceeding with upload...
echo.

REM Change to project directory
cd /d "D:\Youlan\eduhacks-ai-fest-2025"

echo Initializing Git repository...
"%GIT_PATH%" init

echo Adding all files...
"%GIT_PATH%" add .

echo Committing initial version...
"%GIT_PATH%" commit -m "Initial commit - LinguaMate AI with custom scenarios and learning levels"

echo Setting main branch...
"%GIT_PATH%" branch -M main

echo Adding remote origin...
"%GIT_PATH%" remote add origin https://github.com/Crystaria/linguamate-ai.git

echo Pushing to GitHub...
"%GIT_PATH%" push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS! Code pushed to GitHub
    echo Repository: https://github.com/Crystaria/linguamate-ai
    echo ========================================
) else (
    echo.
    echo ========================================
    echo ERROR: Failed to push to GitHub
    echo This might be due to authentication issues.
    echo Please check:
    echo 1. Your GitHub credentials
    echo 2. Repository URL is correct
    echo 3. Repository exists on GitHub
    echo ========================================
)

echo.
pause

