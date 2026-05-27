@echo off
chcp 65001 >nul
title SigmaVPN - Запуск приложения
color 0A

echo.
echo  ╔════════════════════════════════════════╗
echo  ║        SigmaVPN Desktop App            ║
echo  ║         Запуск приложения              ║
echo  ╚════════════════════════════════════════╝
echo.

REM Check if exe exists
if not exist "%~dp0dist\SigmaVPN.exe" (
    echo  ❌ Ошибка: Файл SigmaVPN.exe не найден!
    echo.
    echo  Убедитесь что файл находится в папке:
    echo  %~dp0dist\
    echo.
    pause
    exit /b 1
)

echo  ✅ Запуск приложения...
echo.

REM Run the application
start "" "%~dp0dist\SigmaVPN.exe"

REM Wait a moment
timeout /t 2 /nobreak

echo.
echo  ✅ Приложение запущено!
echo.
echo  Если окно не появилось, проверьте:
echo  • Антивирус не блокирует приложение
echo  • На компьютере установлена Windows 7 или новее
echo.
echo  Поддержка: https://t.me/slogg12
echo.

exit /b 0
