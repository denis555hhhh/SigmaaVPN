@echo off
title SecureVPN - Локальный сервер
color 0A
echo.
echo  ==========================================
echo   SecureVPN - Запуск локального сервера
echo  ==========================================
echo.
echo  [1/2] Запускаем веб-сервер на порту 8080...
start "Python HTTP Server" cmd /k "python -m http.server 8080"
timeout /t 2 /nobreak >nul

echo  [2/2] Создаём публичный туннель Cloudflare...
echo.
echo  Подождите 5-10 секунд, затем скопируйте ссылку
echo  вида: https://xxxx-xxxx.trycloudflare.com
echo.
echo  ==========================================
echo   ССЫЛКА ПОЯВИТСЯ НИЖЕ:
echo  ==========================================
echo.
cloudflared.exe tunnel --url http://localhost:8080
pause
