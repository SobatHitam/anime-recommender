# 📦 Panduan Instalasi & Cara Menjalankan

Panduan lengkap untuk instalasi dan menjalankan **Sistem Rekomendasi Anime** di Windows/Linux/Mac.

## ⚡ Quick Start (3 Langkah)

Jika Anda ingin langsung mencoba aplikasi:

```bash
# 1. Buka terminal di folder project
cd d:\Documents\Coding\SRIPSI

# 2. Install dependencies
python -m pip install -r requirements.txt

# 3. Jalankan aplikasi
streamlit run app.py
```

✅ **Done!** Aplikasi akan membuka di `http://localhost:8501`

---

## 📋 Prerequisites (Yang Harus Ada)

### 1. **Python 3.8+**
Cek versi Python Anda:
```bash
python --version
```

Jika Python belum terinstall, download dari: https://www.python.org/downloads/

**Pastikan saat install:**
- ✅ Centang "Add Python to PATH"
- ✅ Pilih "Customize installation" untuk akses lebih

### 2. **pip (Package Manager)**
Biasanya sudah included dengan Python. Cek:
```bash
pip --version
```

---

## 🔧 Instalasi Lengkap (Step-by-Step)

### Step 1: Verifikasi Python & pip

**Windows (PowerShell/Command Prompt):**
```bash
python --version
pip --version
```

**Linux/Mac (Terminal):**
```bash
python3 --version
pip3 --version
```

**Expected Output:**
```
Python 3.14.2
pip 26.1.1 from C:\Users\...\Python\pythoncore-3.14-64\lib\site-packages\pip
```

### Step 2: Navigate ke Project Folder

**Windows (PowerShell):**
```powershell
cd "d:\Documents\Coding\SRIPSI"
```

**Atau gunakan Command Prompt:**
```cmd
cd d:\Documents\Coding\SRIPSI
```

**Linux/Mac:**
```bash
cd ~/Documents/Coding/SRIPSI
```

### Step 3: Create Virtual Environment (Optional tapi RECOMMENDED)

Virtual environment memastikan dependencies tidak conflict dengan project lain.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Expected Output:**
```
(venv) PS D:\Documents\Coding\SRIPSI>  ← (venv) prefix muncul
```

### Step 4: Upgrade pip, setuptools, wheel (Optional tapi RECOMMENDED)

```bash
python -m pip install --upgrade pip setuptools wheel
```

Ini menghindari error saat install package kompleks seperti pandas.

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

**Penjelasan apa yang diinstall:**
- `streamlit==1.36.0` - Web framework
- `pandas==2.1.4` - Data processing
- `numpy==1.26.2` - Numerical computing
- `scikit-learn==1.3.2` - Machine learning & TF-IDF
- `nltk==3.8.1` - Natural Language Processing

**Expected Output:**
```
Successfully installed streamlit-1.36.0 pandas-2.1.4 numpy-1.26.2 scikit-learn-1.3.2 nltk-3.8.1
```

**Waktu instalasi:** 
- First time: 3-5 menit (build dari source)
- Baru-baru ini (cache): 30 detik

### Step 6: Download NLTK Data (One-time)

NLTK memerlukan data tambahan untuk stopwords. Jalankan:

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

Atau biarkan aplikasi Streamlit download otomatis saat pertama kali dijalankan.

**Expected Output:**
```
[nltk_data] Downloading package punkt to C:\Users\...\nltk_data...
[nltk_data]   Uncompressing tokenizers/punkt.zip.
[nltk_data] Downloading package stopwords to C:\Users\...\nltk_data...
[nltk_data]   Uncompressing corpora/stopwords.zip.
```

---

## 🚀 Menjalankan Aplikasi

### Opsi 1: Terminal Command

**Windows:**
```bash
streamlit run app.py
```

**Linux/Mac:**
```bash
streamlit run app.py
```

### Opsi 2: Specify Port (jika 8501 sudah terpakai)

```bash
streamlit run app.py --server.port 8502
```

### Opsi 3: Disable Analytics (Optional)

```bash
streamlit run app.py --logger.level=error
```

