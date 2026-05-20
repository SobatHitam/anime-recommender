# 📋 PANDUAN DEPLOYMENT STEP-BY-STEP

## 🎯 Tujuan
Deploy aplikasi Anime Recommender ke Streamlit Cloud agar bisa diakses online dengan URL public.

## ⏱️ Estimasi Waktu: 20-30 menit

---

## 📝 TAHAP 1: Persiapan (5 menit)

### Step 1.1: Buat GitHub Account (Jika belum punya)
- Buka: https://github.com
- Click "Sign up"
- Isi: email, password, username
- Verify email
- **Ingat username GitHub Anda** (misal: `john-doe`)

### Step 1.2: Buka Terminal/PowerShell
```
Windows: Buka PowerShell atau Command Prompt
Linux/Mac: Buka Terminal
```

### Step 1.3: Navigate ke Folder Project
```powershell
cd d:\Documents\Coding\SRIPSI
```

**Verifikasi folder struktur:**
```powershell
# List files
dir

# Should show:
# - app.py
# - anime.csv
# - requirements.txt
# - .gitignore
# - README.md
# - etc
```

---

## 🔧 TAHAP 2: Setup Git (5 menit)

### Step 2.1: Check if Git Installed
```powershell
git --version

# Should show: git version xxx
```

**Jika error:** Download Git dari https://git-scm.com/

### Step 2.2: Configure Git (First time only)
```powershell
git config --global user.name "Your Full Name"
git config --global user.email "your.email@gmail.com"

# Example:
# git config --global user.name "John Doe"
# git config --global user.email "john@example.com"
```

### Step 2.3: Initialize Git Repository
```powershell
git init

# Output: Initialized empty Git repository in ...
```

### Step 2.4: Add All Files
```powershell
git add .

# Verify files to be committed:
git status
# Should show all files in "Changes to be committed"
```

### Step 2.5: Create First Commit
```powershell
git commit -m "Initial commit: Anime Recommender System"

# Output: create mode 100644 app.py
#         create mode 100644 anime.csv
#         etc...
```

---

## 🌐 TAHAP 3: Create GitHub Repository (5 menit)

### Step 3.1: Go to GitHub
- Buka browser ke: https://github.com
- **Sign in** dengan akun Anda

### Step 3.2: Create New Repository
1. Klik **"+"** di top-right → **"New repository"**
2. Atau buka: https://github.com/new

### Step 3.3: Fill Repository Details

```
Repository name:        anime-recommender
Description:            Content-Based Filtering Anime Recommendation System
                       (optional tapi recommended)

Visibility:             PUBLIC (PENTING! Must be public untuk Streamlit Cloud)

Initialize repository: Uncheck semua (sudah punya .git locally)
```

### Step 3.4: Create Repository
- Click **"Create repository"** button

### Step 3.5: Copy Repository URL
- Akan melihat page baru dengan:
  ```
  Quick setup — if you've done this kind of thing before
  
  …or push an existing repository from the command line
  
  git remote add origin https://github.com/YOUR_USERNAME/anime-recommender.git
  git branch -M main
  git push -u origin main
  ```
- **Copy** URL Anda (replace `YOUR_USERNAME`)

---

## 🚀 TAHAP 4: Push to GitHub (5 menit)

### Step 4.1: Add Remote Repository
```powershell
# Replace YOUR_USERNAME dengan username GitHub Anda
git remote add origin https://github.com/YOUR_USERNAME/anime-recommender.git

# Example:
# git remote add origin https://github.com/john-doe/anime-recommender.git
```

### Step 4.2: Rename Branch to Main
```powershell
git branch -M main
```

### Step 4.3: Push to GitHub
```powershell
git push -u origin main

# Mungkin minta GitHub credentials:
# - Username: YOUR_GITHUB_USERNAME
# - Password: YOUR_GITHUB_TOKEN (atau personal access token)
```

**Jika minta authentication:**

Option A: Personal Access Token (Recommended)
1. Go: https://github.com/settings/tokens
2. Click "Generate new token"
3. Select scopes: `repo`, `workflow`, `gist`
4. Click "Generate token"
5. Copy token
6. Paste di PowerShell saat minta password

Option B: GitHub CLI (Alternative)
```powershell
# Install: https://cli.github.com/
# Then:
gh auth login
# Follow prompts
```

