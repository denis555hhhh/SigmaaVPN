@echo off
REM Automatic Railway Deployment Script
REM This script handles Git initialization, commit, and push to GitHub

cd /d "c:\Users\Gnida222\Desktop\Сайт впн"

echo.
echo ============================================================
echo 🚀 SIGMAVPN RAILWAY DEPLOYMENT - AUTOMATIC
echo ============================================================
echo.

REM Step 1: Configure Git
echo 🔧 Configuring Git...
git config --global user.email "test@example.com"
git config --global user.name "SigmaVPN"

REM Step 2: Initialize Git Repository
echo 🔧 Initializing Git Repository...
git init

REM Step 3: Add all files
echo 🔧 Adding all files to Git...
git add .

REM Step 4: Create initial commit
echo 🔧 Creating initial commit...
git commit -m "Initial commit: SigmaVPN website with Railway deployment"

REM Step 5: Add remote repository
echo 🔧 Adding GitHub remote repository...
git remote add origin https://github.com/deni555hhhh/sigma.git

REM Step 6: Rename branch to main
echo 🔧 Renaming branch to main...
git branch -M main

REM Step 7: Push to GitHub
echo 🔧 Pushing code to GitHub...
echo.
echo ⚠️  You may be prompted for your GitHub credentials.
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
