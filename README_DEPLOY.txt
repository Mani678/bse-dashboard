# BSE Dashboard - Deployment Guide

## Files You Need:

1. **dashboard.py** - Main app
2. **requirements.txt** - Dependencies
3. **config.toml** - Theme settings

## Folder Structure:

```
your-project/
  ├── dashboard.py
  ├── requirements.txt
  └── .streamlit/
      └── config.toml
```

## Steps to Deploy:

### 1. Create GitHub Repository
- Go to github.com
- Click "New repository"
- Name it: "bse-dashboard"
- Create it

### 2. Upload Files
- Upload dashboard.py
- Upload requirements.txt
- Create folder: .streamlit
- Inside .streamlit, upload config.toml

### 3. Deploy to Streamlit Cloud
- Go to streamlit.io/cloud
- Sign in with GitHub
- Click "New app"
- Select your repo: bse-dashboard
- Main file: dashboard.py
- Click "Deploy"

### 4. Wait 2 Minutes
Your dashboard will be live at:
https://YOUR-USERNAME-bse-dashboard.streamlit.app

## That's It!

Share the URL with anyone - they can watch BSE live! 🎉
