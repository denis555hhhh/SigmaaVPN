@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

color 0A
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║              🔒 SigmaVPN - Запуск системы 🔒              ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Проверка Python
echo [1/4] Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не установлен!
    echo Пожалуйста, установите Python 3.8+ с сайта python.org
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ %PYTHON_VERSION% найден

REM Проверка и установка зависимостей
echo.
echo [2/4] Проверка зависимостей...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Установка Flask и Flask-CORS...
    pip install flask flask-cors -q
    echo ✓ Зависимости установлены
) else (
    echo ✓ Flask уже установлен
)

REM Создание базы данных если её нет
echo.
echo [3/4] Инициализация базы данных...
if not exist "sigmavpn.db" (
    python init_database.py
) else (
    echo ✓ База данных уже существует
)

REM Запуск сервисов
echo.
echo [4/4] Запуск сервисов...
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                   Запуск сервисов...                      ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Запуск API сервера в отдельном окне
start "SigmaVPN API Server" cmd /k "title SigmaVPN API Server (порт 5000) & python app.py"

REM Небольшая задержка для инициализации API
timeout /t 3 /nobreak

REM Запуск веб-сервера в отдельном окне
start "SigmaVPN Web Server" cmd /k "title SigmaVPN Web Server (порт 8080) & python -m http.server 8080"

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                  ✓ Все сервисы запущены!                 ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 🌐 Веб-сайт:        http://localhost:8080
echo 🔌 API Сервер:      http://localhost:5000
echo 📊 База данных:     sigmavpn.db
echo.
echo 📝 Регистрация:     http://localhost:8080/register.html
echo 🔑 Вход:            http://localhost:8080/login.html
echo.
echo ⚠️  Закройте окна сервисов для остановки системы
echo.
pause
