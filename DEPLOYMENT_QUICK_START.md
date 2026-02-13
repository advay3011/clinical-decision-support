# Deployment Quick Start (5 Minutes)

## 1️⃣ Push to GitHub

```bash
git add .
git commit -m "Initial commit: Clinical Decision Support Chatbot"
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

Replace:
- `YOUR_USERNAME` with your GitHub username
- `REPO_NAME` with your repository name (e.g., `clinical-decision-support`)

## 2️⃣ Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select:
   - Repository: `YOUR_USERNAME/REPO_NAME`
   - Branch: `main`
   - Main file: `streamlit_app.py`
5. Click "Deploy"

## 3️⃣ Add API Key

1. After deployment, click ⋯ (top right)
2. Select "Settings"
3. Go to "Secrets"
4. Add:
   ```
   ANTHROPIC_API_KEY = "your-api-key-here"
   ```
5. Save

## 4️⃣ Done! 🎉

Your app is live at:
```
https://YOUR_USERNAME-REPO_NAME.streamlit.app
```

## Updating Your App

Every time you push to GitHub, Streamlit Cloud auto-deploys:

```bash
git add .
git commit -m "Update: [your changes]"
git push origin main
```

Wait 1-2 minutes and your changes are live!

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "ModuleNotFoundError" | Check `requirements.txt` has all packages |
| "API key not found" | Add to Streamlit Cloud Secrets (Step 3) |
| Changes not showing | Wait 2 minutes, hard refresh (Cmd+Shift+R) |
| App is slow | First load is slow, subsequent loads are faster |

## Files You Need

✅ `streamlit_app.py` - Main app (required)  
✅ `requirements.txt` - Dependencies (required)  
✅ `.streamlit/config.toml` - Config (optional)  
✅ `.gitignore` - Git ignore (optional)  

All are already created for you!

---

**Full guide:** See `DEPLOYMENT_GUIDE.md`
