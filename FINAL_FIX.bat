@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo 🚀 ФИНАЛЬНОЕ ИСПРАВЛЕНИЕ
echo ========================================
echo.

echo 📝 Добавляю все файлы...
git add -A

echo 💾 Коммитю...
git commit -m "Minimal working Flask app - serve static files"

echo 🌐 Пушу на GitHub...
git push

echo.
echo ✨ ГОТОВО!
echo.
echo Railway перестроится автоматически (2-3 минуты)
echo Сайт: https://sigmaVPNN-production.up.railway.app/
echo.
pause
