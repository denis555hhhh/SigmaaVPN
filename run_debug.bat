@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

color 0A
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║         🔒 SigmaVPN - Запуск с диагностикой 🔒           ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Проверка Python
echo [1/5] Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не установлен!
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ %PYTHON_VERSION% найден

REM Проверка Flask
echo.
echo [2/5] Проверка Flask...
python -c "import flask; print('Flask версия:', flask.__version__)" >nul 2>&1
if errorlevel 1 (
    echo Установка Flask...
    pip install flask flask-cors -q
    echo ✓ Flask установлен
) else (
    echo ✓ Flask уже установлен
)

REM Создание БД
echo.
echo [3/5] Инициализация базы данных...
if not exist "sigmavpn.db" (
    python init_database.py
) else (
    echo ✓ База данных уже существует
)

REM Проверка портов
echo.
echo [4/5] Проверка портов...
netstat -ano | findstr ":5000" >nul 2>&1
if not errorlevel 1 (
    echo ⚠️  Порт 5000 уже используется!
    echo Закройте другие приложения или используйте другой порт
)

netstat -ano | findstr ":8080" >nul 2>&1
if not errorlevel 1 (
    echo ⚠️  Порт 8080 уже используется!
    echo Закройте другие приложения или используйте другой порт
)

REM Запуск API сервера
echo.
echo [5/5] Запуск сервисов...
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                   Запуск API сервера...                   ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

start "SigmaVPN API Server" cmd /k "title SigmaVPN API Server (порт 5000) & python app.py"

timeout /t 3 /nobreak

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                  Запуск веб-сервера...                    ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

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
echo 🧪 Тестирование API:
echo    python test_api.py
echo.
echo ⚠️  Закройте окна сервисов для остановки системы
echo.
pause
