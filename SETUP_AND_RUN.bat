@echo off
chcp 65001 >nul
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  🚀 SigmaVPN - Полная автоматическая настройка            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Проверить Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не установлен!
    echo 📝 Установите Python с https://python.org
    pause
    exit /b 1
)

echo ✅ Python найден
echo.

REM Установить зависимости
echo 📦 Проверка зависимостей...
pip install -q pyinstaller 2>nul

REM Проверить, существует ли БД
if not exist "sigmavpn.db" (
    echo.
    echo ⚠️  БД не найдена!
    echo 📥 Скачайте файл sigmavpn.db с Railway:
    echo.
    echo 1. Откройте https://railway.app
    echo 2. Откройте проект SigmaVPN
    echo 3. Откройте сервис sigmaVPNN (веб)
    echo 4. Найдите файл sigmavpn.db
    echo 5. Скачайте его в эту папку
    echo 6. Запустите этот файл снова
    echo.
    pause
    exit /b 1
)

echo ✅ БД найдена
echo.

REM Проверить, существует ли EXE
if not exist "dist\SigmaVPN_Bot_Admin.exe" (
    echo 🔨 Создаю EXE файл...
    echo.
    
    REM Удалить старые файлы
    if exist "build" rmdir /s /q build >nul 2>&1
    if exist "dist" rmdir /s /q dist >nul 2>&1
    
    REM Создать EXE
    pyinstaller --onefile --windowed --name=SigmaVPN_Bot_Admin bot_admin_panel.py
    
    if errorlevel 1 (
        echo ❌ Ошибка при создании EXE
        pause
        exit /b 1
    )
    
    echo ✅ EXE файл создан!
    echo.
)

REM Запустить панель
echo 🚀 Запускаю панель управления...
echo.

start "" "dist\SigmaVPN_Bot_Admin.exe"

echo ✅ Панель управления запущена!
echo.
echo 💡 Совет: Нажмите '🔄 Обновить' для загрузки данных из БД
echo.

exit /b 0
