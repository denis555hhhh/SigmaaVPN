@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║          🔒 SigmaVPN - Админ Панель Базы Данных              ║
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
echo 🚀 Запуск админ-панели...
echo.

python db_launcher.py

pause
