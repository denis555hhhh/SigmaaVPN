@echo off
REM Simple Railway Deployment Script
REM Run this from Command Prompt (NOT PowerShell)

cd /d "c:\Users\Gnida222\Desktop\Сайт впн"

echo.
echo ============================================================
echo 🚀 SIGMAVPN RAILWAY DEPLOYMENT
echo ============================================================
echo.

REM Step 1: Configure Git
echo 🔧 Step 1: Configuring Git...
git config --global user.email "test@example.com"
git config --global user.name "SigmaVPN"

REM Step 2: Initialize Git Repository
echo 🔧 Step 2: Initializing Git Repository...
git init

REM Step 3: Add all files
echo 🔧 Step 3: Adding all files...
git add .

REM Step 4: Create initial commit
echo 🔧 Step 4: Creating commit...
git commit -m "Initial commit: SigmaVPN website with Railway deployment"

REM Step 5: Add remote repository
echo 🔧 Step 5: Adding GitHub remote...
git remote add origin https://github.com/deni555hhhh/sigma.git

REM Step 6: Rename branch to main
echo 🔧 Step 6: Renaming branch to main...
git branch -M main

REM Step 7: Push to GitHub
echo 🔧 Step 7: Pushing to GitHub...
echo.
echo ⚠️  You may be prompted for GitHub credentials.
echo    Use your GitHub username and personal access token as password.
echo.
git push -u origin main

echo.
echo ============================================================
echo ✅ DEPLOYMENT COMPLETE!
echo ============================================================
echo.
echo 📋 Next Steps:
echo 1. Go to https://railway.app
echo 2. Click 'New Project'
echo 3. Select 'Deploy from GitHub'
echo 4. Choose repository 'sigma'
echo 5. Click 'Deploy'
echo.
echo ⏱ Wait 2-5 minutes for Railway to build and deploy
echo 🌐 Your site will be available at: https://sigma-production.railway.app
echo.
echo ============================================================
echo.
pause