### Opsi 4: Headless Mode (untuk server/deployment)

```bash
streamlit run app.py --server.headless true
```

- Opsi 1: Edit dan upload ke server
- Opsi 2: Jalankan di background tanpa browser

---

## 📊 Expected Output & Browser

### Terminal Output:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://YOUR_IP:8501

  To stop the Streamlit server, press Ctrl+C to abort
```

### Browser akan opening otomatis ke:
```
http://localhost:8501
```

Jika tidak, copy-paste URL tersebut ke browser Anda.

---

## 🎮 Testing & Verification

Setelah aplikasi running, verify setiap fitur:

### ✅ Test Checklist

**Halaman Home:**
- [ ] Sidebar menu visible
- [ ] Header terlihat dengan styling yang bagus
- [ ] Layout responsive (test di mobile juga)

**Halaman Rekomendasi Anime:**
- [ ] Dropdown anime ter-load
- [ ] Tombol "Tampilkan Rekomendasi" clickable
- [ ] Rekomendasi muncul dengan scoring
- [ ] Tidak ada error

**Halaman Top Rating:**
- [ ] Anime dengan rating tinggi muncul
- [ ] Sorting benar (tertinggi dulu)

**Halaman Populer:**
- [ ] Anime populer ter-load
- [ ] Popularity score calculation valid

**Halaman Search & Filter:**
- [ ] Search functionality bekerja
- [ ] Genre filter multi-select bekerja
- [ ] Hasil filter akurat

**Halaman Statistics:**
- [ ] Metrics menampilkan nilai correct
- [ ] Chart genre visible
- [ ] Loading spinner muncul saat loading

**Performance:**
- [ ] Pertama load: 5-10 detik
- [ ] Kedua kali: < 2 detik (dari cache)
- [ ] Rekomendasi instant (<100ms)

---

## 🐛 Troubleshooting

### Error 1: "ModuleNotFoundError: No module named 'streamlit'"

**Penyebab:** Dependencies belum diinstall

**Solusi:**
```bash
pip install -r requirements.txt
```

### Error 2: "FileNotFoundError: anime.csv"

**Penyebab:** File anime.csv tidak ada atau path salah

**Solusi:**
1. Verifikasi anime.csv ada di folder project
2. Pastikan Anda berada di folder yang benar
3. Check file permissions

```bash
# Verify file existence
ls anime.csv   (Linux/Mac)
dir anime.csv  (Windows)
```

### Error 3: "Port 8501 already in use"

**Penyebab:** Port 8501 sudah dipakai aplikasi lain

**Solusi:** Gunakan port berbeda
```bash
streamlit run app.py --server.port 8502
```

Atau stop aplikasi yang sebelumnya running:
```bash
# Windows: Find dan kill process
taskkill /F /IM python.exe  (HATI-HATI! Kill semua Python)

# Linux/Mac: 
lsof -i :8501
kill -9 PID_NUMBER
```

### Error 4: "NLTK stopwords not found"

**Penyebab:** NLTK data belum di-download

**Solusi:**
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

### Error 5: "numpy/pandas build error"

**Penyebah:** Compiler compatibility issue

**Solusi 1:** Upgrade build tools
```bash
pip install --upgrade pip setuptools wheel
```

**Solusi 2:** Install pre-built wheels
```bash
pip install -r requirements.txt --no-build-isolation
```

### Error 6: Aplikasi running tapi tampilan jelek/CSS tidak load

**Penyebab:** Browser cache

**Solusi:**
- Hard refresh: Ctrl+Shift+R (Windows) atau Cmd+Shift+R (Mac)
- Clear browser cache
- Buka di incognito/private mode

### Error 7: Dataset tidak ter-load dengan benar

**Penyebab:** Encoding atau format CSV issue

**Solusi:**
- Pastikan anime.csv tidak ada BOM (Byte Order Mark)
- Cek delimiter sesuai (comma)
- Verifikasi kolom names: anime_id, title, genre, synopsis, rating

---

## 💾 Environment & Development

### Activate Virtual Environment (jika sudah dibuat)

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Deactivate Virtual Environment

```bash
deactivate
```

### List Installed Packages

```bash
pip list
```

### Verify Specific Package Version

```bash
pip show streamlit
```

**Output:**
```
Name: streamlit
Version: 1.36.0
Location: C:\Users\...\Python\Lib\site-packages
```

---

## 🎨 Customization & Configuration

### Gunakan Streamlit Config File

Config sudah tertersedia di `.streamlit/config.toml` untuk:
- Dark mode theme
- Port customization
- Security settings
- Logging configuration

### Edit Config (Optional)

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#ff006e"        # Warna accent
backgroundColor = "#0a0e27"     # Background
textColor = "#e0e0e0"          # Text color

[server]
port = 8501                    # Port default
headless = false              # Run di browser

[client]
toolbarMode = "minimal"       # Toolbar minimal
```

