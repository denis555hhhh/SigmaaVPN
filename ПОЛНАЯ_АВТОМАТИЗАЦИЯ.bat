@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:start
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo 🚀 SIGMAVPN - ПОЛНАЯ АВТОМАТИЗАЦИЯ РАЗВЕРТЫВАНИЯ
echo ════════════════════════════════════════════════════════════════
echo.

cd /d "c:\Users\Gnida222\Desktop\Сайт впн"

echo 📋 ПРОВЕРКА ПРЕДВАРИТЕЛЬНЫХ ТРЕБОВАНИЙ...
echo.

REM Проверка Git
echo ⏳ Проверка Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git не установлен!
    echo.
    echo 📌 Установите Git с https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)
echo ✅ Git установлен

REM Проверка Python
echo ⏳ Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Python не установлен (опционально)
)
echo ✅ Python проверен

echo.
echo ════════════════════════════════════════════════════════════════
echo 📝 КОНФИГУРАЦИЯ GIT
echo ════════════════════════════════════════════════════════════════
echo.

echo ⏳ Настройка Git конфигурации...
git config --global user.email "sigmavpn@example.com"
git config --global user.name "SigmaVPN"
echo ✅ Git настроен

echo.
echo ════════════════════════════════════════════════════════════════
echo 📦 ИНИЦИАЛИЗАЦИЯ РЕПОЗИТОРИЯ
echo ════════════════════════════════════════════════════════════════
echo.

if exist .git (
    echo ✓ Репозиторий уже существует
) else (
    echo ⏳ Инициализация Git репозитория...
    git init
    echo ✅ Репозиторий инициализирован
)

echo.
echo ════════════════════════════════════════════════════════════════
echo 🔗 НАСТРОЙКА УДАЛЕННОГО РЕПОЗИТОРИЯ
echo ════════════════════════════════════════════════════════════════
echo.

git remote -v >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Удаленный репозиторий не настроен!
    echo.
    echo 📌 ВАЖНО: Вам нужно создать репозиторий на GitHub
    echo.
    echo 🎯 ШАГИ:
    echo    1. Перейдите на https://github.com/new
    echo    2. Имя репозитория: sigma
    echo    3. Выберите: Public
    echo    4. Нажмите "Create repository"
    echo.
    echo 📌 После создания выполните команду:
    echo    git remote add origin https://github.com/ВАШ_ЮЗЕРНЕЙМ/sigma.git
    echo.
    echo Замените ВАШ_ЮЗЕРНЕЙМ на ваше имя пользователя GitHub
    echo.
    pause
    exit /b 1
)
echo ✅ Удаленный репозиторий настроен

echo.
echo ════════════════════════════════════════════════════════════════
echo 📂 ДОБАВЛЕНИЕ ФАЙЛОВ
echo ════════════════════════════════════════════════════════════════
echo.

echo ⏳ Добавление всех файлов...
git add .
echo ✅ Файлы добавлены

echo.
echo ════════════════════════════════════════════════════════════════
echo 💾 СОЗДАНИЕ КОММИТА
echo ════════════════════════════════════════════════════════════════
echo.

echo ⏳ Создание коммита...
git commit -m "Initial commit: SigmaVPN website with Railway deployment" 2>nul
if errorlevel 1 (
    echo ℹ️  Коммит уже существует (файлы не изменились)
) else (
    echo ✅ Коммит создан
)

echo.
echo ════════════════════════════════════════════════════════════════
echo 🌿 ПЕРЕИМЕНОВАНИЕ ВЕТКИ
echo ════════════════════════════════════════════════════════════════
echo.

echo ⏳ Переименование ветки на main...
git branch -M main
echo ✅ Ветка переименована

echo.
echo ════════════════════════════════════════════════════════════════
echo 🚀 ОТПРАВКА КОДА НА GITHUB
echo ════════════════════════════════════════════════════════════════
echo.

echo ⏳ Отправка кода на GitHub...
echo.
echo 📌 Если будет запрошена аутентификация:
echo    - Username: ваше имя пользователя GitHub
echo    - Password: ваш личный токен доступа
echo.
echo 💡 Как создать токен:
echo    1. Перейдите на https://github.com/settings/tokens
echo    2. Нажмите "Generate new token"
echo    3. Выберите scopes: repo, workflow
echo    4. Скопируйте токен и используйте как пароль
echo.

git push -u origin main
if errorlevel 1 (
    echo ❌ Ошибка при отправке!
    echo.
    echo 📌 Возможные причины:
    echo    1. Неправильные учетные данные GitHub
    echo    2. Удаленный репозиторий не настроен
    echo    3. Нет интернета
    echo.
    pause
    exit /b 1
)
echo ✅ Код успешно отправлен на GitHub!

