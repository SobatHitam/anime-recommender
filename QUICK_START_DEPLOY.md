# 🚀 QUICK START DEPLOYMENT - 5 MENIT SAJA!

## Langkah 1: Buka GitHub & Create Token (2 menit)

### 1.1 Buat GitHub Account (Jika belum punya)
- Buka: https://github.com
- Sign up (gratis)
- Verify email

### 1.2 Generate Personal Access Token
1. Buka: https://github.com/settings/tokens
2. Klik **"Generate new token"** → **"Generate new token (classic)"**
3. Isi:
   - **Note**: `Anime Recommender Deployment`
   - **Expiration**: 90 days (atau No expiration)
   - **Scopes**: Pilih ✅ repo, ✅ workflow, ✅ gist
4. Scroll down, klik **"Generate token"**
5. **COPY TOKEN** (hanya muncul sekali!)

**Simpan ini - butuh di Step 2!** ✅

---

## Langkah 2: Run Deployment Script (2 menit)

### 2.1 Buka PowerShell di Folder Project

```powershell
# Buka PowerShell
# Navigate ke folder project
cd d:\Documents\Coding\SRIPSI

# Lihat script ada:
ls deploy.bat
```

### 2.2 Run Script

```powershell
# Windows
.\deploy.bat

# Atau bisa double-click file deploy.bat
```

### 2.3 Isi Info Saat Diminta

```
Prompt: GitHub Username (e.g., john-doe): 
Jawab:  [Ketik username GitHub Anda]

Prompt: GitHub Personal Access Token: 
Jawab:  [Paste token dari Step 1.2]

Then: Script akan push otomatis!
```

**Output yang benar:**
```
✅ Git installed
✅ Remote configured
✅ Successfully pushed to GitHub!
```

---

## Langkah 3: Deploy ke Streamlit Cloud (1 menit)

### 3.1 Buka Streamlit Cloud
- Buka: https://share.streamlit.io/

### 3.2 Sign In dengan GitHub
- Klik **"Sign in"** → **"Continue with GitHub"**
- Authorize Streamlit app

### 3.3 Deploy App
1. Klik **"New app"** (top-left)
2. **Repository**: YOUR_USERNAME/anime-recommender
3. **Branch**: main
4. **Main file path**: app.py
5. Klik **"Deploy"**

---

## 🎉 Selesai! App Anda Live!

Setelah ~5-10 menit, aplikasi akan live di:
```
https://anime-recommender-[random].streamlit.app
```

**Test aplikasi:**
- ✅ Pilih anime "One Piece"
- ✅ Coba search "naruto"
- ✅ Coba filter "Movie"
- ✅ Lihat statistics

---

## 📱 Share URL dengan Siapa Saja!

URL aplikasi Anda bisa dibagikan:
- Ke teman via WhatsApp/Email
- Di LinkedIn/Twitter
- Di portfolio/resume
- Di dokumentasi GitHub

---

## 🔄 Update Aplikasi (Kapan Saja)

Jika ingin update code:
```powershell
# Edit app.py atau file apapun

# Commit & push
git add .
git commit -m "Describe your changes"
git push

# Streamlit Cloud otomatis redeploy dalam 1-2 menit!
```

---

## 🆘 Troubleshooting

### Error: "ModuleNotFoundError"
```
→ Tunggu Streamlit download NLTK (5-10 menit first time)
→ Atau check error logs di Streamlit Cloud dashboard
```

### Error: "anime.csv not found"  
```
→ Ensure anime.csv di-commit ke GitHub
→ Run: git ls-files | grep anime.csv
→ If missing: git add anime.csv && git push
```

### Script tidak jalan
```
→ Open PowerShell as Administrator
→ Run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
→ Then: .\deploy.bat
```

---

## 📊 Repository Sudah Ada!

```
Local: d:\Documents\Coding\SRIPSI
├── .git/ (version control)
├── .streamlit/ (config)
├── app.py (main aplikasi)
├── anime.csv (12,434 anime)
├── requirements.txt (dependencies)
└── [semua documentation files]
```

**Status**: ✅ Ready to push ke GitHub

---

## ✅ Deployment Checklist

- [ ] GitHub account created
- [ ] Personal Access Token generated (& saved)
- [ ] deploy.bat script ready
- [ ] Run deploy.bat dengan credentials
- [ ] GitHub repository created
- [ ] Files pushed to GitHub (verify: https://github.com/YOUR_USERNAME/anime-recommender)
- [ ] Streamlit Cloud deployment started
- [ ] App live & tested
- [ ] URL shared

---

**That's it! Anda officially have a live production app! 🎊**

Next time mau update, cukup:
```
Edit code → git add . → git commit -m "..." → git push → Done!
```

Streamlit Cloud otomatis handle semuanya! 🚀

---

**Questions?** Check logs di:
- Local: Terminal output
- GitHub: Repository page
- Streamlit Cloud: App dashboard → Logs
