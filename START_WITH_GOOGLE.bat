@echo off
chcp 65001 >nul
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║         🔐 SigmaVPN - Запуск с Google Sign-In 🔐         ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не установлен!
    echo Установите Python с сайта python.org
    pause
    exit /b 1
)

echo ✓ Python найден

REM Установка зависимостей
echo.
echo Проверка Flask...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Установка Flask...
    pip install flask flask-cors requests
)

echo ✓ Flask установлен

REM Создание БД
echo.
echo Создание базы данных...
if not exist "sigmavpn.db" (
    python init_database.py
)

echo ✓ База данных готова

REM Запуск API
echo.
echo ════════════════════════════════════════════════════════════
echo Запуск API сервера на порту 5000...
echo ════════════════════════════════════════════════════════════
echo.

start "API" cmd /k "python app.py"

timeout /t 2 /nobreak

REM Запуск веб-сервера
echo.
echo ════════════════════════════════════════════════════════════
echo Запуск веб-сервера на порту 8080...
echo ════════════════════════════════════════════════════════════
echo.

start "WEB" cmd /k "python -m http.server 8080"

echo.
echo ✓ Оба сервера запущены!
echo.
echo 📋 ВАЖНО: Прежде чем использовать Google Sign-In:
echo.
echo 1. Откройте GOOGLE_SETUP.txt
echo 2. Следуйте инструкциям по получению Google Client ID
echo 3. Обновите Client ID в register.js и login.js
echo.
echo 🌐 Откройте браузер: http://localhost:8080
echo.
pause
