@echo off
REM ============================================================
REM  TikTok Stream Clipper - one-time UPLOAD setup
REM  Installs what the app needs to log in and post to TikTok.
REM  You only need to run this once.
REM ============================================================
setlocal
cd /d "%~dp0"

echo(
echo === One-time setup for TikTok login and uploading ===
echo(

REM --- Python (required for the uploader) ---
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not on PATH.
    echo Install Python 3.11+ from https://www.python.org/downloads/
    echo and tick "Add python.exe to PATH", then run this again.
    echo(
    pause
    exit /b 1
)

echo Installing uploader Python dependencies (this can take a few minutes)...
python -m pip install --upgrade pip >nul
python -m pip install -r external\TiktokAutoUploader\requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install uploader Python dependencies.
    pause
    exit /b 1
)

echo(
echo NOTE: Logging in opens a Chrome window automatically.
echo Make sure Google Chrome is installed: https://www.google.com/chrome/
echo(

REM --- Node.js signature helper (needed to sign uploads) ---
where npm >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Node.js/npm was not found.
    echo Login may work, but POSTING videos needs the signature helper.
    echo Install Node.js LTS from https://nodejs.org/ then run this script again.
    echo(
    pause
    exit /b 0
)

echo Installing the TikTok signature helper (Node.js)...
pushd external\TiktokAutoUploader\tiktok_uploader\tiktok-signature
call npm install
call npx playwright install chromium
popd

echo(
echo === Setup complete ===
echo You can now use "Open TikTok" on the Upload page to log in.
echo(
pause
