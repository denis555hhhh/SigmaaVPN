@echo off
cd /d "%~dp0"
echo Добавляю файлы в git...
git add -A
echo Коммитю изменения...
git commit -m "Fix app.py and add style.css, main.js"
echo Пушу на GitHub...
git push
echo Готово! Railway автоматически перестроится.
pause
