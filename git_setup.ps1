# LinguaMate AI - Git Setup Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "LinguaMate AI - Git Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
Write-Host "Checking if Git is installed..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "Git is not installed. Please install Git first." -ForegroundColor Red
    Write-Host ""
    Write-Host "Option 1: Download Git from https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "Option 2: Use GitHub Desktop from https://desktop.github.com/" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Git is installed! Proceeding with setup..." -ForegroundColor Green
Write-Host ""

# Change to project directory
Set-Location "D:\Youlan\eduhacks-ai-fest-2025"

# Initialize Git repository
Write-Host "Initializing Git repository..." -ForegroundColor Yellow
git init

# Add all files
Write-Host "Adding all files..." -ForegroundColor Yellow
git add .

# Commit initial version
Write-Host "Committing initial version..." -ForegroundColor Yellow
git commit -m "Initial commit - LinguaMate AI with custom scenarios and learning levels"

# Set main branch
Write-Host "Setting main branch..." -ForegroundColor Yellow
git branch -M main

# Add remote origin
Write-Host "Adding remote origin..." -ForegroundColor Yellow
git remote add origin https://github.com/Crystaria/linguamate-ai.git

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
$pushResult = git push -u origin main 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "SUCCESS! Code pushed to GitHub" -ForegroundColor Green
    Write-Host "Repository: https://github.com/Crystaria/linguamate-ai" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "ERROR: Failed to push to GitHub" -ForegroundColor Red
    Write-Host "Error details:" -ForegroundColor Yellow
    Write-Host $pushResult -ForegroundColor Red
    Write-Host ""
    Write-Host "Possible solutions:" -ForegroundColor Yellow
    Write-Host "1. Check your GitHub credentials" -ForegroundColor White
    Write-Host "2. Verify the repository URL is correct" -ForegroundColor White
    Write-Host "3. Make sure the repository exists on GitHub" -ForegroundColor White
    Write-Host "4. Try using GitHub Desktop instead" -ForegroundColor White
    Write-Host "========================================" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"

