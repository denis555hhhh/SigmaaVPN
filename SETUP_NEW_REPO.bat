@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo 🔄 ПОДКЛЮЧЕНИЕ К НОВОМУ РЕПОЗИТОРИЮ
echo ========================================
echo.

echo 📝 Удаляю старый remote...
git remote remove origin
if errorlevel 1 (
    echo ⚠️  Старого remote не было (это нормально)
)

echo.
echo 🔗 Добавляю новый remote...
git remote add origin https://github.com/denis555hhhh/SigmaaVPN.git
if errorlevel 1 (
    echo ❌ Ошибка при добавлении remote
    pause
    exit /b 1
)

echo ✅ Remote добавлен

echo.
echo 📝 Добавляю все файлы...
git add -A

echo.
echo 💾 Коммитю изменения...
git commit -m "Initial commit - SigmaVPN website with Telegram integration"

echo.
echo 🌐 Пушу на новый репозиторий...
git push -u origin main
if errorlevel 1 (
    echo ⚠️  Ошибка при пуше (может быть нужно создать main ветку)
    echo Попробуй: git push -u origin master
    pause
    exit /b 1
)

echo ✅ Запушено на GitHub

echo.
echo ========================================
echo ✨ ГОТОВО!
echo ========================================
echo.
echo 🔗 Репозиторий: https://github.com/denis555hhhh/SigmaaVPN
echo.
pause
