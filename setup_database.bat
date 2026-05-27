@echo off
REM Setup database for SigmaVPN
REM This batch file creates the SQLite database

cd /d "c:\Users\Gnida222\Desktop\Сайт впн"

echo Creating SigmaVPN database...
python create_database.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Database setup completed successfully!
    echo.
) else (
    echo.
    echo Error: Database setup failed!
    echo.
)

pause
