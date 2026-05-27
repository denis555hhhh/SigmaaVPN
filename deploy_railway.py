#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Railway Deployment Automation Script
Handles Git initialization, commit, and push to GitHub
"""

import os
import subprocess
import sys

def run_command(cmd, description=""):
    """Run a shell command and return success status"""
    try:
        if description:
            print(f"\n📌 {description}")
        print(f"▶️  {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(f"❌ Error: {result.stderr}")
            return False
        
        print("✅ Success!")
        return True
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def main():
    """Main deployment function"""
    project_dir = r"c:\Users\Gnida222\Desktop\Сайт впн"
    os.chdir(project_dir)
    
    print("=" * 70)
    print("🚀 SIGMAVPN - RAILWAY DEPLOYMENT AUTOMATION")
    print("=" * 70)
    
    # Step 1: Configure Git
    print("\n📋 STEP 1: Configuring Git...")
    run_command('git config --global user.email "test@example.com"', "Setting Git email")
    run_command('git config --global user.name "SigmaVPN"', "Setting Git name")
    
    # Step 2: Initialize Git repository
    print("\n📋 STEP 2: Initializing Git repository...")
    if not os.path.exists('.git'):
        run_command('git init', "Initializing Git repository")
    else:
        print("✅ Git repository already exists")
    
    # Step 3: Add all files
    print("\n📋 STEP 3: Adding files to Git...")
    run_command('git add .', "Adding all files")
    
    # Step 4: Create initial commit
    print("\n📋 STEP 4: Creating initial commit...")
    run_command('git commit -m "Initial commit: SigmaVPN website with Railway deployment"', "Creating commit")
    
    # Step 5: Check remote
    print("\n📋 STEP 5: Checking remote repository...")
    result = subprocess.run('git remote -v', shell=True, capture_output=True, text=True)
    if result.stdout:
        print("✅ Remote already configured:")
        print(result.stdout)
    else:
        print("⚠️  No remote configured yet")
        print("\n📌 To add remote, run:")
        print('   git remote add origin https://github.com/deni555hhhh/sigma.git')
        print('   git branch -M main')
        print('   git push -u origin main')
    
    print("\n" + "=" * 70)
    print("✅ DEPLOYMENT PREPARATION COMPLETE!")
    print("=" * 70)
    print("\n📌 NEXT STEPS:")
    print("1. If remote not configured, run the commands above")
    print("2. Go to https://railway.app")
    print("3. Create new project → Deploy from GitHub")
    print("4. Select 'sigma' repository")
    print("5. Railway will automatically deploy!")
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()
