# 📋 Dokumentasi Implementasi Sistem Rekomendasi Anime

## 🎯 Overview Sistem

Sistem Rekomendasi Anime berbasis **Content-Based Filtering** yang menggabungkan:
- **TF-IDF (Term Frequency-Inverse Document Frequency)** untuk analisis konten text (synopsis)
- **Genre Binary Encoding** untuk fitur kategori
- **Cosine Similarity** untuk perhitungan kemiripan konten
- **Hybrid Similarity** yang menggabungkan kedua fitur (70% TF-IDF + 30% Genre)

---

## 🏗️ Arsitektur Sistem

### Use Case Diagram

```
┌─────────────────────┐
│   Pengguna (User)   │
└─────────────────────┘
          │
    ┌─────┴─────┬──────────┬────────────┐
    │            │          │            │
    ▼            ▼          ▼            ▼
┌───────────┐ ┌────────┐ ┌──────────┐ ┌───────────┐
│ Memasukan │ │ Melihat│ │ Melihat  │ │  Search & │
│   Anime   │ │ Rekomen│ │  Detail  │ │  Filter   │
└───────────┘ └────────┘ └──────────┘ └───────────┘
    │            │          │            │
    └─────────────┴──────────┴────────────┘
                   │
           ┌───────▼────────┐
           │  Sistem Input  │
           │  & Output API  │
           └───────┬────────┘
                   │
         ┌─────────▼──────────┐
         │  Preprocessing     │
         │  - Tokenisasi      │
         │  - Hapus Stopword  │
         │  - Lemmatization   │
         └─────────┬──────────┘
                   │
         ┌─────────▼──────────────────┐
         │  Feature Extraction        │
         │  ┌──────────────────────┐  │
         │  │ TF-IDF (Synopsis)    │  │
         │  ├──────────────────────┤  │
         │  │ Genre Binary Vector  │  │
         │  └──────────────────────┘  │
         └─────────┬──────────────────┘
                   │
         ┌─────────▼──────────────────┐
         │  Similarity Calculation    │
         │  - TF-IDF Cosine Sim      │
         │  - Genre Cosine Sim       │
         │  - Hybrid Combination     │
         └─────────┬──────────────────┘
                   │
         ┌─────────▼──────────────────┐
         │  Ranking & Filtering       │
         │  (Top-K Recommendations)   │
         └─────────┬──────────────────┘
                   │
         ┌─────────▼──────────────────┐
         │  Output Formatting         │
         │  - Rekomendasi List        │
         │  - Genre Matching Info     │
         │  - Similarity Score        │
         └────────────────────────────┘
```

---

## 📊 Flow Diagram Rekomendasi

```
START: User memilih anime favorit
    │
    ▼
LOAD: Data anime + Preprocessing (TF-IDF)
    │
    ├─► Extract Genre Vector (Binary encoding)
    │   - 1.0 jika anime memiliki genre
    │   - 0.0 jika tidak
    │
    ├─► Build TF-IDF Matrix (Synopsis + Genre)
    │   - Term Frequency (TF)
    │   - Inverse Document Frequency (IDF)
    │   - TF-IDF = TF × IDF
    │
    ▼
SEARCH: Cari anime yang dipilih di database
    │
    ▼
EXTRACT: Vektor TF-IDF dan Genre dari anime pilihan
    │
    ▼
CALCULATE SIMILARITY:
    │
    ├─► Untuk setiap anime lain (i ≠ selected):
    │   ├─ TF-IDF Cosine Sim = dot(v1, v2) / (||v1|| × ||v2||)
    │   ├─ Genre Cosine Sim = dot(g1, g2) / (||g1|| × ||g2||)
    │   └─ Hybrid Sim = (TF-IDF × 0.7) + (Genre × 0.3)
    │
    ▼
FIND MATCHING GENRES:
    │
    ├─► Identifikasi genre yang cocok antara dua anime
    │   (Genre yang dimiliki KEDUA anime)
    │
    ▼
RANK & SORT: Urutkan berdasarkan similarity score (tertinggi)
    │
    ▼
RETURN: Top-K recommendations dengan:
    ├─ Judul anime
    ├─ Rating/Score
    ├─ Genre
    ├─ Sinopsis ringkas
    ├─ Similarity score (%)
    └─ Genre yang cocok (highlight)
    │
    ▼
DISPLAY: Tampilkan rekomendasi di UI dengan:
    ├─ Anime yang dipilih (referensi)
    ├─ Daftar rekomendasi bernomor
    ├─ Warna indikator untuk genre cocok
    └─ Persentase kesamaan
    │
    ▼
END: User dapat melihat detail dan memilih anime lain
```

---

## 🔧 Implementasi Teknis

### 1. Data Loading (`load_anime_data()`)