### Step 4.4: Verify Push Success
```powershell
# Should see:
# Enumerating objects: XXX, done.
# Counting objects: 100% (XXX/XXX), done.
# Delta compression using up to 8 threads
# ...
# * [new branch]      main -> main
# Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## ✅ TAHAP 5: Verifikasi GitHub (2 menit)

### Step 5.1: Go to Your Repository
- Buka: https://github.com/YOUR_USERNAME/anime-recommender
- Replace `YOUR_USERNAME` dengan GitHub username

### Step 5.2: Verify Files
Harus terlihat semua files:
- ✅ app.py
- ✅ anime.csv
- ✅ requirements.txt
- ✅ README.md
- ✅ Semua documentation files

### Step 5.3: Verify Repository Settings
- **Visibility**: Public ✅
- **Description**: Isi dengan deskripsi

---

## 🌟 TAHAP 6: Deploy ke Streamlit Cloud (5 menit)

### Step 6.1: Sign Up Streamlit Community Cloud
- Buka: https://share.streamlit.io/
- Click **"Sign in"** → **"Continue with GitHub"**
- Authorize Streamlit app
- Streamlit akan redirect ke dashboard

### Step 6.2: Create New App
- Di dashboard Streamlit Cloud
- Click **"New app"** button (top-left)

### Step 6.3: Fill Deployment Info

```
Repository:        YOUR_USERNAME/anime-recommender
Branch:            main
Main file path:    app.py
```

**Contoh:**
```
Repository:        john-doe/anime-recommender
Branch:            main
Main file path:    app.py
```

### Step 6.4: Deploy!
- Click **"Deploy"** button
- Streamlit akan:
  1. Clone repository
  2. Install dependencies (pip install -r requirements.txt)
  3. Download NLTK data (~2-5 menit first time)
  4. Run aplikasi

**Monitor deployment:**
- Akan terlihat logs realtime
- Tunggu hingga muncul "App is running"

---

## 🎉 TAHAP 7: Selesai! (1 menit)

### Step 7.1: Dapatkan URL Public
```
Format: https://anime-recommender-YOUR_USERNAME.streamlit.app

Contoh:
https://anime-recommender-john-doe.streamlit.app
```

Streamlit akan otomatis generate URL dengan format: `[app-name]-[random].streamlit.app`

### Step 7.2: Akses Aplikasi
- Copy URL
- Paste di browser
- **Aplikasi Anda live!** 🎊

### Step 7.3: Test Features
```
✅ Coba recommendation: pilih "One Piece"
✅ Coba search: ketik "naruto"
✅ Coba filter: select "Movie" type
✅ Coba statistics: lihat metrics
✅ Verify dark theme muncul
```

### Step 7.4: Share URL
**Kirim ke:**
- Teman via WhatsApp/Email
- LinkedIn profile
- GitHub README
- Portfolio website

---

## 🔄 TAHAP BONUS: Auto-Redeploy

Setiap kali push code ke GitHub, Streamlit otomatis redeploy!

### Cara Update Aplikasi:
```powershell
# 1. Edit app.py (misalnya)
# 2. Save file

# 3. Commit & push
git add .
git commit -m "Update: improve recommendation algorithm"
git push

# 4. Streamlit Cloud otomatis redeploy!
# (check pada app dashboard, biasanya 1-2 menit)
```

---

## 🆘 Troubleshooting

### Error 1: "ModuleNotFoundError: No module named 'nltk'"

**Solusi:**
- Streamlit Cloud akan install dari requirements.txt
- Pastikan requirements.txt ada & di-commit
- Force redeploy: Settings → Reboot app

### Error 2: "anime.csv not found"

**Solusi:**
- Pastikan anime.csv ada di repository
- Check: `git ls-files | grep anime.csv`
- Jika hilang: `git add anime.csv && git push`

### Error 3: "Permission denied" atau auth error

**Solusi:**
- Use Personal Access Token (lebih aman)
- Atau gunakan GitHub CLI (`gh auth login`)
- Check SSH keys (optional)

### Error 4: Aplikasi timeout (>15 menit deployment)

**Solusi:**
- Streamlit Cloud environment powerful
- Biasanya NLTK download yang lama (5-10 min)
- Tunggu saja, atau check logs

### Error 5: Deployment gagal dengan "Build failed"

**Solusi:**
- Check deployment logs
- Common causes:
  - Missing anime.csv
  - Syntax error di code
  - Missing dependency di requirements.txt

**Fix:**
1. Fix error locally
2. Test: `streamlit run app.py`
3. Commit & push
4. Streamlit otomatis redeploy

---

## 📊 Dashboard Streamlit Cloud

### Setelah Deploy, Anda Bisa:

**Monitor:**
- CPU/Memory usage
- Request logs
- Error logs
- Deployment status

**Access:**
- Click app di dashboard
- See URL & settings
- View deployment history

**Reboot/Redeploy:**
- Settings → Reboot app (force restart)
- Or push to GitHub (auto redeploy)

---

## 🎯 Useful Commands Recap

```powershell
# Navigate to folder
cd d:\Documents\Coding\SRIPSI

