@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo 🚀 ПУША В НОВЫЙ РЕПОЗИТОРИЙ
echo ========================================
echo.

echo 📝 Добавляю файлы...
git add -A

echo 💾 Коммитю...
git commit -m "Add index.html, style.css, main.js - working SigmaVPN website"

echo 🌐 Пушу...
git push

echo.
echo ✨ ГОТОВО!
echo.
echo Сайт: https://sigmaavpn-production.up.railway.app/
echo.
pause
