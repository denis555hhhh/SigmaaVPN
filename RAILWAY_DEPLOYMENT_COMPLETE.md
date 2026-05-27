# 🚀 SigmaVPN Railway Deployment - Complete Guide

## ✅ Status: READY FOR DEPLOYMENT

All files are prepared and configured for Railway deployment. Your SigmaVPN website is ready to go live!

---

## 📋 What's Been Prepared

### 1. **Railway Configuration Files** ✓
- `Procfile` - Defines how to run your app on Railway
- `requirements.txt` - All Python dependencies
- `runtime.txt` - Python version (3.11.0)
- `.gitignore` - Excludes unnecessary files from Git

### 2. **Backend API** ✓
- `app.py` - Flask backend with full API support
  - User registration & login
  - Subscription management
  - Database integration
  - CORS enabled for frontend

### 3. **Frontend Files** ✓
- Complete HTML/CSS/JS website
- All pages configured
- API integration ready
- Green theme (#16a34a)

### 4. **Database** ✓
- SQLite database (`sigmavpn.db`)
- Three tables: users, subscriptions, logs
- Ready for production use

---

## 🎯 Deployment Steps (Manual)

Since PowerShell has terminal issues, follow these steps manually:

### Step 1: Initialize Git Repository

Open Command Prompt or PowerShell and run:

```bash
cd "c:\Users\Gnida222\Desktop\Сайт впн"
git config --global user.email "test@example.com"
git config --global user.name "SigmaVPN"
git init
git add .
git commit -m "Initial commit: SigmaVPN website with Railway deployment files"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Fill in:
   - Repository name: `sigmavpn-website`
   - Description: `SigmaVPN website with API`
   - Choose: Public
3. Click "Create repository"

### Step 3: Push to GitHub

After creating the GitHub repo, run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/sigmavpn-website.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### Step 4: Deploy to Railway

1. Go to https://railway.app
2. Sign up or log in (use GitHub for easier setup)
3. Click "New Project"
4. Select "Deploy from GitHub"
5. Authorize GitHub if prompted
6. Select `sigmavpn-website` repository
7. Click "Deploy"

Railway will automatically:
- Install dependencies from `requirements.txt`
- Run your app using `Procfile`
- Assign a public URL
- Set up environment variables

### Step 5: Update API URLs

After Railway deployment, you'll get a URL like: `https://sigmavpn-website.railway.app`

Update these files with your Railway URL:

**File: `register.js`** (Line ~5)
```javascript
// Change from:
const API_URL = 'http://localhost:5000';

// To:
const API_URL = 'https://sigmavpn-website.railway.app';
```

**File: `login.js`** (Line ~5)
```javascript
const API_URL = 'https://sigmavpn-website.railway.app';
```

**File: `checkout.js`** (Line ~5)
```javascript
const API_URL = 'https://sigmavpn-website.railway.app';
```

**File: `cabinet.js`** (Line ~5)
```javascript
const API_URL = 'https://sigmavpn-website.railway.app';
```

### Step 6: Commit and Push Updates

```bash
git add .
git commit -m "Update API URLs for Railway deployment"
git push origin main
```

Railway will automatically redeploy your app!

---

## 🔍 Verify Deployment

After deployment, check:

1. **Website loads**: Visit your Railway URL
2. **Registration works**: Try creating an account
3. **Login works**: Try logging in
4. **API responds**: Check browser console for errors
5. **Database saves**: Verify data is stored

---

## 📊 Railway Dashboard

Once deployed, you can:

- **View Logs**: See application output and errors
- **Monitor Metrics**: Check CPU, memory, requests
- **Manage Variables**: Set environment variables
- **View Domains**: See your public URL
- **Redeploy**: Push to GitHub to auto-redeploy

---

## 🆘 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution**: Railway automatically installs from `requirements.txt`. Check that the file exists and is correct.

### Issue: "Port already in use"
**Solution**: Railway automatically assigns a port. The `PORT` environment variable is set automatically.

### Issue: "Database not found"
**Solution**: `app.py` automatically creates the database on first run.

### Issue: "CORS error"
**Solution**: CORS is already configured in `app.py` for all origins.

### Issue: "API not responding"
**Solution**: 
1. Check that API_URL is updated in JavaScript files
2. Verify Railway deployment completed successfully
3. Check Railway logs for errors

---

## 📁 File Structure

```
Сайт впн/
├── Procfile                 ← Railway configuration
├── requirements.txt         ← Python dependencies
├── runtime.txt             ← Python version
├── .gitignore              ← Git exclusions
├── app.py                  ← Flask backend
├── index.html              ← Main page
├── register.html           ← Registration page
├── login.html              ← Login page
├── cabinet.html            ← User cabinet
├── configurator.html       ← Subscription configurator
├── key-configurator.html   ← Key configurator
├── style.css               ← Styling
├── main.js                 ← Main JavaScript
├── register.js             ← Registration logic
├── login.js                ← Login logic
├── cabinet.js              ← Cabinet logic
├── configurator.js         ← Configurator logic
├── key-configurator.js     ← Key configurator logic
├── sigmavpn.db             ← SQLite database
└── app/                    ← Desktop app
    └── sigmavpn.py         ← Desktop application
```

---

## 🎉 You're All Set!

Your SigmaVPN website is fully prepared for Railway deployment. Follow the steps above and your site will be live on the internet within minutes!

### Quick Checklist:
- [ ] Initialize Git repository
- [ ] Create GitHub repository
- [ ] Push code to GitHub
- [ ] Deploy to Railway
- [ ] Update API URLs
- [ ] Commit and push updates
- [ ] Test website functionality
- [ ] Monitor Railway dashboard

---

## 📞 Support

For Railway support: https://docs.railway.app
For GitHub help: https://docs.github.com

Good luck! 🚀
