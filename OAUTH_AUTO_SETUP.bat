@echo off
chcp 65001 >nul
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║         🔐 АВТОМАТИЧЕСКАЯ НАСТРОЙКА GOOGLE OAUTH 🔐      ║
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
echo.

REM Запуск setup_oauth.py
echo ════════════════════════════════════════════════════════════
echo Запуск автоматической настройки OAuth...
echo ════════════════════════════════════════════════════════════
echo.

python setup_oauth.py

if errorlevel 1 (
    echo.
    echo ❌ Ошибка при настройке OAuth
    pause
    exit /b 1
)

echo.
echo ════════════════════════════════════════════════════════════
echo ✅ НАСТРОЙКА ЗАВЕРШЕНА!
echo ════════════════════════════════════════════════════════════
echo.
echo Следующие шаги:
echo 1. Запустите: START_WITH_GOOGLE.bat
echo 2. Откройте: http://localhost:8080/register.html
echo 3. Нажмите: "Войти через Google"
echo.
pause
