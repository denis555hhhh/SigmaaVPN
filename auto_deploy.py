#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automatic Railway Deployment Script
Handles Git initialization, commit, and push to GitHub
"""

import os
import subprocess
import sys

def run_command(cmd, description):
    """Run a shell command and report status"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}\n")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        
        if result.stdout:
            print("✓ Output:")
            print(result.stdout[:500])  # Limit output
        
        if result.stderr:
            print("⚠ Warnings/Errors:")
            print(result.stderr[:500])
        
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"❌ {description} - FAILED (code: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏱ {description} - TIMEOUT")
        return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {str(e)}")
        return False

def main():
    """Main deployment function"""
    
    project_dir = r"c:\Users\Gnida222\Desktop\Сайт впн"
    os.chdir(project_dir)
    
    print("\n" + "="*60)
    print("🚀 SIGMAVPN RAILWAY DEPLOYMENT - AUTOMATIC")
    print("="*60)
    print(f"📁 Project Directory: {project_dir}")
    print(f"📍 Current Directory: {os.getcwd()}")
    
    # Step 1: Configure Git
    if not run_command(
        'git config --global user.email "test@example.com"',
        "Configure Git Email"
    ):
        print("⚠ Git config email failed, continuing...")
    
    if not run_command(
        'git config --global user.name "SigmaVPN"',
        "Configure Git Name"
    ):
        print("⚠ Git config name failed, continuing...")
    
    # Step 2: Initialize Git Repository
    if not run_command(
        'git init',
        "Initialize Git Repository"
    ):
        print("⚠ Git init failed, checking if already initialized...")
    
    # Step 3: Add all files
    if not run_command(
        'git add .',
        "Add All Files to Git"
    ):
        print("❌ Failed to add files")
        return False
    
    # Step 4: Create initial commit
    if not run_command(
        'git commit -m "Initial commit: SigmaVPN website with Railway deployment"',
        "Create Initial Commit"
    ):
        print("⚠ Commit failed, might already exist")
    
    # Step 5: Add remote repository
    if not run_command(
        'git remote add origin https://github.com/deni555hhhh/sigma.git',
        "Add GitHub Remote Repository"
    ):
        print("⚠ Remote might already exist, trying to update...")
        run_command(
            'git remote set-url origin https://github.com/deni555hhhh/sigma.git',
            "Update GitHub Remote URL"
        )
    
    # Step 6: Rename branch to main
    if not run_command(
        'git branch -M main',
        "Rename Branch to Main"
    ):
        print("⚠ Branch rename failed")
    
    # Step 7: Push to GitHub
    if not run_command(
        'git push -u origin main',
        "Push Code to GitHub"
    ):
        print("❌ Failed to push to GitHub")
        print("\n⚠ IMPORTANT: You may need to:")
        print("  1. Create a GitHub Personal Access Token")
        print("  2. Use the token as password when prompted")
        print("  3. Or configure SSH keys")
        return False
    
    # Success!
    print("\n" + "="*60)
    print("✅ DEPLOYMENT SUCCESSFUL!")
    print("="*60)
    print("\n📋 Next Steps:")
    print("1. Go to https://railway.app")
    print("2. Click 'New Project'")
    print("3. Select 'Deploy from GitHub'")
    print("4. Choose repository 'sigma'")
    print("5. Click 'Deploy'")
    print("\n⏱ Wait 2-5 minutes for Railway to build and deploy")
    print("🌐 Your site will be available at: https://sigma-production.railway.app")
    print("\n" + "="*60)
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
