@echo off
echo ========================================================
echo       STARTING ICE PLATFORM SYSTEM SERVICES
echo ========================================================

start "Platform Core API (Port 8000)" cmd /k "cd /d %~dp0server && python -m uvicorn main:app --host 0.0.0.0 --port 8000"
timeout /t 2 >nul

start "Ice Fishing RGS Game Server (Port 8001)" cmd /k "cd /d %~dp0rgs && python -m uvicorn rgs_server:app --host 0.0.0.0 --port 8001"
timeout /t 2 >nul

start "Platform Web Lobby (Port 3000)" cmd /k "cd /d %~dp0client && python -m http.server 3000 --bind 0.0.0.0"

echo Platform started! Open http://localhost:3000 in your browser.
pause
