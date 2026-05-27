@echo off
chcp 65001 >nul
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║           🔧 ИСПРАВЛЕНИЕ ОШИБКИ GOOGLE OAUTH 🔧          ║
echo ║                                                            ║
echo ║              Ошибка: no registered origin                 ║
echo ║              Решение: Получить реальный Client ID         ║
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

REM Запуск FIX_OAUTH_ERROR.py
python FIX_OAUTH_ERROR.py

if errorlevel 1 (
    echo.
    echo ❌ Ошибка при исправлении
    pause
    exit /b 1
)

echo.
echo ════════════════════════════════════════════════════════════
echo ✅ ОШИБКА ИСПРАВЛЕНА!
echo ════════════════════════════════════════════════════════════
echo.
echo Следующие шаги:
echo 1. Закройте браузер
echo 2. Запустите: START_WITH_GOOGLE.bat
echo 3. Откройте: http://localhost:8080/register.html
echo 4. Нажмите: "Войти через Google"
echo.
pause
