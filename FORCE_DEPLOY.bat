@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo 🚀 ФОРСИРОВАННЫЙ ДЕПЛОЙ
echo ========================================
echo.

echo 📝 Форсирую добавление файлов...
git add -f index.html
git add -f style.css
git add -f main.js
git add -f app.py
git add -f Procfile
git add -f requirements.txt

echo 💾 Коммитю...
git commit -m "Force add all necessary files for deployment"

echo 🌐 Пушу...
git push

echo.
echo ✨ ГОТОВО!
echo.
echo Railway перестроится автоматически
echo Сайт: https://sigmaVPNN-production.up.railway.app/
echo.
pause
