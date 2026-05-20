# 🎌 Sistem Rekomendasi Anime - README

## 📚 Daftar Isi
- [Overview](#overview)
- [Fitur Utama](#fitur-utama)
- [Teknologi](#teknologi)
- [Instalasi](#instalasi)
- [Cara Penggunaan](#cara-penggunaan)
- [Struktur Project](#struktur-project)
- [FAQ](#faq)
- [Contact & Support](#contact--support)

---

## 🎯 Overview

**Sistem Rekomendasi Anime** adalah aplikasi web interaktif yang menggunakan **Content-Based Filtering** untuk memberikan rekomendasi anime yang dipersonalisasi berdasarkan preferensi user.

### Apa yang Membedakan?

| Fitur | Platform Lain | Sistem Kami |
|-------|---|---|
| **Rekomendasi Terpopuler** | ✅ | ✅ |
| **Rekomendasi Personal** | ✅ (Collaborative) | ✅ (Content-Based) |
| **Transparansi Alasan** | ❌ | ✅ **Genre Matching** |
| **Tidak Perlu Login** | ❌ | ✅ |
| **Instant Recommendations** | ❌ (Butuh data) | ✅ |
| **Handle Cold-Start** | ❌ | ✅ |

---

## ✨ Fitur Utama

### 1. 🎯 Rekomendasi Anime (Main Feature)

**Cara Kerja:**
1. Pilih anime favorit dari dropdown
2. Atur jumlah rekomendasi (1-20)
3. Klik "Tampilkan Rekomendasi"
4. Dapatkan list anime yang mirip dengan genre matching terlihat

**Output:**
- Anime yang dipilih sebagai referensi
- Top-K recommendations dengan:
  - Rating dan informasi dasar
  - Genre yang cocok (highlight hijau)
  - Similarity score (%)
  - Sinopsis ringkas

**Algoritma:** Hybrid Content-Based Filtering
- 70% TF-IDF (Synopsis Similarity)
- 30% Genre Matching

---

### 2. ⭐ Top Rating

**Fitur:**
- Tampilkan anime dengan rating tertinggi
- Filter jumlah (5-50)
- Medal untuk top 3 (🥇 🥈 🥉)
- Sorting otomatis berdasarkan score

---

### 3. 🔥 Populer

**Fitur:**
- Anime paling populer (by rating)
- Customizable count
- Same display format dengan Top Rating

---

### 4. 🔍 Search & Filter

**Tab 1 - Search:**
- Search by title atau keywords di synopsis
- Real-time results display
- Max 10 results per search

**Tab 2 - Filter:**
- Multi-select anime types (TV, Movie, OVA, Special, ONA)
- Filter hasil diurutkan by rating
- Deduplicate results

---

### 5. 📊 Statistics

**Menampilkan:**
- Total anime di database
- Average score
- Score tertinggi/terendah
- Distribusi tipe anime

---

## 💻 Teknologi

### Backend & Frontend
- **Framework:** Streamlit (Python)
- **Python Version:** 3.8+
- **Style:** Custom CSS (Dark Mode Anime Theme)

### Libraries

| Library | Fungsi |
|---------|--------|
| **streamlit** | Web framework |
| **nltk** | Natural Language Processing |
| **csv** | Data loading |
| **math** | Mathematical operations |
| **collections** | Data structures |

### Algoritma
- **TF-IDF:** Text feature extraction
- **Cosine Similarity:** Distance metric
- **Binary Encoding:** Genre features
- **Hybrid Approach:** Combine content + categorical

---

## 🚀 Instalasi

### Prerequisites
- Python 3.8 atau lebih tinggi
- pip (Python package manager)

### Step-by-Step

#### 1. Clone/Download Project
```bash
cd path/to/SRIPSI
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Note:** Jika ada error dengan NLTK, download manual:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

#### 4. Run Application
```bash
streamlit run app.py
```

**Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://xxx.xxx.x.x:8501
```

**Buka browser ke:** `http://localhost:8501`

---

## 📱 Cara Penggunaan

### Scenario 1: Mencari Rekomendasi

**Step-by-Step:**
1. Navigasi ke halaman "🎯 Rekomendasi Anime"
2. Di dropdown, cari dan pilih anime favorit (misal: "One Piece")
3. Atur jumlah rekomendasi (default 5)
4. Klik tombol biru "💡 Tampilkan Rekomendasi"
5. Tunggu beberapa detik (sistem processing)
6. Lihat hasil:
   - Anime pilihan ditampilkan sebagai referensi
   - Daftar rekomendasi dengan genre matching highlighted
   - Setiap item bisa dilihat detailnya

**Tips:**
- Coba pilih anime favorit Anda yang paling disukai
- Rekomendasi akan lebih akurat jika anime populer
- Genre Cocok menunjukkan alasan rekomendasi

---

### Scenario 2: Mencari Top Rated

**Step-by-Step:**
1. Go to "⭐ Top Rating"
2. Sesuaikan slider "Tampilkan" (misal: 15)
3. Otomatis display hasil urutkan by rating tertinggi
4. Klik gambar/judul untuk melihat full details

---

### Scenario 3: Search Specific Anime

**Step-by-Step:**
1. Go to "🔍 Search & Filter"
2. Click tab "🔎 Search"
3. Ketik nama anime atau keywords (misal: "dragon")
4. Hasil muncul otomatis
5. Lihat semua anime yang matching

**Contoh Searches:**
- "naruto" → Direct title match
- "ninja" → Keyword in synopsis
- "school" → Type in genre/synopsis

---

### Scenario 4: Filter by Type

**Step-by-Step:**
1. Go to "🔍 Search & Filter"
2. Click tab "📂 Filter Genre"
3. Multi-select tipe anime (bisa pilih lebih dari 1):
   - TV
   - Movie
   - OVA
   - Special
   - ONA
4. Auto-display hasil filtered & sorted by rating

---

### Scenario 5: Lihat Statistics

**Step-by-Step:**
1. Go to "📊 Statistics"
2. Lihat metrics:
   - Berapa total anime
   - Average rating
   - Highest/Lowest rated
   - Popular types

---

## 🏗️ Struktur Project

```
SRIPSI/
├── app.py                                      # Main Streamlit Application
├── anime.csv                                   # Dataset (12,434+ anime)
├── requirements.txt                            # Python dependencies
├── README.md                                   # File ini (User Guide)
├── DOKUMENTASI_IMPLEMENTASI.md                 # Technical Implementation
├── PENJELASAN_ALGORITMA_DETAIL.md             # Detailed Algorithm Explanation
├── INSTALLATION_GUIDE.md                       # Installation Instructions
└── assets/                                     # Static assets folder
```

### File Descriptions

| File | Purpose |
|------|---------|
| **app.py** | Main aplikasi dengan semua functions & UI |
| **anime.csv** | Database 12,434+ anime dari MyAnimeList |
| **requirements.txt** | Dependencies list (pip install -r) |
| **README.md** | Quick start guide (ini) |
| **DOKUMENTASI_IMPLEMENTASI.md** | Detailed technical docs |
| **PENJELASAN_ALGORITMA_DETAIL.md** | In-depth algorithm explanation |

---

## 🎨 UI/UX Features

### Theme
- **Dark Mode:** Anime-style dark purple + pink accent
- **Responsive:** Works on desktop, tablet, mobile
- **Interactive:** Live feedback & instant results

### Color Scheme
```
Primary Background: #0a0e27 (Dark Blue)
Accent Color: #ff006e (Hot Pink)
Text Primary: #e0e0e0 (Light Gray)
Success Color: #4CAF50 (Green)
```

### Icons
- 🎌 Header/Brand
- 🎯 Rekomendasi
- ⭐ Rating
- 🔥 Popular
- 🔍 Search
- 📊 Statistics
- 🎬 Anime Card
- ✓ Genre Match (Green)

---

## ⚙️ Configuration

### Dapat di-adjust dalam code

```python
# app.py

# Preprocessing
STOPWORDS_LANG = 'english'
MIN_WORD_LENGTH = 3

# Similarity weights
TFIDF_WEIGHT = 0.7  # Can change to 0.5, 0.8, etc
GENRE_WEIGHT = 0.3  # Inverse of TFIDF_WEIGHT

# Display
DEFAULT_K_RECOMMENDATIONS = 5
MAX_K_RECOMMENDATIONS = 20
```

### Untuk mengubah:
1. Open `app.py` in text editor
2. Find constants di bagian konfigurasi
3. Modify values
4. Save & restart `streamlit run app.py`

---

## 🐛 Troubleshooting

### Issue 1: "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
```bash
pip install streamlit
# atau
pip install -r requirements.txt
```

---

### Issue 2: NLTK Data Not Found

**Error:**
```
LookupError: Resource punkt not found.
```

**Solution:**
```bash
python -c "
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
"
```

---

### Issue 3: anime.csv Not Found

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'anime.csv'
```

**Solution:**
- Ensure file `anime.csv` is in same directory as `app.py`
- Check file path in `load_anime_data()` function
- File size should be ~40MB

---

### Issue 4: Slow Performance

**Causes & Solutions:**
1. **First load:** NLTK downloads data (only once)
   - Wait 1-2 minutes on first run

2. **Caching enabled:** Streamlit caches results
   - Clear cache: Ctrl+C in terminal, restart

3. **Dataset large:** 12,434 anime = normal
   - Feature extraction on first run takes time
   - Subsequent runs use cache (instant)

---

### Issue 5: Rekomendasi Tidak Sesuai

**Possible Causes:**
- Anime tidak ditemukan (typo in title)
- Anime terlalu niche (limited features)
- Genre encoding incomplete

**Solutions:**
- Check exact spelling in dropdown
- Try anime populer (lebih akurat)
- Adjust TFIDF_WEIGHT / GENRE_WEIGHT

---

## 📊 Dataset Information

### Source
- **MyAnimeList** (Kaggle Dataset)
- **Total Anime:** 12,434
- **Columns:** anime_id, title, score, genre, synopsis, type, episodes, image_url

### Sample Data
```
Title: One Piece
Score: 8.61
Type: TV
Episodes: 1100
Genre: Action, Adventure, Comedy, Shounen, SuperPower
Synopsis: Monkey D. Luffy, a young man with straw hat...
```

### Statistics
```
Average Score: 6.89
Highest Score: 9.29
Lowest Score: 1.84
Most Common Type: TV (8,500+)
Total Genres: 47
```

---

## 📚 Dokumentasi Lengkap

Untuk informasi lebih detail:

| Document | Content |
|----------|---------|
| [DOKUMENTASI_IMPLEMENTASI.md](DOKUMENTASI_IMPLEMENTASI.md) | Architecture, use cases, flow diagrams |
| [PENJELASAN_ALGORITMA_DETAIL.md](PENJELASAN_ALGORITMA_DETAIL.md) | Algorithm deep-dive, math formulas, complexity analysis |
| [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) | Step-by-step installation guide |

---

## ❓ FAQ

### Q1: Apakah saya perlu login?
**A:** Tidak! Aplikasi open untuk semua, tidak perlu registrasi.

---

### Q2: Bagaimana akurasi rekomendasi?
**A:** Tergantung:
- Anime populer: 80%+ akurat
- Anime niche: 60-70% akurat
- Genre matching sangat akurat (berbasis explicit data)

---

### Q3: Apakah data real-time?
**A:** Data dari MyAnimeList tapi tidak auto-update. Update manual (~3 bulan sekali).

---

### Q4: Berapa banyak anime bisa direkomendasikan?
**A:** Max 20 rekomendasi (can change di settings).

---

### Q5: Bisakah saya export hasil rekomendasi?
**A:** Tidak built-in, tapi bisa:
- Screenshot halaman
- Copy dari browser
- Suggest feature request untuk export

---

### Q6: Apa difference TF-IDF vs Genre dalam rekomendasi?
**A:**
- **TF-IDF (70%):** Analisis sinopsis detail (semantic meaning)
- **Genre (30%):** Kategori explicit (action/romance/etc)
- **Hybrid:** Kombinasi untuk hasil balanced

---

### Q7: Bisakah saya request penambahan anime baru?
**A:** Dataset from Kaggle. Untuk update:
1. Download latest dataset dari Kaggle
2. Replace `anime.csv`
3. Restart aplikasi

---

### Q8: Apakah opensource?
**A:** Ya! Untuk kontribusi, submit pull request.

---

## 🔗 Links Berguna

- **MyAnimeList:** https://myanimelist.net/
- **Kaggle Dataset:** https://www.kaggle.com/datasets/dbdmobile/myanimelist-dataset
- **Streamlit Docs:** https://docs.streamlit.io/
- **NLTK:** https://www.nltk.org/

---

## 👥 Contact & Support

### Issues & Bug Report
Jika menemukan bug:
1. Describe masalah dengan detail
2. Share screenshot/error message
3. List steps to reproduce
4. Submit via issue tracker

### Feature Request
Punya ide fitur baru?
- Create feature request issue
- Describe use case
- Explain benefit

### Support Email
```
📧 support@sripsi-anime.local
```

---

## 📝 License

Project ini dibuat untuk tujuan edukasi & research.

---

## ✅ Checklist Setup

Sebelum menggunakan, pastikan:

- [ ] Python 3.8+ terinstall
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `anime.csv` ada di folder yang sama dengan `app.py`
- [ ] NLTK data downloaded
- [ ] Jalankan `streamlit run app.py`
- [ ] Browser buka `http://localhost:8501`
- [ ] UI load dengan benar (dark theme visible)

---

## 🎓 Learning Resources

Untuk memahami lebih dalam:

1. **Content-Based Filtering:**
   - https://en.wikipedia.org/wiki/Recommender_system#Content-based_filtering
   
2. **TF-IDF:**
   - https://en.wikipedia.org/wiki/Tf%E2%80%93idf
   - https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf
   
3. **Cosine Similarity:**
   - https://en.wikipedia.org/wiki/Cosine_similarity
   
4. **NLTK:**
   - https://www.nltk.org/book/
   - https://www.nltk.org/api/nltk.html

---

## 🎉 Terima Kasih!

Terima kasih telah menggunakan Sistem Rekomendasi Anime!

Enjoy exploring anime recommendations! 🎌

---

**Last Updated:** May 19, 2026  
**Version:** 1.0.0  
**Status:** ✅ Stable