```python
def load_anime_data():
    """
    Load CSV dengan field:
    - anime_id: ID unik anime
    - title: Nama anime
    - score: Rating MyAnimeList (0-10)
    - type: TV, Movie, OVA, Special, ONA
    - episodes: Jumlah episode
    - genre: Genre (comma-separated)
    - synopsis: Deskripsi anime
    - image_url: URL gambar poster
    """
```

**Format CSV:**
```csv
anime_id,title,score,rank,popularity,members,synopsis,start_date,end_date,type,episodes,image_url,genre
28977,Gintama°,9.05,...,TV,51,...
```

---

### 2. Text Preprocessing (`preprocess_text()`)

**Pipeline Preprocessing:**

| Step | Operasi | Contoh |
|------|---------|---------|
| 1 | Lowercase | "The Hero" → "the hero" |
| 2 | Remove URLs | "Visit http://..." → "Visit" |
| 3 | Remove Special Chars | "Hello!" → "Hello" |
| 4 | Remove Extra Spaces | "hello  world" → "hello world" |
| 5 | Remove Stopwords | "the a is" → (dihapus) |
| 6 | Lemmatization | "running" → "run", "children" → "child" |
| 7 | Filter Pendek | Hapus kata < 3 karakter |

**Contoh Preprocessing Synopsis:**
```
Input:
"Hunters devote themselves to accomplishing hazardous tasks, all from traversing 
the world's uncharted territories to locating rare items and monsters."

Output:
"hunters devote accomplishing hazardous tasks traversing worlds uncharted 
territories locating rare items monsters"
```

---

### 3. Feature Extraction

#### A. Genre Feature (Binary Encoding)

```python
def extract_genres(anime_data):
    """
    Untuk setiap genre:
    - 1.0 jika anime memiliki genre
    - 0.0 jika tidak
    
    Contoh:
    Anime: "One Piece"
    Genres: "Action, Adventure, Comedy"
    
    Vector: [1.0, 0.0, 1.0, 0.0, 1.0, ...]
             [Action, Drama, Adventure, Fantasy, Comedy, ...]
    """
```

#### B. TF-IDF Feature (Synopsis + Genre)

**Formula TF-IDF:**
```
TF(term, doc) = (term_frequency) / (total_words_in_doc)
IDF(term) = log(total_documents / documents_containing_term)
TF-IDF = TF × IDF
```

**Contoh Perhitungan:**
```
Term: "adventure"
Doc 1 (One Piece): 
  - TF = 2/100 = 0.02
  - IDF = log(10000/500) = 2.996
  - TF-IDF = 0.02 × 2.996 = 0.0599

Doc 2 (Naruto):
  - TF = 3/150 = 0.02
  - IDF = 2.996 (sama untuk semua)
  - TF-IDF = 0.02 × 2.996 = 0.0599
```

---

### 4. Similarity Calculation

#### A. Cosine Similarity Formula

```
cosine_sim(v1, v2) = (v1 · v2) / (||v1|| × ||v2||)

Dimana:
- v1 · v2 = Σ(v1[i] × v2[i]) [Dot Product]
- ||v|| = √(Σ(v[i]²)) [Magnitude/Norm]
```

**Interpretasi Score:**
- **1.0** = Identical (100% sama)
- **0.5** = Moderate similarity (50% sama)
- **0.0** = Completely different (0% sama)

#### B. Hybrid Similarity

```
hybrid_sim = (tfidf_sim × 0.7) + (genre_sim × 0.3)

Weight:
- 70% dari TF-IDF (Content-based: synopsis)
- 30% dari Genre (Categorical similarity)
```

**Mengapa Hybrid?**
- TF-IDF menangkap kesamaan konten naratif
- Genre memberikan signal kategori eksplisit
- Kombinasi memberikan hasil yang lebih balanced

---

### 5. Matching Genres Function

```python
def get_matching_genres(vec1, vec2, genre_list):
    """
    Identifikasi genre SAMA di antara dua anime
    
    Contoh:
    Anime A: Action, Adventure, Comedy
    Anime B: Action, Fantasy, Comedy
    
    Matching: [Action, Comedy]
    """
```

---

### 6. Recommendation Generation

```python
def get_anime_recommendations(anime_title, anime_data, tf_vectors, 
                             genre_vectors, genre_list, n=5):
    """
    ALGORITMA:
    1. Cari index anime pilihan
    2. Extract vektor TF-IDF dan Genre
    3. Untuk setiap anime lain:
       a. Hitung TF-IDF similarity
       b. Hitung Genre similarity
       c. Hitung Hybrid similarity
       d. Dapatkan matching genres
    4. Sort by similarity (descending)
    5. Return Top-K recommendations
    
    Output: List of {
        'title': str,
        'score': float,
        'type': str,
        'episodes': int,
        'synopsis': str,
        'genre': str,
        'similarity_score': float (0-1),
        'matching_genres': list
    }
    """
```

---

## 📱 User Interface Features

### Halaman 1: 🎯 Rekomendasi Anime

**Input:**
- Dropdown pilih anime favorit
- Number input jumlah rekomendasi (1-20)

