@echo off
echo ========================================
echo LinguaMate AI - Git Setup Script
echo ========================================
echo.

echo Checking if Git is installed...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed. Please install Git first.
    echo.
    echo Option 1: Download Git from https://git-scm.com/download/win
    echo Option 2: Use GitHub Desktop from https://desktop.github.com/
    echo.
    pause
    exit /b 1
)

echo Git is installed! Proceeding with setup...
echo.

cd /d "D:\Youlan\eduhacks-ai-fest-2025"

echo Initializing Git repository...
git init

echo Adding all files...
git add .

echo Committing initial version...
git commit -m "Initial commit - LinguaMate AI with custom scenarios and learning levels"

echo Setting main branch...
git branch -M main

echo Adding remote origin...
git remote add origin https://github.com/Crystaria/linguamate-ai.git

echo Pushing to GitHub...
git push -u origin main

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
    echo Please check your GitHub credentials and repository URL
    echo ========================================
)

echo.
pause

