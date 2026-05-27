@echo off
chcp 65001 >nul
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║         🔐 ПОЛНАЯ АВТОМАТИЧЕСКАЯ НАСТРОЙКА OAUTH 🔐      ║
echo ║                                                            ║
echo ║                    Я делаю это за вас!                    ║
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

REM Запуск AUTO_OAUTH_COMPLETE.py
python AUTO_OAUTH_COMPLETE.py

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
