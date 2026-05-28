@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo 🚀 ФИНАЛЬНЫЙ ДЕПЛОЙ НА RAILWAY
echo ========================================
echo.

echo ✅ Проверка файлов:
if exist app.py echo   ✓ app.py
if exist index.html echo   ✓ index.html
if exist style.css echo   ✓ style.css
if exist main.js echo   ✓ main.js
if exist Procfile echo   ✓ Procfile
if exist requirements.txt echo   ✓ requirements.txt

echo.
echo 📝 Добавляю все файлы в git...
git add -A

echo.
echo 💾 Коммитю изменения...
git commit -m "Final deploy - fix Procfile and ensure all files are included"

echo.
echo 🌐 Пушу на GitHub...
git push

echo.
echo ========================================
echo ✨ ДЕПЛОЙ ЗАВЕРШЕН!
echo ========================================
echo.
echo 🔗 Репозиторий: https://github.com/denis555hhhh/SigmaaVPN
echo 📍 Сайт: https://sigmaVPNN-production.up.railway.app/
echo.
echo ⏱️  Ожидайте 2-3 минуты для завершения развертывания
echo.
pause