echo.
echo ════════════════════════════════════════════════════════════════
echo 🎉 ЭТАП 1 ЗАВЕРШЕН!
echo ════════════════════════════════════════════════════════════════
echo.
echo ✅ Ваш код загружен на GitHub!
echo.
echo 📌 СЛЕДУЮЩИЙ ШАГ: Развертывание на Railway
echo.
echo 🎯 ИНСТРУКЦИИ:
echo    1. Перейдите на https://railway.app
echo    2. Нажмите "New Project"
echo    3. Выберите "Deploy from GitHub"
echo    4. Авторизуйте GitHub (если требуется)
echo    5. Выберите репозиторий "sigma"
echo    6. Нажмите "Deploy"
echo.
echo ⏱️  Ожидание развертывания: 2-5 минут
echo.
echo 📌 После развертывания:
echo    1. Скопируйте Railway URL (например: https://sigma-production.railway.app)
echo    2. Запустите этот батник еще раз
echo    3. Выберите опцию для обновления API URLs
echo.
pause

:menu
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo 🚀 SIGMAVPN - СЛЕДУЮЩИЕ ШАГИ
echo ════════════════════════════════════════════════════════════════
echo.
echo 📌 ГЛАВНОЕ МЕНЮ:
echo.
echo 1. 🔗 Обновить API URLs для Railway
echo 2. 📖 Показать инструкцию
echo 3. 🔄 Отправить обновления на GitHub
echo 4. ❌ Выход
echo.
set /p choice="Выберите опцию (1-4): "

if "%choice%"=="1" goto update_urls
if "%choice%"=="2" goto instructions
if "%choice%"=="3" goto push_updates
if "%choice%"=="4" goto exit
goto menu

:update_urls
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo 🔗 ОБНОВЛЕНИЕ API URLs
echo ════════════════════════════════════════════════════════════════
echo.

if exist update_api_urls.py (
    python update_api_urls.py
) else (
    echo ⚠️  Скрипт update_api_urls.py не найден!
    echo.
    echo 📌 Обновите API URLs вручную:
    echo.
    echo Файлы для редактирования:
    echo - register.js
    echo - login.js
    echo - checkout.js
    echo - cabinet.js
    echo.
    echo Найдите строку:
    echo const API_URL = 'http://localhost:5000'
    echo.
    echo Замените на:
    echo const API_URL = 'https://ВАШ_RAILWAY_URL'
    echo.
)

pause
goto menu

:push_updates
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo 🔄 ОТПРАВКА ОБНОВЛЕНИЙ НА GITHUB
echo ════════════════════════════════════════════════════════════════
echo.

echo ⏳ Добавление файлов...
git add .

echo ⏳ Создание коммита...
git commit -m "Update API URLs for Railway deployment" 2>nul
if errorlevel 1 (
    echo ℹ️  Нет изменений для коммита
) else (
    echo ✅ Коммит создан
)

echo ⏳ Отправка на GitHub...
git push origin main
if errorlevel 1 (
    echo ❌ Ошибка при отправке!
) else (
    echo ✅ Обновления отправлены!
    echo.
    echo 📌 Railway автоматически перестроит приложение!
)

pause
goto menu

:instructions
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo 📖 ПОЛНАЯ ИНСТРУКЦИЯ
echo ════════════════════════════════════════════════════════════════
echo.
echo 🎯 ШАГ 1: GITHUB РЕПОЗИТОРИЙ
echo ────────────────────────────────────────────────────────────────
echo 1. Перейдите на https://github.com/new
echo 2. Имя: sigma
echo 3. Выберите: Public
echo 4. Нажмите "Create repository"
echo.
echo 🎯 ШАГ 2: RAILWAY РАЗВЕРТЫВАНИЕ
echo ────────────────────────────────────────────────────────────────
echo 1. Перейдите на https://railway.app
echo 2. Нажмите "New Project"
echo 3. Выберите "Deploy from GitHub"
echo 4. Выберите репозиторий "sigma"
echo 5. Нажмите "Deploy"
echo 6. Ожидайте 2-5 минут
echo.
echo 🎯 ШАГ 3: ПОЛУЧЕНИЕ RAILWAY URL
echo ────────────────────────────────────────────────────────────────
echo 1. После развертывания перейдите на страницу проекта
echo 2. Найдите "Domains"
echo 3. Скопируйте URL (например: https://sigma-production.railway.app)
echo.
echo 🎯 ШАГ 4: ОБНОВЛЕНИЕ API URLs
echo ────────────────────────────────────────────────────────────────
echo Используйте опцию 1 в меню для автоматического обновления
echo или отредактируйте вручную:
echo.
echo Файлы: register.js, login.js, checkout.js, cabinet.js
echo Найдите: const API_URL = 'http://localhost:5000'
echo Замените на: const API_URL = 'https://ВАШ_RAILWAY_URL'
echo.
echo 🎯 ШАГ 5: ФИНАЛЬНАЯ ОТПРАВКА
echo ────────────────────────────────────────────────────────────────
echo Используйте опцию 3 в меню для отправки обновлений
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
