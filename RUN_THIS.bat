@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo 🚀 SIGMAVPN DEPLOYMENT - ПРАВИЛЬНЫЙ СКРИПТ
echo ============================================================
echo.

cd /d "c:\Users\Gnida222\Desktop\Сайт впн"

echo 🔧 Шаг 1: Удаляю старый Git...
rmdir /s /q .git 2>nul
echo ✅ Готово

echo.
echo 🔧 Шаг 2: Создаю новый Git...
git init
echo ✅ Готово

echo.
echo 🔧 Шаг 3: Добавляю все файлы...
git add .
echo ✅ Готово

echo.
echo 🔧 Шаг 4: Создаю коммит...
git config user.email "test@example.com"
git config user.name "SigmaVPN"
git commit -m "Initial commit with all files"
echo ✅ Готово

echo.
echo 🔧 Шаг 5: Добавляю GitHub...
git remote add origin https://github.com/deni555hhhh/SigmaVPN.git
echo ✅ Готово

echo.
echo 🔧 Шаг 6: Переименовываю ветку...
git branch -M main
echo ✅ Готово

echo.
echo 🔧 Шаг 7: Отправляю на GitHub...
echo ⚠️  Введите учетные данные:
echo    Username: deni555hhhh
echo    Password: Ваш Personal Access Token
echo.
git push -u origin main --force

echo.
echo ============================================================
echo ✅ ГОТОВО!
echo ============================================================
echo.
echo 📋 Дальше:
echo 1. Откройте https://railway.app
echo 2. Создайте новый проект
echo 3. Выберите deni555hhhh/SigmaVPN
echo 4. Нажмите Deploy
echo 5. Ждите 2-5 минут
echo.
pause