**Output:**
- Anime pilihan ditampilkan dengan detail lengkap
- Daftar rekomendasi bernomor dengan:
  - Judul dan poster
  - Rating (⭐ badge)
  - Tipe dan episode count
  - Genre tags (5 terbanyak)
  - **Genre Cocok** (highlighted dengan badge hijau)
  - Similarity percentage
  - Sinopsis ringkas (150 karakter)

**Visualisasi Genre Cocok:**
```
Genre Cocok: ✓ Action ✓ Adventure ✓ Comedy
(Ditampilkan dengan warna hijau untuk highlight)
```

---

### Halaman 2: ⭐ Top Rating

**Fitur:**
- Menampilkan anime dengan rating tertinggi
- Filter jumlah yang ditampilkan (5-50)
- Medal emoji (🥇 🥈 🥉) untuk top 3

---

### Halaman 3: 🔥 Populer

**Fitur:**
- Anime populer (sorted by rating)
- Display count customizable

---

### Halaman 4: 🔍 Search & Filter

**Tab 1 - Search:**
- Text input untuk search title/synopsis
- Hasil live dalam format card

**Tab 2 - Filter Genre:**
- Multi-select anime types (TV, Movie, OVA, dll)
- Display filtered results

---

### Halaman 5: 📊 Statistics

**Metrics:**
- Total anime di database
- Average score
- Highest/Lowest score
- Distribution tipe anime

---

## ⚙️ Konfigurasi & Parameter

### Default Parameters

```python
# Preprocessing
MIN_WORD_LENGTH = 3  # Filter kata < 3 karakter
STOPWORDS_LANG = 'english'

# Similarity Weights
TFIDF_WEIGHT = 0.7  # 70% importance
GENRE_WEIGHT = 0.3  # 30% importance

# Recommendation
DEFAULT_K_RECOMMENDATIONS = 5  # Top-5 default
MAX_K_RECOMMENDATIONS = 20  # Maximum limit
```

---

## 🚀 Cara Menjalankan

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi

```bash
streamlit run app.py
```

Aplikasi akan buka di browser: `http://localhost:8501`

---

## 📁 Struktur File

```
SRIPSI/
├── app.py                              # Main aplikasi Streamlit
├── anime.csv                           # Dataset anime
├── requirements.txt                    # Dependencies
├── DOKUMENTASI_IMPLEMENTASI.md        # File ini
├── PENJELASAN_ALGORITMA.md            # Penjelasan algoritma detail
├── README.md                           # User guide
├── INSTALLATION_GUIDE.md               # Panduan instalasi
└── assets/                             # Static assets
```

---

## 🔍 Validasi & Testing

### Test Cases Rekomendasi

**Test 1: Anime Populer**
```
Input: "One Piece"
Expected: Anime dengan genre Action, Adventure mirip
Contoh: Naruto, Bleach, Jujutsu Kaisen
```

**Test 2: Anime Niche**
```
Input: "Clannad"
Expected: Anime dengan genre Drama, Romance, School
Contoh: Toradora, Angel Beats, Plastic Memories
```

**Test 3: Genre Matching**
```
Anime A: "Action, Adventure, Comedy"
Anime B: "Action, Fantasy, Comedy"
Matching: [Action, Comedy]
```

---

## 🎓 Penjelasan Algoritma (Detail)

### Mengapa Content-Based Filtering?

**Kelebihan:**
1. ✅ Tidak memerlukan collaborative data (interaksi user)
2. ✅ Bisa handle cold-start problem (anime/user baru)
3. ✅ Transparan - pengguna tahu alasan rekomendasi
4. ✅ Bisa customize berdasarkan genre/konten

**Keterbatasan:**
1. ❌ Tidak bisa recommend beyond existing features
2. ❌ Memerlukan feature extraction yang baik
3. ❌ Genre bisa overlap atau subjektif

---

## 📈 Future Improvements

1. **Hybrid Filtering:**
   - Integrasikan collaborative filtering (user ratings)
   - Combine dengan content-based untuk lebih baik

2. **Advanced Features:**
   - Ekstrak karakter utama sebagai feature
   - NLP-based semantic similarity
   - Embeddings (Word2Vec, TF-IDF variations)

3. **User Personalization:**
   - Track user preferences over time
   - Personalized weights (adjust TF-IDF vs Genre ratio)
   - User rating feedback loop

4. **Performance:**
   - Cache similarity matrix untuk faster querying
   - Implement approximate nearest neighbors (ANN)
   - Database optimization

---

## 📞 Support & Documentation

Untuk pertanyaan atau bug report, silakan buka issue di repository.

Dokumentasi lengkap:
- [PENJELASAN_ALGORITMA.md](PENJELASAN_ALGORITMA.md) - Deep dive algoritma
- [README.md](README.md) - User guide
- [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) - Setup instructions

---

**Last Updated:** May 19, 2026  
**Version:** 1.0.0  
**Author:** SRIPSI Team

---
