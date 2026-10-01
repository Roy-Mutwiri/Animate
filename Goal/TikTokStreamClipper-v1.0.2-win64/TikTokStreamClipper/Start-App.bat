@echo off
REM ============================================================
REM  TikTok Stream Clipper - one-click launcher
REM  Double-click this file to open the app in your browser.
REM ============================================================
setlocal
cd /d "%~dp0"

REM --- Build the exe automatically if it isn't here yet ---
if not exist "TikTokStreamClipper.exe" (
    echo TikTokStreamClipper.exe was not found. Building it now...
    echo(
    call "%~dp0Build-App.bat"
)

if not exist "TikTokStreamClipper.exe" (
    echo [ERROR] Could not find or build TikTokStreamClipper.exe.
    pause
    exit /b 1
)

echo(
echo Starting TikTok Stream Clipper...
echo Your browser will open at http://127.0.0.1:8787
echo Keep this window open while you use the app. Close it to stop.
echo(

REM No arguments = launch the web UI and open the browser (see build_exe\launcher.py)
"TikTokStreamClipper.exe"

echo(
echo The app has stopped.
pause
