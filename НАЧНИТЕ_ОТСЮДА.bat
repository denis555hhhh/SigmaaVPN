@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:menu
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo 🚀 SIGMAVPN - РАЗВЕРТЫВАНИЕ НА RAILWAY
echo ════════════════════════════════════════════════════════════════
echo.
echo 📌 ГЛАВНОЕ МЕНЮ:
echo.
echo 1. 📤 Отправить код на GitHub
echo 2. 🔗 Обновить API URLs для Railway
echo 3. 📖 Показать инструкцию
echo 4. ❌ Выход
echo.
set /p choice="Выберите опцию (1-4): "

if "%choice%"=="1" goto github
if "%choice%"=="2" goto update_urls
if "%choice%"=="3" goto instructions
if "%choice%"=="4" goto exit
goto menu

:github
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo 📤 ОТПРАВКА КОДА НА GITHUB
echo ════════════════════════════════════════════════════════════════
echo.

cd /d "c:\Users\Gnida222\Desktop\Сайт впн"

echo 📋 Проверка Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git не установлен!
    pause
    goto menu
)
echo ✅ Git установлен

echo.
echo 📝 Конфигурация Git...
git config --global user.email "test@example.com"
git config --global user.name "SigmaVPN"
echo ✅ Git настроен

echo.
echo 📦 Инициализация репозитория...
if exist .git (
    echo ✓ Репозиторий уже существует
) else (
    git init
    echo ✅ Репозиторий инициализирован
)

echo.
echo 📂 Добавление файлов...
git add .
echo ✅ Файлы добавлены

echo.
echo 💾 Создание коммита...
git commit -m "Initial commit: SigmaVPN website with Railway deployment" 2>nul
if errorlevel 1 (
    echo ℹ️  Коммит уже существует
) else (
    echo ✅ Коммит создан
)

echo.
echo 🔗 Проверка удаленного репозитория...
git remote -v >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠️  ВАЖНО: Удаленный репозиторий не настроен!
    echo.
    echo 📌 Шаги для создания репозитория:
    echo    1. Перейдите на https://github.com/new
    echo    2. Имя: sigma
    echo    3. Выберите Public
    echo    4. Создайте репозиторий
    echo.
    echo 📌 Затем выполните команду:
    echo    git remote add origin https://github.com/ВАШ_ЮЗЕРНЕЙМ/sigma.git
    echo.
    echo Замените ВАШ_ЮЗЕРНЕЙМ на ваше имя пользователя GitHub
    echo.
    pause
    goto menu
)
echo ✅ Удаленный репозиторий настроен

echo.
echo 🚀 Отправка кода на GitHub...
git push -u origin main
if errorlevel 1 (
    echo ❌ Ошибка при отправке!
    pause
    goto menu
)
echo ✅ Код успешно отправлен!

echo.
echo ════════════════════════════════════════════════════════════════
echo ✅ ГОТОВО!
echo ════════════════════════════════════════════════════════════════
echo.
echo 📌 Следующий шаг: Разверните на Railway
echo    1. Перейдите на https://railway.app
echo    2. Нажмите "New Project"
echo    3. Выберите "Deploy from GitHub"
echo    4. Выберите репозиторий "sigma"
echo    5. Нажмите "Deploy"
echo.
pause
goto menu

:update_urls
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo 🔗 ОБНОВЛЕНИЕ API URLs
echo ════════════════════════════════════════════════════════════════
echo.

cd /d "c:\Users\Gnida222\Desktop\Сайт впн"
python update_api_urls.py

pause
goto menu

:instructions
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo 📖 ПОЛНАЯ ИНСТРУКЦИЯ РАЗВЕРТЫВАНИЯ
echo ════════════════════════════════════════════════════════════════
echo.
echo 🎯 ШАГ 1: СОЗДАНИЕ GITHUB РЕПОЗИТОРИЯ
echo ────────────────────────────────────────────────────────────────
echo 1. Перейдите на https://github.com/new
echo 2. Заполните:
echo    - Repository name: sigma
echo    - Description: SigmaVPN website with API
echo    - Выберите: Public
echo 3. Нажмите "Create repository"
echo.
echo 🎯 ШАГ 2: ОТПРАВКА КОДА НА GITHUB
echo ────────────────────────────────────────────────────────────────
echo Выполните команду в Command Prompt:
echo.
echo git remote add origin https://github.com/ВАШ_ЮЗЕРНЕЙМ/sigma.git
echo git branch -M main
echo git push -u origin main
echo.
echo Замените ВАШ_ЮЗЕРНЕЙМ на ваше имя пользователя GitHub
echo.
echo 🎯 ШАГ 3: РАЗВЕРТЫВАНИЕ НА RAILWAY
echo ────────────────────────────────────────────────────────────────
echo 1. Перейдите на https://railway.app
echo 2. Нажмите "New Project"
echo 3. Выберите "Deploy from GitHub"
echo 4. Авторизуйте GitHub (если требуется)
echo 5. Выберите репозиторий "sigma"
echo 6. Нажмите "Deploy"
echo.
echo Railway автоматически:
echo - Установит зависимости из requirements.txt
echo - Запустит приложение через Procfile
echo - Создаст публичный URL
echo.
echo 🎯 ШАГ 4: ПОЛУЧЕНИЕ RAILWAY URL
echo ────────────────────────────────────────────────────────────────
echo После развертывания (2-5 минут):
echo 1. Перейдите на страницу проекта Railway
echo 2. Найдите "Domains"
echo 3. Скопируйте URL (например: https://sigma-production.railway.app)
echo.
echo 🎯 ШАГ 5: ОБНОВЛЕНИЕ API URLs
echo ────────────────────────────────────────────────────────────────
echo Используйте опцию 2 в главном меню для автоматического обновления
echo или отредактируйте вручную:
echo.
echo Файлы: register.js, login.js, checkout.js, cabinet.js
echo Найдите: const API_URL = 'http://localhost:5000'
echo Замените на: const API_URL = 'https://ВАШ_RAILWAY_URL'
echo.
echo 🎯 ШАГ 6: ФИНАЛЬНАЯ ОТПРАВКА
echo ────────────────────────────────────────────────────────────────
echo git add .
echo git commit -m "Update API URLs for Railway"
echo git push origin main
echo.
echo Railway автоматически перестроит приложение!
echo.
echo ════════════════════════════════════════════════════════════════
echo ✅ ГОТОВО! Ваш сайт будет доступен в интернете!
echo ════════════════════════════════════════════════════════════════
echo.
pause
goto menu

:exit
echo.
echo 👋 До свидания!
echo.
exit /b 0