# Check status
git status

# Add files
git add .

# Commit
git commit -m "Your message"

# Push
git push

# Check logs
git log

# Check remote
git remote -v
```

---

## 📱 Share Your App

### URLs to Share:

**GitHub Repo:**
```
https://github.com/YOUR_USERNAME/anime-recommender
```

**Live App:**
```
https://anime-recommender-YOUR_USERNAME.streamlit.app
```

### Marketing Message:

```
🎌 Check out my Anime Recommender System!

🚀 Live Demo: https://anime-recommender-YOUR_USERNAME.streamlit.app

📚 Source Code: https://github.com/YOUR_USERNAME/anime-recommender

🔬 Content-Based Filtering dengan TF-IDF + Type Matching
Rekomendasi anime based on synopsis & type similarity!

Try it now! 🎬
```

---

## ✨ Deployment Checklist

- [ ] GitHub account created
- [ ] Local Git configured
- [ ] Files committed locally
- [ ] GitHub repository created (PUBLIC)
- [ ] Files pushed to GitHub
- [ ] Repository verified (all files present)
- [ ] Streamlit Cloud account created
- [ ] New app deployed
- [ ] Deployment successful
- [ ] URL generated
- [ ] Features tested
- [ ] URL shared with team

---

## 🎓 Next Steps (Optional)

### After Successful Deployment:

1. **Update README.md** dengan link ke live app:
   ```markdown
   # Anime Recommender System
   
   🚀 **Live Demo:** [anime-recommender-xxx.streamlit.app](https://...)
   ```

2. **Setup custom domain** (Streamlit Pro, $15/mo)

3. **Add Google Analytics** (track usage)

4. **Continuous improvements:**
   - Push updates to GitHub
   - Auto-redeploy on Streamlit Cloud

---

## ⏱️ Quick Reference

| Step | Time | Action |
|------|------|--------|
| 1 | 2 min | Create GitHub account |
| 2 | 5 min | Git setup & commit |
| 3 | 5 min | Create GitHub repo |
| 4 | 5 min | Push to GitHub |
| 5 | 2 min | Verify on GitHub |
| 6 | 5-10 min | Deploy to Streamlit Cloud |
| 7 | 1 min | Test & share |
| **TOTAL** | **30 min** | **App live!** |

---

## 🆘 Need Help?

### Resources:
- Streamlit Docs: https://docs.streamlit.io/
- Streamlit Cloud: https://docs.streamlit.io/streamlit-cloud
- GitHub Help: https://docs.github.com
- Git Guide: https://git-scm.com/docs

### Common Questions:
- **Q: Berapa cost?** A: Gratis (Streamlit Community Cloud free tier)
- **Q: Berapa uptime?** A: 99.9% (reliable)
- **Q: Perlu credit card?** A: Tidak untuk free tier
- **Q: Bisa update offline?** A: Ya, push ke GitHub kapan saja
- **Q: URL bisa custom?** A: Bisa dengan Streamlit Pro ($15/mo)

---

## 🎉 Congrats!

Aplikasi Anda now **live di internet**! 

Setiap orang di dunia bisa akses via URL Anda.

**Share dengan bangga!** 🚀

---

**Status:** ✅ Ready to Deploy  
**Last Updated:** May 19, 2026  
**Version:** 1.0.0

---

*Sudah siap? Follow tahapan di atas dan aplikasi Anda akan live dalam 30 menit!*
