#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct Railway Deployment Script
Handles Git initialization and push without PowerShell
"""

import os
import subprocess
import sys

def run_command(cmd, description=""):
    """Run a shell command and return success status"""
    try:
        if description:
            print(f"\n🔧 {description}")
        print(f"   Executing: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.stdout:
            print(f"   Output: {result.stdout[:200]}")
        if result.stderr:
            print(f"   Error: {result.stderr[:200]}")
        
        return result.returncode == 0
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
        return False

def main():
    """Main deployment function"""
    project_dir = r"c:\Users\Gnida222\Desktop\Сайт впн"
    os.chdir(project_dir)
    
    print("=" * 60)
    print("🚀 SIGMAVPN RAILWAY DEPLOYMENT")
    print("=" * 60)
    
    # Step 1: Configure Git
    if not run_command('git config --global user.email "test@example.com"', "Step 1: Configure Git email"):
        print("❌ Failed to configure Git email")
        return False
    
    if not run_command('git config --global user.name "SigmaVPN"', "Step 2: Configure Git name"):
        print("❌ Failed to configure Git name")
        return False
    
    # Step 3: Initialize Git Repository
    if not run_command('git init', "Step 3: Initialize Git Repository"):
        print("❌ Failed to initialize Git repository")
        return False
    
    # Step 4: Add all files
    if not run_command('git add .', "Step 4: Adding all files"):
        print("❌ Failed to add files")
        return False
    
    # Step 5: Create initial commit
    if not run_command('git commit -m "Initial commit: SigmaVPN website with Railway deployment"', "Step 5: Creating commit"):
        print("❌ Failed to create commit")
        return False
    
    # Step 6: Add remote repository
    if not run_command('git remote add origin https://github.com/deni555hhhh/sigma.git', "Step 6: Adding GitHub remote"):
        print("❌ Failed to add remote")
        return False
    
    # Step 7: Rename branch to main
    if not run_command('git branch -M main', "Step 7: Renaming branch to main"):
        print("❌ Failed to rename branch")
        return False
    
    # Step 8: Push to GitHub
    print("\n" + "=" * 60)
    print("⚠️  IMPORTANT: GitHub Credentials Required")
    print("=" * 60)
    print("\nYou will be prompted for GitHub credentials.")
    print("Username: deni555hhhh")
    print("Password: Use your GitHub Personal Access Token")
    print("\nTo create a token:")
    print("1. Go to https://github.com/settings/tokens")
    print("2. Click 'Generate new token'")
    print("3. Select scopes: repo, workflow")
    print("4. Copy the token and paste it when prompted")
    print("\n" + "=" * 60 + "\n")
    
    if not run_command('git push -u origin main', "Step 8: Pushing to GitHub"):
        print("❌ Failed to push to GitHub")
        print("\nTroubleshooting:")
        print("- Check your GitHub credentials")
        print("- Ensure you're using a Personal Access Token, not your password")
        print("- Verify the token has 'repo' and 'workflow' scopes")
        return False
    
    # Success!
    print("\n" + "=" * 60)
    print("✅ DEPLOYMENT COMPLETE!")
    print("=" * 60)
    print("\n📋 Next Steps:")
    print("1. Go to https://railway.app")
    print("2. Click 'New Project'")
    print("3. Select 'Deploy from GitHub'")
    print("4. Choose repository 'sigma'")
    print("5. Click 'Deploy'")
    print("\n⏱️  Wait 2-5 minutes for Railway to build and deploy")
    print("🌐 Your site will be available at: https://sigma-production.railway.app")
    print("\n" + "=" * 60)
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
