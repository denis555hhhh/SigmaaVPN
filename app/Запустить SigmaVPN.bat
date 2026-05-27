@echo off
chcp 65001 >nul
title SigmaVPN
color 0A
echo.
echo  ================================
echo   SigmaVPN - Запуск приложения
echo  ================================
echo.
start "" "%~dp0dist\SigmaVPN.exe"
timeout /t 2 /nobreak
exit
