@echo off
REM ============================================================
REM  TikTok Stream Clipper - one-click builder
REM  Double-click this file to create TikTokStreamClipper.exe
REM ============================================================
setlocal
cd /d "%~dp0"

echo(
echo === TikTok Stream Clipper - Building the app ===
echo(

REM --- Check Python is installed ---
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not on PATH.
    echo Install Python 3.11+ from https://www.python.org/downloads/
    echo Make sure to tick "Add python.exe to PATH" during setup.
    echo(
    pause
    exit /b 1
)

echo Installing build tools and dependencies (first run may take a few minutes)...
python -m pip install --upgrade pip >nul
python -m pip install pyinstaller >nul
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo(
echo Building TikTokStreamClipper.exe ...
python -m PyInstaller --clean --noconfirm --distpath dist --workpath build_exe\work build_exe\tiktok_poster.spec
if errorlevel 1 (
    echo [ERROR] Build failed. See the messages above.
    pause
    exit /b 1
)

if exist "dist\TikTokStreamClipper.exe" (
    copy /Y "dist\TikTokStreamClipper.exe" "TikTokStreamClipper.exe" >nul
    echo(
    echo === SUCCESS ===
    echo Created: TikTokStreamClipper.exe  (in this folder)
    echo Double-click Start-App.bat to run it.
) else (
    echo [ERROR] Build finished but the exe was not found.
    pause
    exit /b 1
)

echo(
pause
