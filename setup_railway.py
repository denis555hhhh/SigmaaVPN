#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Railway Deployment Setup Script
Initializes Git repository and prepares for Railway deployment
"""

import os
import subprocess
import sys

def run_command(cmd, description):
    """Run a shell command and report results"""
    print(f"\n📝 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()[:100]}")
            return True
        else:
            print(f"❌ {description} - FAILED")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()[:200]}")
            return False
    except Exception as e:
        print(f"❌ {description} - EXCEPTION: {str(e)}")
        return False

def main():
    print("=" * 70)
    print("🚀 RAILWAY DEPLOYMENT SETUP")
    print("=" * 70)
    
    # Step 1: Configure Git
    print("\n📋 STEP 1: Configure Git")
    run_command('git config --global user.email "test@example.com"', "Set Git email")
    run_command('git config --global user.name "SigmaVPN"', "Set Git name")
    
    # Step 2: Initialize Git repository
    print("\n📋 STEP 2: Initialize Git Repository")
    if os.path.exists('.git'):
        print("✓ Git repository already exists")
    else:
        run_command('git init', "Initialize Git repository")
    
    # Step 3: Add all files
    print("\n📋 STEP 3: Add Files to Git")
    run_command('git add .', "Add all files to Git")
    
    # Step 4: Create initial commit
    print("\n📋 STEP 4: Create Initial Commit")
    run_command('git commit -m "Initial commit: SigmaVPN website with Railway deployment files"', "Create initial commit")
    
    # Step 5: Display next steps
    print("\n" + "=" * 70)
    print("✅ GIT SETUP COMPLETE!")
    print("=" * 70)
    print("\n📌 NEXT STEPS:")
    print("\n1. Create GitHub Repository:")
    print("   - Go to https://github.com/new")
    print("   - Repository name: sigmavpn-website")
    print("   - Click 'Create repository'")
    print("\n2. Add Remote and Push:")
    print("   git remote add origin https://github.com/YOUR_USERNAME/sigmavpn-website.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    print("\n3. Deploy to Railway:")
    print("   - Go to https://railway.app")
    print("   - Click 'New Project'")
    print("   - Select 'Deploy from GitHub'")
    print("   - Choose 'sigmavpn-website'")
    print("   - Railway will automatically deploy!")
    print("\n4. Update API URLs:")
    print("   - After deployment, update API_URL in:")
    print("     * register.js")
    print("     * login.js")
    print("     * checkout.js")
    print("     * cabinet.js")
    print("   - Change from: http://localhost:5000")
    print("   - Change to: https://your-railway-url.railway.app")
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()
