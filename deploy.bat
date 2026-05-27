@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo 🚀 SIGMAVPN DEPLOYMENT SCRIPT
echo ============================================================
echo.

cd /d "c:\Users\Gnida222\Desktop\Сайт впн"

echo 🔧 Step 1: Removing old Git repository...
rmdir /s /q .git 2>nul
echo ✅ Done

echo.
echo 🔧 Step 2: Initializing new Git repository...
git init
echo ✅ Done

echo.
echo 🔧 Step 3: Adding all files...
git add .
echo ✅ Done

echo.
echo 🔧 Step 4: Creating commit...
git config user.email "test@example.com"
git config user.name "SigmaVPN"
git commit -m "Initial commit with all files"
echo ✅ Done

echo.
echo 🔧 Step 5: Adding GitHub remote...
git remote add origin https://github.com/deni555hhhh/FIgma.git
echo ✅ Done

echo.
echo 🔧 Step 6: Renaming branch to main...
git branch -M main
echo ✅ Done

echo.
echo 🔧 Step 7: Pushing to GitHub...
echo ⚠️  You will be prompted for GitHub credentials
echo    Username: deni555hhhh
echo    Password: Your Personal Access Token
echo.
git push -u origin main --force

echo.
echo ============================================================
echo ✅ DEPLOYMENT COMPLETE!
echo ============================================================
echo.
echo 📋 Next Steps:
echo 1. Go to https://railway.app
echo 2. Click on your FIgma project
echo 3. Wait for automatic rebuild (2-5 minutes)
echo 4. Your site will be available at the Railway URL
echo.
echo ============================================================
echo.
pause
