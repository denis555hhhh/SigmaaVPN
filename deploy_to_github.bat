@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ════════════════════════════════════════════════════════════════
echo 🚀 РАЗВЕРТЫВАНИЕ SIGMAVPN НА GITHUB И RAILWAY
echo ════════════════════════════════════════════════════════════════
echo.

REM Переход в папку проекта
cd /d "c:\Users\Gnida222\Desktop\Сайт впн"

REM Проверка Git
echo 📋 Проверка Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git не установлен!
    pause
    exit /b 1
)
echo ✅ Git установлен

REM Конфигурация Git
echo.
echo 📝 Конфигурация Git...
git config --global user.email "test@example.com"
git config --global user.name "SigmaVPN"
echo ✅ Git настроен

REM Инициализация репозитория
echo.
echo 📦 Инициализация Git репозитория...
if exist .git (
    echo ✓ Репозиторий уже существует
) else (
    git init
    echo ✅ Репозиторий инициализирован
)

REM Добавление файлов
echo.
echo 📂 Добавление файлов в Git...
git add .
echo ✅ Файлы добавлены

REM Создание коммита
echo.
echo 💾 Создание коммита...
git commit -m "Initial commit: SigmaVPN website with Railway deployment files" 2>nul
if errorlevel 1 (
    echo ℹ️  Коммит уже существует или нет изменений
) else (
    echo ✅ Коммит создан
)

REM Проверка удаленного репозитория
echo.
echo 🔗 Проверка удаленного репозитория...
git remote -v >nul 2>&1
if errorlevel 1 (
    echo ℹ️  Удаленный репозиторий не настроен
    echo.
    echo ⚠️  ВАЖНО: Вам нужно создать репозиторий на GitHub!
    echo.
    echo 📌 Шаги:
    echo    1. Перейдите на https://github.com/new
    echo    2. Имя репозитория: sigma
    echo    3. Выберите Public
    echo    4. Создайте репозиторий
    echo.
    echo 📌 Затем запустите эту команду:
    echo    git remote add origin https://github.com/ВАШ_ЮЗЕРНЕЙМ/sigma.git
    echo    git branch -M main
    echo    git push -u origin main
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Удаленный репозиторий настроен
)

REM Отправка на GitHub
echo.
echo 🚀 Отправка кода на GitHub...
git push -u origin main
if errorlevel 1 (
    echo ❌ Ошибка при отправке на GitHub
    echo.
    echo 💡 Возможные решения:
    echo    1. Проверьте интернет соединение
    echo    2. Проверьте, что репозиторий создан на GitHub
    echo    3. Проверьте права доступа
    pause
    exit /b 1
) else (
    echo ✅ Код успешно отправлен на GitHub!
)

REM Успешное завершение
echo.
echo ════════════════════════════════════════════════════════════════
echo ✅ ВСЕ ГОТОВО!
echo ════════════════════════════════════════════════════════════════
echo.
echo 📌 Следующие шаги:
echo.
echo 1️⃣  Перейдите на https://railway.app
echo 2️⃣  Нажмите "New Project"
echo 3️⃣  Выберите "Deploy from GitHub"
echo 4️⃣  Выберите репозиторий "sigma"
echo 5️⃣  Нажмите "Deploy"
echo.
echo 6️⃣  После развертывания обновите API URLs в файлах:
echo    - register.js
echo    - login.js
echo    - checkout.js
echo    - cabinet.js
echo.
echo 7️⃣  Замените http://localhost:5000 на ваш Railway URL
echo.
echo 8️⃣  Закоммитьте и отправьте обновления:
echo    git add .
echo    git commit -m "Update API URLs for Railway"
echo    git push origin main
echo.
echo ════════════════════════════════════════════════════════════════
echo.
pause
