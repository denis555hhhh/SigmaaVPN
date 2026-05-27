@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    🔒 SigmaVPN - Запуск                        ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не установлен!
    echo Пожалуйста, установите Python с https://www.python.org
    pause
    exit /b 1
)

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Flask не установлен. Установка...
    pip install flask flask-cors
)

REM Check if database exists
if not exist "sigmavpn.db" (
    echo 📦 Создание базы данных...
    python create_database.py
    if errorlevel 1 (
        echo ❌ Ошибка при создании базы данных!
        pause
        exit /b 1
    )
    echo ✅ База данных создана
)

echo.
echo 🚀 Запуск сервисов...
echo.

REM Start Flask API server in a new window
echo 📍 Запуск Flask API на http://localhost:5000
start "SigmaVPN API Server" cmd /k python app.py

REM Wait for Flask to start
timeout /t 3 /nobreak

REM Start website server in a new window
echo 📍 Запуск веб-сервера на http://localhost:8080
start "SigmaVPN Website" cmd /k python -m http.server 8080

REM Wait for servers to start
timeout /t 2 /nobreak

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    ✅ Все сервисы запущены!                    ║
echo ╠════════════════════════════════════════════════════════════════╣
echo ║                                                                ║
echo ║  🌐 Веб-сайт:     http://localhost:8080                       ║
echo ║  🔌 API:          http://localhost:5000                       ║
echo ║  📊 БД:           sigmavpn.db                                 ║
echo ║                                                                ║
echo ║  Откройте браузер и перейдите на http://localhost:8080        ║
echo ║                                                                ║
echo ║  Для остановки закройте оба окна консоли                      ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

pause