### Restart aplikasi setelah edit config:
```bash
streamlit run app.py
```

---

## 📈 Performance Optimization

### Jika aplikasi lambat:

1. **Clear Streamlit cache:**
```bash
streamlit cache clear
```

2. **Restart Python process:**
```
Ctrl+C di terminal untuk stop
streamlit run app.py untuk restart
```

3. **Reduce features (untuk laptop lama):**
   - Edit app.py baris TfidfVectorizer:
   ```python
   TfidfVectorizer(max_features=250)  # Kurang dari 500
   ```

4. **Monitor resource:**
   - Open Task Manager (Ctrl+Shift+Esc)
   - Check CPU & Memory usage
   - Jika terlalu tinggi, restart browser

---

## 🌐 Deployment (Production)

### Deploy ke Streamlit Cloud (Free)

1. Push code ke GitHub
2. Visit: https://share.streamlit.io/
3. Connect GitHub account
4. Select repository & branch
5. Deploy otomatis

### Deploy ke Server (Self-hosted)

**Requirements:**
- Linux server (Debian/Ubuntu recommended)
- Python 3.8+
- Port 8501 accessible

**Commands:**
```bash
# SSH ke server
ssh user@server_ip

# Clone/upload repository
git clone <your-repo-url>
cd SRIPSI

# Install dependencies
pip install -r requirements.txt

# Run in background
nohup streamlit run app.py &

# Atau gunakan supervisor:
sudo apt-get install supervisor
# Config supervisor untuk auto-restart
```

---

## 📞 Support & Help

### Jika ada masalah:

1. **Check requirements.txt** - Semua library installed?
2. **Check Python version** - Python 3.8+?
3. **Read terminal error** - Lihat error message dengan teliti
4. **Google error message** - Biasanya ada solusi di SO
5. **Check anime.csv** - File valid dan ada?
6. **Verify folder structure** - Struktur sesuai dokumentasi?

### Terminal Logs:

Streamlit menyimpan logs. Check:

**Windows:**
```
C:\Users\<USERNAME>\.streamlit\
```

**Linux/Mac:**
```
~/.streamlit/
```

---

## ✅ Maintenance

### Regular Updates (Recommended)

```bash
# Update pip
pip install --upgrade pip

# Update dependencies (HATI-HATI! bisa break things)
pip install --upgrade -r requirements.txt

# Atau update specific package
pip install --upgrade streamlit
```

### Backup & Version Control

```bash
# Initialize git repository (sekali)
git init
git add .
git commit -m "Initial commit"

# Push ke GitHub untuk backup
git push origin main
```

---

## 📝 Checklist Sebelum Submit Skripsi

- [ ] Aplikasi running tanpa error
- [ ] Semua 5 halaman berfungsi
- [ ] Dataset terload dengan benar
- [ ] Rekomendasi logis dan relevan
- [ ] UI clean dan professional looking
- [ ] README lengkap
- [ ] Kode ter-comment dengan baik
- [ ] PENJELASAN_ALGORITMA.md terisi lengkap
- [ ] requirements.txt updated
- [ ] Tested di laptop lain (optional tapi recommended)

---

**Happy Running! 🎌**

Jika berhasil running, next step adalah **customize dataset** dengan anime yang lebih menarik atau **menambah features** sesuai kebutuhan skripsi Anda.
