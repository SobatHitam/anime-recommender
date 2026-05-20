# 📚 Penjelasan Algoritma - Content-Based Filtering

Dokumen ini menjelaskan algoritma yang digunakan dalam Sistem Rekomendasi Anime menggunakan **Content-Based Filtering** dengan **TF-IDF** dan **Cosine Similarity**.

## 📖 Daftar Isi

1. [Pengenalan Content-Based Filtering](#pengenalan-content-based-filtering)
2. [TF-IDF (Term Frequency-Inverse Document Frequency)](#tf-idf)
3. [Cosine Similarity](#cosine-similarity)
4. [Text Preprocessing](#text-preprocessing)
5. [Implementasi di Python](#implementasi-di-python)
6. [Contoh Perhitungan Manual](#contoh-perhitungan-manual)
7. [Diagram Alur Sistem](#diagram-alur-sistem)

---

## 🎯 Pengenalan Content-Based Filtering

### Definisi
Content-Based Filtering adalah metode rekomendasi yang memberikan rekomendasi berdasarkan **karakteristik/konten dari item itu sendiri**, bukan berdasarkan perilaku pengguna lain.

### Prinsip Kerja
```
User memilih Anime A
↓
Sistem menganalisis karakteristik (konten) Anime A
↓
Sistem mencari anime lain dengan karakteristik mirip
↓
Sistem merekomendasikan anime yang mirip
```

### Keuntungan
- ✅ Tidak memerlukan data perilaku pengguna lain
- ✅ Cocok untuk item baru yang belum ada rating
- ✅ Transparan: mudah dijelaskan mengapa item direkomendasikan
- ✅ Tidak ada masalah "cold start" untuk user baru

### Kerugian
- ❌ Tidak bisa menangkap selera unik user
- ❌ Cenderung merekomendasikan item yang terlalu mirip (kurang diversitas)
- ❌ Bergantung pada kualitas deskripsi konten

---

## 🔤 TF-IDF (Term Frequency-Inverse Document Frequency)

### Definisi
TF-IDF adalah teknik untuk mengkonversi text menjadi **representasi numerik (vector)** yang menunjukkan kepentingan setiap kata dalam dokumen.

### Rumus TF-IDF

```
TF-IDF(t,d) = TF(t,d) × IDF(t)

Dimana:
- TF (Term Frequency) = berapa sering term t muncul di dokumen d
- IDF (Inverse Document Frequency) = seberapa unik term t di seluruh dokumen
```

### A. Term Frequency (TF)

**Rumus:**
```
TF(t,d) = (frekuensi term t di dokumen d) / (total term di dokumen d)
```

**Contoh:**
```
Dokumen: "anime action adventure anime"
Total term: 4
- Frekuensi "anime": 2
- Frekuensi "action": 1
- Frekuensi "adventure": 1

TF("anime") = 2/4 = 0.5
TF("action") = 1/4 = 0.25
TF("adventure") = 1/4 = 0.25
```

**Interpretasi:** Kata "anime" lebih penting dalam dokumen ini karena muncul lebih sering.

### B. Inverse Document Frequency (IDF)

**Rumus:**
```
IDF(t) = log(N / df(t))

Dimana:
- N = total dokumen dalam corpus
- df(t) = berapa dokumen yang mengandung term t
```

**Contoh (misal total 100 anime):**
```
- "anime" muncul di 99 anime → IDF("anime") = log(100/99) ≈ 0.01
- "thriller" muncul di 10 anime → IDF("thriller") = log(100/10) ≈ 1.0
- "supernatural" muncul di 5 anime → IDF("supernatural") = log(100/5) ≈ 2.996
```

**Interpretasi:** Kata langka ("supernatural") lebih bernilai daripada kata umum ("anime").

### C. Perhitungan Akhir TF-IDF

**Rumus:**
```
TF-IDF(t,d) = TF(t,d) × IDF(t)
```

**Contoh lengkap:**
```
Dokumen: "anime action adventure anime"
N = 100 anime dalam database

TF-IDF("anime") = 0.5 × 0.01 = 0.005
TF-IDF("action") = 0.25 × 1.5 = 0.375
TF-IDF("adventure") = 0.25 × 1.8 = 0.450
```

### D. Output TF-IDF: Vector Representasi

```
Dokumen direpresentasikan sebagai vector:
[0.005, 0.375, 0.450, 0, 0, ..., 0]  ← 500-dimensional vector (500 kata unik)

Setiap dimensi mewakili satu kata dalam vocabulary.
Nilai menunjukkan kepentingan kata tersebut dalam dokumen.
```

### Implementasi di Python

```python
from sklearn.feature_extraction.text import TfidfVectorizer

# Contoh dataset
documents = [
    "anime action adventure",
    "anime comedy slice of life",
    "thriller psychological dark"
]

# Buat TF-IDF vectorizer
vectorizer = TfidfVectorizer(max_features=500, min_df=1, max_df=0.8)

# Fit dan transform untuk dapatkan TF-IDF matrix
tfidf_matrix = vectorizer.fit_transform(documents)

# tfidf_matrix shape: (3, n_features)
# Setiap baris adalah dokumen
# Setiap kolom adalah term/kata
```

---

## 📐 Cosine Similarity

### Definisi
Cosine Similarity mengukur **sudut (angle) antara dua vector** untuk menentukan kesamaan mereka. Range nilai: **0 hingga 1**.

```
0 = sangat berbeda (sudut 90°)
1 = identik (sudut 0°)
```

### Rumus Cosine Similarity

```
Similarity(A, B) = (A · B) / (||A|| × ||B||)

Dimana:
- A · B = dot product (hasil perkalian skalar)
- ||A|| = magnitude/norm vector A = √(a₁² + a₂² + ... + aₙ²)
- ||B|| = magnitude/norm vector B = √(b₁² + b₂² + ... + bₙ²)
```

### Contoh Perhitungan Manual

**Data:**
```
Vector A (Anime "Attack on Titan"): [0.5, 0.3, 0.2, 0, 0.1]
Vector B (Anime "Demon Slayer"):    [0.4, 0.35, 0.1, 0.05, 0.1]
```

**Langkah 1: Hitung Dot Product (A · B)**
```
A · B = (0.5 × 0.4) + (0.3 × 0.35) + (0.2 × 0.1) + (0 × 0.05) + (0.1 × 0.1)
      = 0.20 + 0.105 + 0.02 + 0 + 0.01
      = 0.335
```

**Langkah 2: Hitung Magnitude Vector A (||A||)**
```
||A|| = √(0.5² + 0.3² + 0.2² + 0² + 0.1²)
      = √(0.25 + 0.09 + 0.04 + 0 + 0.01)
      = √0.39
      = 0.624
```

**Langkah 3: Hitung Magnitude Vector B (||B||)**
```
||B|| = √(0.4² + 0.35² + 0.1² + 0.05² + 0.1²)
      = √(0.16 + 0.1225 + 0.01 + 0.0025 + 0.01)
      = √0.305
      = 0.552
```

**Langkah 4: Hitung Cosine Similarity**
```
Similarity = 0.335 / (0.624 × 0.552)
           = 0.335 / 0.344
           = 0.974
```

**Interpretasi:** "Attack on Titan" dan "Demon Slayer" memiliki similarity **0.974** (97.4%) → sangat mirip!

### Implementasi di Python

```python
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Vector dari dua anime
anime_a = np.array([0.5, 0.3, 0.2, 0, 0.1]).reshape(1, -1)
anime_b = np.array([0.4, 0.35, 0.1, 0.05, 0.1]).reshape(1, -1)

# Hitung cosine similarity
similarity = cosine_similarity(anime_a, anime_b)
# Output: [[0.973]]

# Untuk matrix
similarity_matrix = cosine_similarity(tfidf_matrix)
# Shape: (n_anime, n_anime)
# similarity_matrix[0, 1] = similarity antara anime 0 dan anime 1
```

---

## 🔤 Text Preprocessing

### Mengapa Preprocessing Penting?

Text raw mengandung noise yang mengganggu:
- ❌ Uppercase/lowercase inconsistency
- ❌ Simbol dan karakter khusus
- ❌ Stopwords (kata umum seperti "the", "a", "is")
- ❌ Whitespace berlebihan

### Langkah-Langkah Preprocessing

#### 1. Lowercase Conversion
```
Input:  "Attack on Titan - An AMAZING Anime!"
Output: "attack on titan - an amazing anime!"
```

**Tujuan:** Normalisasi, sehingga "Titan" dan "titan" dianggap sama kata.

#### 2. Remove Special Characters & URLs
```
Input:  "Check out https://anime.com! This is EPIC!!!123"
Output: "Check out this is EPIC"
```

**Regex Pattern:** `r'http\S+|www\S+|[^a-zA-Z\s]'`

**Tujuan:** Hapus URL dan angka/simbol yang tidak berguna.

#### 3. Stopword Removal
```
Stopwords: "the", "is", "a", "an", "and", "or", "but", "in", "on", "at", ...

Input:  "the cat is on the mat"
Output: "cat mat"
```

**Tujuan:** Fokus pada kata-kata bermakna (content words), bukan filler words.

#### 4. Whitespace Normalization
```
Input:  "anime   is    great"  (multiple spaces)
Output: "anime is great"       (single spaces)
```

**Tujuan:** Konsistensi format.

### Implementasi di Python

```python
import nltk
from nltk.corpus import stopwords
import re

# Download data NLTK (jalankan sekali)
nltk.download('stopwords')

def preprocess_text(text):
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # 3. Remove special characters & numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # 4. Normalize whitespace
    text = ' '.join(text.split())
    
    # 5. Remove stopwords
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word not in stop_words])
    
    return text

# Testing
raw_text = "The Amazing Attack on Titan - The BEST anime!!!"
processed = preprocess_text(raw_text)
# Output: "amazing attack titan best anime"
```

---

## 💻 Implementasi di Python

### Complete Pipeline

```python
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
nltk.download('stopwords')

# ===== STEP 1: Load Data =====
df = pd.read_csv('anime.csv')
# Columns: anime_id, title, genre, synopsis, rating

# ===== STEP 2: Prepare Content =====
df['content'] = df['genre'] + ' ' + df['synopsis']

# ===== STEP 3: Preprocess =====
from nltk.corpus import stopwords
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join(text.split())
    stop_words = set(stopwords.words('english'))
    text = ' '.join([w for w in text.split() if w not in stop_words])
    return text

df['content_processed'] = df['content'].apply(preprocess_text)

# ===== STEP 4: Create TF-IDF Matrix =====
tfidf_vectorizer = TfidfVectorizer(max_features=500)
tfidf_matrix = tfidf_vectorizer.fit_transform(df['content_processed'])

# ===== STEP 5: Get Recommendations =====
def get_recommendations(anime_title, n=5):
    # Find anime index
    anime_idx = df[df['title'] == anime_title].index[0]
    
    # Calculate similarities
    similarities = cosine_similarity(tfidf_matrix[anime_idx], tfidf_matrix).flatten()
    
    # Get top similar (exclude the selected anime itself)
    similar_indices = similarities.argsort()[::-1][1:n+1]
    
    # Return recommendations
    recommendations = df.iloc[similar_indices][['title', 'rating', 'genre']]
    recommendations['similarity'] = similarities[similar_indices]
    return recommendations

# ===== USAGE =====
result = get_recommendations('Attack on Titan', n=5)
print(result)
```

### Output Contoh:
```
                 title  rating                     genre  similarity
1       Jujutsu Kaisen     8.7  Action|Drama|Shounen|... 0.874
2       Demon Slayer     8.7  Action|Shounen|... 0.851
3          Bleach        7.9  Action|Shounen|... 0.823
4    My Hero Academia    8.3  Action|School|Shounen|... 0.801
5       Hunter x Hunter   8.6  Action|Shounen|... 0.787
```

---

## 🧮 Contoh Perhitungan Manual - Lengkap

Mari kita proses dari awal dengan 3 anime sample.

### Dataset Awal
```
1. "Attack on Titan"
   Genre: Action Drama
   Synopsis: Giant creatures attack humanity

2. "Slice of Life School Comedy"
   Genre: Comedy School
   Synopsis: Students experience daily school life

3. "Supernatural Thriller Drama"
   Genre: Supernatural Thriller
   Synopsis: Ghost hunters face scary creatures
```

### Step 1: Bentuk Content

```
Anime 1: "action drama giant creatures attack humanity"
Anime 2: "comedy school students experience daily school life"
Anime 3: "supernatural thriller ghost hunters face scary creatures"
```

### Step 2: Identify Unique Terms (Vocabulary)
```
Vocabulary (16 terms, sorted):
[1] attack
[2] comedy
[3] creatures
[4] daily
[5] drama
[6] experience
[7] face
[8] ghost
[9] giant
[10] hunters
[11] humanity
[12] life
[13] school
[14] scary
[15] students
[16] supernatural
[17] thriller
```

### Step 3: Calculate TF for Each Anime

**Anime 1:** "action drama giant creatures attack humanity" (6 words)
```
action: 1/6 = 0.167
attack: 1/6 = 0.167
creatures: 1/6 = 0.167
drama: 1/6 = 0.167
giant: 1/6 = 0.167
humanity: 1/6 = 0.167
```

**Anime 2:** "comedy school students experience daily school life" (7 words)
```
comedy: 1/7 = 0.143
daily: 1/7 = 0.143
experience: 1/7 = 0.143
life: 1/7 = 0.143
school: 2/7 = 0.286  ← "school" muncul 2x
students: 1/7 = 0.143
```

**Anime 3:** "supernatural thriller ghost hunters face scary creatures" (7 words)
```
creatures: 1/7 = 0.143
face: 1/7 = 0.143
ghost: 1/7 = 0.143
hunters: 1/7 = 0.143
scary: 1/7 = 0.143
supernatural: 1/7 = 0.143
thriller: 1/7 = 0.143
```

### Step 4: Calculate IDF for Each Term

**Asumsi:** Kita punya 100 anime dalam database total

```
Term              Count  IDF = log(100 / count)
attack            5      log(100/5) = 2.996
comedy            15     log(100/15) = 1.897
creatures         8      log(100/8) = 2.525
daily             3      log(100/3) = 3.507
drama             20     log(100/20) = 1.609
experience        2      log(100/2) = 3.912
face              1      log(100/1) = 4.605
ghost             1      log(100/1) = 4.605
giant             2      log(100/2) = 3.912
hunters           1      log(100/1) = 4.605
humanity          1      log(100/1) = 4.605
life              10     log(100/10) = 2.303
school            12     log(100/12) = 2.120
scary             1      log(100/1) = 4.605
students          2      log(100/2) = 3.912
supernatural      3      log(100/3) = 3.507
thriller          2      log(100/2) = 3.912
```

### Step 5: Calculate TF-IDF

**Anime 1 - TF-IDF Vector:**
```
[0, 0, 0.167×2.525, 0, 0.167×1.609, 0, 0, 0, 0.167×3.912, 0, 0.167×4.605, 0, 0, 0, 0, 0, 0]
= [0, 0, 0.421, 0, 0.269, 0, 0, 0, 0.653, 0, 0.768, 0, 0, 0, 0, 0, 0]
```

**Anime 2 - TF-IDF Vector:**
```
[0, 0.143×1.897, 0, 0.143×3.507, 0, 0.143×3.912, 0, 0, 0, 0, 0, 0.143×2.303, 0.286×2.120, 0, 0.143×3.912, 0, 0]
= [0, 0.272, 0, 0.502, 0, 0.560, 0, 0, 0, 0, 0, 0.329, 0.607, 0, 0.560, 0, 0]
```

**Anime 3 - TF-IDF Vector:**
```
[0, 0, 0.143×2.525, 0, 0, 0, 0.143×4.605, 0.143×4.605, 0, 0.143×4.605, 0, 0, 0, 0.143×4.605, 0, 0.143×3.507, 0.143×3.912]
= [0, 0, 0.361, 0, 0, 0, 0.659, 0.659, 0, 0.659, 0, 0, 0, 0.659, 0, 0.502, 0.560]
```

### Step 6: Calculate Cosine Similarity

**Similarity antara Anime 1 & Anime 3:**

```
Dot Product (A1 · A3):
= 0×0 + 0×0 + 0.421×0.361 + ... (semua term)
= 0.152 (only 'creatures' term overlap yang significant)

Magnitude A1 (||A1||):
= √(0² + 0² + 0.421² + 0² + 0.269² + ... )
= √(0.177 + 0.072 + 0.426 + 0.590)
= √1.265 = 1.125

Magnitude A3 (||A3||):
= √(0² + 0² + 0.361² + ... + 0.560²)
= √(0.130 + 0.434 + 0.434 + 0.434 + 0.252 + 0.314)
= √1.998 = 1.414

Cosine Similarity = 0.152 / (1.125 × 1.414)
                 = 0.152 / 1.591
                 = 0.096 (≈ 9.6%) ← Anime 1 & 3 tidak mirip!
```

**Similarity antara Anime 1 & Anime 2:**
```
Dot Product: ≈ 0.000 (tidak ada term yang sama)
Cosine Similarity ≈ 0.0 ← Sama sekali tidak mirip (akurat!)
```

---

## 📊 Diagram Alur Sistem

```
┌─────────────────────────────────────────────────────────────────┐
│            SISTEM REKOMENDASI ANIME - CONTENT-BASED             │
└─────────────────────────────────────────────────────────────────┘

USER INTERFACE (Streamlit)
    │
    ├── [Halaman 1] Rekomendasi Anime
    ├── [Halaman 2] Top Rating
    ├── [Halaman 3] Populer
    ├── [Halaman 4] Search & Filter
    └── [Halaman 5] Statistics
    
    │
    ▼
DATA LOADING & CACHING (@st.cache_data)
    │
    ├── Load anime.csv
    ├── Fill missing values
    ├── Combine genre + synopsis → content
    │
    ▼
TEXT PREPROCESSING (@st.cache_resource)
    │
    ├── Lowercase conversion
    ├── Remove URLs & special chars
    ├── Normalize whitespace
    ├── Stopword removal (NLTK)
    │
    ▼
TF-IDF VECTORIZATION (@st.cache_resource)
    │
    ├── Create TfidfVectorizer
    ├── Fit & transform content_processed
    ├── Generate TF-IDF matrix (n_anime × n_features)
    │
    ▼
SIMILARITY CALCULATION
    │
    ├── User selects anime A
    ├── Get anime A TF-IDF vector
    ├── Calculate cosine_similarity(A, all_anime)
    ├── Sort by similarity score descending
    ├── Return top-N recommendations
    │
    ▼
DISPLAY RECOMMENDATIONS (UI)
    │
    ├── Show selected anime info
    ├── Show top-N recommended anime
    ├── Display similarity scores
    ├── Display genre, rating, synopsis
    │
    ▼
USER EXPERIENCE
```

### Data Flow Example

```
Input: User selects "Attack on Titan"

Attack on Titan
    ↓
Content: "action drama fantasy shounen giant creatures..."
    ↓
Preprocessing: "action drama fantasy shounen giant creatures"
    ↓
TF-IDF Vector: [0.15, 0.12, 0.08, 0.10, 0.05, ...]
    ↓
Cosine Similarity with all anime:
    • Jujutsu Kaisen: 0.874
    • Demon Slayer: 0.851
    • Bleach: 0.823
    • My Hero Academia: 0.801
    ↓
Output: Recommend Top-5 ↑
    ↓
Display on UI with cards & styling
```

---

## 🎓 Kesimpulan

### Content-Based Filtering dengan TF-IDF & Cosine Similarity adalah:

1. **Efektif** untuk merekomendasikan item mirip
2. **Scalable** dan cepat untuk dataset besar
3. **Interpretable** - mudah dijelaskan
4. **Simple** namun powerful
5. **Cocok untuk skripsi** karena algoritmanya jelas dan terdokumentasi

### Karakteristik Algoritma:
- ✅ **Tidak perlu interaksi user historis**
- ✅ **Bekerja untuk item baru** (new item problem solved)
- ✅ **Cold start untuk user baru** (solved untuk content-based)
- ❌ **Sulit mendeteksi preferensi unik** (limitation)
- ❌ **Diverse recommendations** (jarang recommend outside preferences)

### Pengembangan Lebih Lanjut:
Untuk meningkatkan sistem, dapat menambahkan:
1. **Hybrid Filtering** (content-based + collaborative)
2. **Deep Learning** (embeddings, neural networks)
3. **Explainable AI** (explain predictions)
4. **User Feedback Loop** (improve over time)

---

*Dokumen ini dibuat untuk keperluan skripsi Sistem Rekomendasi Anime - 2024*
