@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo   SigmaVPN - Запуск всех сервисов
echo ========================================
echo.

REM Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не установлен!
    pause
    exit /b 1
)

echo ✓ Python найден

REM Проверка и установка зависимостей
echo.
echo Проверка зависимостей...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Установка Flask...
    pip install flask flask-cors -q
)

REM Создание базы данных если её нет
if not exist "sigmavpn.db" (
    echo.
    echo Создание базы данных...
    python create_database.py
)

REM Запуск API сервера
echo.
echo ========================================
echo Запуск API сервера на порту 5000...
echo ========================================
start "SigmaVPN API" cmd /k python app.py

REM Небольшая задержка
timeout /t 3 /nobreak

REM Запуск веб-сервера
echo.
echo ========================================
echo Запуск веб-сервера на порту 8080...
echo ========================================
start "SigmaVPN Web" cmd /k python -m http.server 8080

echo.
echo ✓ Все сервисы запущены!
echo.
echo 🌐 Веб-сайт: http://localhost:8080
echo 🔌 API: http://localhost:5000
echo.
echo Закройте это окно для остановки.
pause
