# 🚀 Panduan Deployment - Hosting Aplikasi Anime Recommender

## 📚 Daftar Isi
1. [Opsi Deployment](#opsi-deployment)
2. [Metode 1: Streamlit Cloud (RECOMMENDED - Gratis & Termudah)](#metode-1-streamlit-cloud--recommended)
3. [Metode 2: Railway](#metode-2-railway)
4. [Metode 3: Heroku](#metode-3-heroku)
5. [Metode 4: Replit](#metode-4-replit)
6. [Post-Deployment](#post-deployment)

---

## 🎯 Opsi Deployment

### Perbandingan Platform

| Platform | Cost | Setup | Performance | Recommendation |
|----------|------|-------|-------------|---|
| **Streamlit Cloud** | FREE | ⭐⭐ | Good | ✅ **BEST** |
| **Railway** | FREE tier | ⭐⭐⭐ | Excellent | Good alternative |
| **Heroku** | Paid (~$7/mo) | ⭐⭐ | Good | Legacy option |
| **Replit** | FREE tier | ⭐ | Fair | Simple start |
| **AWS/GCP** | Variable | ⭐⭐⭐⭐ | Excellent | Enterprise |

**Rekomendasi**: **Streamlit Cloud** - Khusus dibuat untuk Streamlit, paling mudah!

---

## 🌐 Metode 1: Streamlit Cloud (RECOMMENDED)

### Prerequisites
- GitHub account (gratis di https://github.com)
- Streamlit Community Cloud account (gratis)

### Step 1: Prepare Repository

#### 1a. Initialize Git
```bash
cd d:\Documents\Coding\SRIPSI
git init
```

#### 1b. Create .gitignore
```bash
# Create file named .gitignore
cat > .gitignore << EOF
venv/
__pycache__/
*.pyc
.DS_Store
.streamlit/secrets.toml
.env
*.csv.bak
EOF
```

#### 1c. Configure Git
```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

#### 1d. Add & Commit Files
```bash
git add .
git commit -m "Initial commit: Anime Recommender System"
```

### Step 2: Create GitHub Repository

1. **Go to** https://github.com/new
2. **Repository name**: `anime-recommender` (atau nama lain)
3. **Description**: "Content-Based Filtering Anime Recommendation System"
4. **Public** (supaya bisa deploy ke Streamlit Cloud)
5. **Skip initializing** (sudah punya git)
6. Click **Create repository**

### Step 3: Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/anime-recommender.git
git branch -M main
git push -u origin main
```

**Note**: Replace `YOUR_USERNAME` dengan username GitHub Anda

### Step 4: Deploy ke Streamlit Cloud

1. **Go to** https://share.streamlit.io/
2. **Sign in** dengan GitHub account
3. Click **"New app"** button
4. **Repository**: Select `your-username/anime-recommender`
5. **Branch**: `main`
6. **Main file path**: `app.py`
7. Click **Deploy!**

Streamlit akan:
- Install dependencies dari `requirements.txt`
- Download NLTK data (first run ~5 menit)
- Deploy aplikasi
- Berikan URL public (contoh: `https://anime-recommender-xyz.streamlit.app`)

### Step 5: Verify & Share

```
URL Anda: https://anime-recommender-YOUR_USERNAME.streamlit.app

Share dengan:
- Copy URL
- Kirim ke teman/kolega
- Embed di website
```

**Aplikasi live dalam 5-10 menit!** ✅

---

## 📝 File Konfigurasi untuk Streamlit Cloud

### Create `streamlit/config.toml`
```bash
# Create directory if not exists
mkdir -p .streamlit

# Create config.toml
cat > .streamlit/config.toml << EOF
[theme]
primaryColor = "#ff006e"
backgroundColor = "#0a0e27"
secondaryBackgroundColor = "#1a1f3a"
textColor = "#e0e0e0"

[server]
maxUploadSize = 200
headless = true

[client]
showErrorDetails = true
EOF
```

### Create `streamlit/secrets.toml` (Optional - untuk API keys)
```bash
# Jika butuh secrets/credentials, buat file ini
# PENTING: Jangan push ke GitHub!

cat > .streamlit/secrets.toml << EOF
# Example format (jika ada API keys nanti)
# api_key = "xxxxx"
# database_url = "xxxxx"
EOF

# Add to .gitignore
echo ".streamlit/secrets.toml" >> .gitignore
```

### Push konfigurasi ke GitHub
```bash
git add .streamlit/config.toml
git add .gitignore
git commit -m "Add Streamlit configuration"
git push
```

---

## 🚀 Metode 2: Railway

### Jika Anda lebih suka Railway (alternatif)

#### Step 1: Sign Up
- Go to https://railway.app
- Sign up dengan GitHub

#### Step 2: Create Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Connect GitHub
4. Select `anime-recommender` repository

#### Step 3: Configure
1. Add environment variable:
   ```
   PYTHONUNBUFFERED=1
   ```

2. Set start command:
   ```
   streamlit run app.py --server.port=8080
   ```

#### Step 4: Deploy
- Railway otomatis deploy
- Dapat URL seperti: `https://anime-recommender-prod-xxx.up.railway.app`

---

## 🔴 Metode 3: Heroku

### Setup Heroku (Paid option - $7/bulan)

#### Step 1: Create Account
- Go to https://heroku.com
- Sign up & verify email

#### Step 2: Create App
```bash
# Install Heroku CLI dari: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create anime-recommender

# Check app created
heroku apps
```

#### Step 3: Create Procfile
```bash
# Create file named "Procfile"
cat > Procfile << EOF
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
EOF
```

#### Step 4: Create runtime.txt
```bash
cat > runtime.txt << EOF
python-3.10.13
EOF
```

#### Step 5: Deploy
```bash
git add Procfile runtime.txt
git commit -m "Add Heroku deployment files"
git push heroku main

# Check status
heroku logs --tail
```

---

## 💻 Metode 4: Replit

### Simple Deployment di Replit

#### Step 1: Go to Replit
- https://replit.com
- Sign in dengan GitHub

#### Step 2: Import from GitHub
1. Click **"Create"** → **"Import from GitHub"**
2. Paste repo URL: `https://github.com/YOUR_USERNAME/anime-recommender`
3. Click **"Import"**

#### Step 3: Install & Run
```bash
# Terminal di Replit
pip install -r requirements.txt
streamlit run app.py
```

#### Step 4: Get Public URL
- Replit otomatis generate URL public
- Share URL ke siapapun

---

## 🔧 Troubleshooting Deployment

### Issue 1: NLTK Data Not Found

**Error:**
```
LookupError: Resource punkt not found
```

**Solusi - Create `setup.sh`:**
```bash
cat > setup.sh << EOF
#!/bin/bash
python -m nltk.downloader punkt stopwords wordnet averaged_perceptron_tagger
EOF

chmod +x setup.sh
```

**Untuk Streamlit Cloud**: Add ke requirements.txt:
```
nltk>=3.8.1
```

Add code di awal `app.py`:
```python
import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
```

### Issue 2: CSV File Not Found

**Error:**
```
FileNotFoundError: anime.csv not found
```

**Solusi:**
- Pastikan `anime.csv` ada di repository
- Jangan di .gitignore
- Commit & push ke GitHub

```bash
# Verify file exists
git ls-files | grep anime.csv

# If missing, add it
git add anime.csv
git commit -m "Add anime dataset"
git push
```

### Issue 3: Memory/Timeout

**Jika deployment timeout (>10 menit):**

Create `requirements-slim.txt` (optional dependencies):
```
streamlit>=1.28.0
nltk>=3.8.1
```

Streamlit Cloud memiliki resources cukup untuk ini.

---

## ✅ Post-Deployment Checklist

### Verify Aplikasi Berjalan

- [ ] URL aplikasi accessible
- [ ] Halaman load dengan benar (dark theme visible)
- [ ] Dropdown anime bisa di-scroll
- [ ] Rekomendasi feature bekerja
- [ ] Search functionality aktif
- [ ] Filter type berfungsi
- [ ] Statistics dashboard muncul
- [ ] Semua halaman navigable

### Test Features

```bash
# Test scenarios:
1. Try recommendation: "One Piece"
   Expected: Top 5 recommendations appear in <2s

2. Try search: "dragon"
   Expected: Results show instantly

3. Try filter: Select "Movie"
   Expected: Movie list appears

4. Check statistics:
   Expected: Metrics display correctly
```

### Share & Communicate

**Link untuk dishare:**
```
https://anime-recommender-YOUR_USERNAME.streamlit.app

Contoh:
https://anime-recommender-john.streamlit.app
```

**Share dengan:**
- Email
- WhatsApp
- LinkedIn
- Social media
- Documentation

---

## 📊 Monitoring & Maintenance

### Streamlit Cloud Dashboard

1. Go to https://share.streamlit.io/
2. Click aplikasi Anda
3. See:
   - Runtime stats
   - User activity
   - Deployment logs
   - Health status

### Update Aplikasi

Jika ada perubahan code:

```bash
# Local development
# Make changes di app.py

# Commit & push
git add .
git commit -m "Update recommendation algorithm"
git push

# Streamlit Cloud otomatis redeploy!
# (Usually within 1-2 menit)
```

### View Logs

**Streamlit Cloud:**
- Dashboard → App → Logs

**Railway:**
- Dashboard → Deployments → Logs

**Heroku:**
```bash
heroku logs --tail
```

---

## 🎯 Quick Start - Langkah Tercepat

### Untuk **Streamlit Cloud** (Recommended):

```bash
# 1. Create GitHub repo & push
cd d:\Documents\Coding\SRIPSI
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/anime-recommender.git
git push -u origin main

# 2. Go to https://share.streamlit.io/
# 3. Click "New app"
# 4. Select repo & main
# 5. Click "Deploy"
# 6. Done! App live dalam 5-10 menit
```

**Total time**: 15-20 menit

---

## 💡 Tips & Best Practices

### 1. Environment Variables

**Untuk sensitive data** (jika ada API keys nanti):

Streamlit Cloud:
1. Go to App Settings
2. Secrets tab
3. Add key-value pairs

```toml
# secrets.toml format
api_key = "xxx"
database_url = "xxx"
```

Access in code:
```python
import streamlit as st
api_key = st.secrets["api_key"]
```

### 2. Custom Domain (Paid)

Jika mau domain custom:
```
Default: anime-recommender-xxx.streamlit.app
Custom:  anime-recommender.com
```

Streamlit Cloud Pro ($15/bulan): custom domain support

### 3. Automatic Deploys

GitHub → Streamlit Cloud: **Otomatis sync**
- Push ke GitHub
- Streamlit otomatis redeploy
- Tidak perlu manual action

### 4. Caching untuk Performance

Code sudah optimal dengan:
```python
@st.cache_data
def load_anime_data():
    ...

@st.cache_resource  
def build_tfidf_features():
    ...
```

Ini mempercepat loading significantly!

---

## 📱 Mobile Responsiveness

Aplikasi sudah responsive untuk:
- ✅ Desktop
- ✅ Tablet
- ✅ Mobile

Streamlit handle semua screen sizes otomatis.

---

## 🔐 Security Notes

### What's Safe
- ✅ Source code public (no secrets)
- ✅ CSV data public (no personal info)
- ✅ Streamlit Cloud: SSL/HTTPS automatic

### What to Avoid
- ❌ Don't commit credentials
- ❌ Don't expose API keys
- ❌ Use .gitignore for secrets
- ❌ Don't commit `.streamlit/secrets.toml`

---

## 🎉 Selesai!

Aplikasi Anda akan:
- ✅ Live di URL public
- ✅ Accessible 24/7
- ✅ Auto-redeploy saat push
- ✅ Free (Streamlit Cloud)
- ✅ Professional deployment

---

## 📞 Troubleshooting Resources

| Issue | Resource |
|-------|----------|
| Streamlit Cloud | https://docs.streamlit.io/streamlit-cloud |
| Railway | https://docs.railway.app |
| Heroku | https://devcenter.heroku.com |
| Git Help | https://git-scm.com/docs |

---

## 🎓 Deployment Summary

```
Pilihan           Time    Cost     Effort   Notes
─────────────────────────────────────────────────
Streamlit Cloud   5 min   FREE     ⭐⭐     RECOMMENDED
Railway           10 min  FREE     ⭐⭐⭐    Good alt
Heroku            15 min  $7/mo    ⭐⭐     Paid
Replit            5 min   FREE     ⭐       Simple

→ Choose Streamlit Cloud for best experience!
```

---

**Next Step:** Follow Streamlit Cloud guide di atas, atau tanya jika ada kesulitan! 🚀

**Estimated time to live**: 20 menit ⏱️

---

**Version:** 1.0.0  
**Last Updated:** May 19, 2026  
**Status:** Ready to Deploy ✅
