@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo 🚀 ИСПРАВЛЕНИЕ И ДЕПЛОЙ
echo ========================================
echo.

echo 📝 Добавляю файлы...
git add Procfile app.py

echo 💾 Коммитю...
git commit -m "Fix Procfile - use gunicorn for Railway"

echo 🌐 Пушу...
git push

echo.
echo ✨ ГОТОВО!
echo.
echo Railway перестроится автоматически (2-3 минуты)
echo Сайт: https://sigmaVPNN-production.up.railway.app/
echo.
pause
