@echo off
REM ============================================
REM Anime Recommender - Automated Deployment
REM ============================================

setlocal enabledelayedexpansion

echo.
echo ============================================
echo   🎌 ANIME RECOMMENDER DEPLOYMENT SCRIPT
echo ============================================
echo.

REM Check Git
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Git is not installed!
    echo Please download from: https://git-scm.com/
    pause
    exit /b 1
)
echo ✅ Git installed

REM Get GitHub info
echo.
echo Enter your GitHub information:
echo.
set /p GITHUB_USERNAME="GitHub Username (e.g., john-doe): "
set /p GITHUB_TOKEN="GitHub Personal Access Token: "

if "%GITHUB_USERNAME%"=="" (
    echo ❌ ERROR: GitHub username required!
    pause
    exit /b 1
)

echo.
echo ✅ Credentials received
echo.

REM Create GitHub repository URL
set REPO_URL=https://%GITHUB_USERNAME%:%GITHUB_TOKEN%@github.com/%GITHUB_USERNAME%/anime-recommender.git

REM Add remote
echo Connecting to GitHub...
git remote add origin %REPO_URL% 2>nul
if errorlevel 1 (
    echo ℹ️  Remote already exists, updating...
    git remote set-url origin %REPO_URL%
)
echo ✅ Remote configured

REM Push to GitHub
echo.
echo Pushing to GitHub (may take a moment)...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo ❌ ERROR: Failed to push to GitHub!
    echo Please verify your credentials and try again.
    pause
    exit /b 1
)

echo.
echo ✅ Successfully pushed to GitHub!
echo.
echo ============================================
echo   📡 DEPLOYMENT COMPLETE!
echo ============================================
echo.
echo Your repository is now on GitHub:
echo   https://github.com/%GITHUB_USERNAME%/anime-recommender
echo.
echo Next steps:
echo   1. Go to: https://share.streamlit.io/
echo   2. Sign in with GitHub
echo   3. Click "New app"
echo   4. Select: %GITHUB_USERNAME%/anime-recommender
echo   5. Branch: main
echo   6. File: app.py
echo   7. Click Deploy!
echo.
echo Your app will be live at:
echo   https://anime-recommender-xxx.streamlit.app
echo.
echo ============================================
echo.

pause
