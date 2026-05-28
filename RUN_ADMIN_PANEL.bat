@echo off
chcp 65001 >nul
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     🤖 SigmaVPN Bot Admin Panel - Автозапуск              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Проверить, существует ли EXE
if exist "dist\SigmaVPN_Bot_Admin.exe" (
    echo ✅ EXE файл найден
    echo 🚀 Запускаю панель управления...
    echo.
    start "" "dist\SigmaVPN_Bot_Admin.exe"
    exit /b 0
)

REM Если EXE не существует, запустить Python скрипт
echo ⚠️  EXE файл не найден
echo 📝 Запускаю через Python...
echo.

if exist "bot_admin_panel.py" (
    python bot_admin_panel.py
) else (
    echo ❌ Файл bot_admin_panel.py не найден!
    pause
    exit /b 1
)
