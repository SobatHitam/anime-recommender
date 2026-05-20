# 🔬 Penjelasan Algoritma Content-Based Filtering

## 📚 Daftar Isi

1. [Pendahuluan](#pendahuluan)
2. [Konsep Dasar](#konsep-dasar)
3. [Tahap 1: Preprocessing](#tahap-1-preprocessing)
4. [Tahap 2: Feature Extraction](#tahap-2-feature-extraction)
5. [Tahap 3: Similarity Calculation](#tahap-3-similarity-calculation)
6. [Tahap 4: Ranking & Rekomendasi](#tahap-4-ranking--rekomendasi)
7. [Contoh Implementasi Step-by-Step](#contoh-implementasi-step-by-step)
8. [Analisis Kompleksitas](#analisis-kompleksitas)

---

## 📖 Pendahuluan

### Apa itu Content-Based Filtering?

**Content-Based Filtering** adalah teknik rekomendasi yang menganalisis **karakteristik konten** (fitur) untuk memberikan rekomendasi yang relevan. Sistem ini bekerja dengan:

1. **Menganalisis fitur konten** yang dimiliki setiap item (anime)
2. **Membandingkan fitur** antara item pilihan dengan item lain
3. **Ranking item** berdasarkan tingkat kemiripan fitur
4. **Memberikan rekomendasi** item dengan fitur paling mirip

### Vs Collaborative Filtering

| Aspek | Content-Based | Collaborative |
|-------|---------------|---------------|
| **Data** | Fitur konten (genre, synopsis) | User-item interactions (ratings) |
| **Cold-Start** | ✅ Mengatasi (genre baru) | ❌ Bermasalah (user/item baru) |
| **Transparansi** | ✅ Tinggi (alasan jelas) | ❌ Black box |
| **Scarcity** | ✅ Baik dengan data sedikit | ❌ Perlu banyak user |
| **Diversity** | ❌ Limited (hanya feature) | ✅ Lebih beragam |

---

## 🧠 Konsep Dasar

### 1. Fitur Konten (Content Features)

Dalam sistem kami, fitur konten terdiri dari:

#### A. Genre (Kategori)
```
Anime: "One Piece"
Genres: [Action, Adventure, Comedy, SuperPower, Shounen]

Vector Representation (Binary):
[Action:1, Adventure:1, Comedy:1, Drama:0, Fantasy:0, ...]
```

**Keuntungan:**
- Mudah dipahami user
- Interpretable (transparent)
- Cepat dihitung

#### B. Synopsis (Deskripsi Teks)
```
Anime: "One Piece"
Synopsis: "Monkey D. Luffy, a pirate, travels the ocean seeking treasure 
and making friends. Along the way, he encounters dangerous foes and 
discovers the secrets of the Grand Line."

→ Setelah preprocessing: "monkey luffy pirate ocean treasure friends encounters"
→ Setelah TF-IDF: [0.12, 0.08, 0.15, ..., 0.03]
```

**Keuntungan:**
- Menangkap semantic meaning
- Kaya akan informasi
- Dapat menemukan pattern tersembunyi

---

### 2. Vektor Representasi

Setiap anime direpresentasikan sebagai **vektor multi-dimensional**:

```
Anime A: [f1, f2, f3, ..., fn]

Dimana:
- n = jumlah dimensi feature (vocabulary size + genre count)
- fi = nilai feature i (TF-IDF score atau binary)
```

**Contoh dengan 5 feature:**
```
Anime A (One Piece):  [0.5, 0.3, 0.8, 0.2, 0.1]
Anime B (Naruto):     [0.4, 0.35, 0.7, 0.25, 0.15]
Anime C (Code Geass): [0.1, 0.05, 0.2, 0.9, 0.8]
```

---

### 3. Similarity Metric: Cosine Similarity

**Definisi:** Mengukur sudut antara dua vektor dalam ruang multi-dimensional.

**Formula:**
```
         v1 · v2
sim = ─────────────────────
      ||v1|| × ||v2||

Dimana:
- v1 · v2 = Dot product = Σ(v1[i] × v2[i])
- ||v|| = Magnitude = √(Σ(v[i]²))
```

**Intuisi Geometri:**
```
Cosine = cos(θ)

θ = 0°    → cos(0°) = 1.0    (Identik - 100% sama)
θ = 90°   → cos(90°) = 0.0   (Orthogonal - sama sekali berbeda)
θ = 180°  → cos(180°) = -1.0 (Berlawanan)
```

**Visualisasi 2D:**
```
         v1
        /
       / θ
      /
   Origin ──────────
            v2

cos(θ) = similarity
```

**Mengapa Cosine Similarity?**
1. ✅ Range [-1, 1] mudah interpretasi
2. ✅ Tidak sensitif terhadap magnitude (hanya arah)
3. ✅ Computationally efficient
4. ✅ Bekerja baik untuk sparse vectors
5. ✅ Standard dalam NLP & recommendation systems

---

## 🔄 Tahap 1: Preprocessing

### Tujuan
Mengkonversi text raw menjadi format yang siap untuk analisis.

### Pipeline Preprocessing

```
Raw Text
   │
   ▼
1. Lowercase
   │
   ▼
2. Remove URLs & Special Characters
   │
   ▼
3. Tokenization (Split into words)
   │
   ▼
4. Remove Stopwords
   │
   ▼
5. Lemmatization
   │
   ▼
6. Remove Short Words
   │
   ▼
Clean Text (Processed)
```

### Detail Setiap Step

#### Step 1: Lowercase
```
Input:  "The Hero's Journey Through Dragon Valley"
Output: "the hero's journey through dragon valley"

Alasan: Menghindari duplikasi "The" vs "the"
```

#### Step 2: Remove URLs & Special Characters
```
Input:  "Visit https://myanimelist.net! Best anime: Code;Geass!"
Output: "Visit Best anime Code Geass"

Regex Patterns:
- URLs: https?://\S+
- Special: [^a-zA-Z\s]
```

#### Step 3: Tokenization
```
Input:  "the hero's journey through dragon valley"
Output: ["the", "hero's", "journey", "through", "dragon", "valley"]

Menggunakan: NLTK word_tokenize()
```

#### Step 4: Remove Stopwords
```
Stopwords: {a, an, the, is, are, in, on, at, to, for, ...}

Input:  ["the", "hero's", "journey", "through", "dragon", "valley"]
Output: ["hero's", "journey", "dragon", "valley"]
        (the, through dihapus)

Alasan: Stopwords tidak membawa informasi semantik signifikan
```

#### Step 5: Lemmatization
```
Lemmatization = Konversi kata ke bentuk dasar (lemma)

Input:  ["hero's", "journey", "dragon", "valley"]
         
Mapping:
- hero's → hero
- journeys → journey
- running → run
- children → child
- were → be

Output: ["hero", "journey", "dragon", "valley"]

Alasan: Mengurangi dimensionalitas, handle variasi kata
```

#### Step 6: Remove Short Words
```
Threshold: Hapus kata dengan panjang < 3 karakter

Input:  ["hero", "journey", "dragon", "valley"]
Output: ["hero", "journey", "dragon", "valley"]

Catatan: Semua kata sudah > 3, jadi tidak ada yang dihapus
```

### Contoh End-to-End Preprocessing

```
Original Synopsis:
"Hunters devote themselves to accomplishing hazardous tasks, all from 
traversing the world's uncharted territories to locating rare items and 
monsters. Before becoming a Hunter, one must pass the Hunter Examination—
a high-risk selection process in which most applicants end up handicapped 
or worse, deceased."

↓ (Lowercase)
"hunters devote themselves to accomplishing hazardous tasks, all from 
traversing the world's uncharted territories to locating rare items and 
monsters. before becoming a hunter, one must pass the hunter examination—
a high-risk selection process in which most applicants end up handicapped 
or worse, deceased."

↓ (Remove special chars)
"hunters devote themselves to accomplishing hazardous tasks all from 
traversing the worlds uncharted territories to locating rare items and 
monsters before becoming a hunter one must pass the hunter examination
a highrise selection process in which most applicants end up handicapped 
or worse deceased"

↓ (Tokenize & remove stopwords)
["hunters", "devote", "accomplishing", "hazardous", "tasks", "traversing", 
"worlds", "uncharted", "territories", "locating", "rare", "items", 
"monsters", "becoming", "hunter", "pass", "examination", "highrise", 
"selection", "process", "applicants", "handicapped", "worse", "deceased"]

↓ (Lemmatize)
["hunter", "devote", "accomplish", "hazard", "task", "traverse", 
"world", "uncharted", "teritory", "locate", "rare", "item", 
"monster", "becom", "hunter", "pass", "examin", "highrise", 
"select", "process", "applicant", "handicap", "worse", "dead"]

↓ (Remove short words - none < 3)
["hunter", "devote", "accomplish", "hazard", "task", "traverse", 
"world", "uncharted", "teritory", "locate", "rare", "item", 
"monster", "becom", "hunter", "pass", "examin", "highrise", 
"select", "process", "applicant", "handicap", "worse", "dead"]

Final Output:
"hunter devote accomplish hazard task traverse world uncharted 
teritory locate rare item monster becom pass examin highrise 
select process applicant handicap worse dead"
```

---

## 🎯 Tahap 2: Feature Extraction

### Tujuan
Ekstrak fitur penting dari setiap anime dan representasikan sebagai vektor.

### Fitur yang Diekstrak

#### A. Genre Features (Binary Encoding)

```python
def extract_genres(anime_data):
    """
    Ekstrak semua unique genres dari dataset
    Buat binary vector untuk setiap anime
    """
    
    # Contoh:
    all_genres = {
        "Action", "Adventure", "Comedy", "Drama", "Fantasy",
        "Romance", "Sci-Fi", "Shounen", "Slice of Life", ...
    }
    
    # Untuk anime "One Piece":
    # Genres: Action, Adventure, Comedy, Shounen, SuperPower
    
    # Binary Vector (13 genres):
    # [1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, ...]
    #  Action, Adventure, Comedy, Drama, Fantasy, Romance, Sci-Fi, Shounen...
```

**Visualisasi:**
```
                    Action Adventure Comedy ... SuperPower
One Piece           [  1  ,   1    ,  1   , ...   1    ]
Naruto              [  1  ,   1    ,  0   , ...   1    ]
Code Geass          [  1  ,   0    ,  0   , ...   0    ]
Clannad             [  0  ,   0    ,  0   , ...   0    ]

Kesamaan Genre One Piece vs Naruto: 2/3 genres sama
```

#### B. TF-IDF Features (Text)

**TF-IDF** = **Term Frequency** × **Inverse Document Frequency**

##### a) Term Frequency (TF)

```
TF(term, doc) = (Count of term in doc) / (Total words in doc)

Contoh untuk synopsis "hunter devote accomplish...":
- Total words = 25
- "hunter" appears 2 times → TF("hunter") = 2/25 = 0.08
- "task" appears 1 time   → TF("task") = 1/25 = 0.04
- "adventure" appears 0   → TF("adventure") = 0/25 = 0.0

Interpretasi: Proporsi kata dalam dokumen
```

**Mengapa TF Penting?**
- Kata yang sering muncul = lebih penting untuk dokumen
- "adventure" yang sering → anime itu likely bertipe adventure

##### b) Inverse Document Frequency (IDF)

```
IDF(term) = log(Total documents / Documents containing term)

Contoh dengan 10,000 anime:
- "adventure" appears in 2,000 docs
  → IDF("adventure") = log(10000/2000) = log(5) = 2.32

- "the" appears in 9,500 docs (stopword)
  → IDF("the") = log(10000/9500) = log(1.05) = 0.05

- "XYZ" appears in 1 doc (rare term)
  → IDF("XYZ") = log(10000/1) = log(10000) = 9.21

Interpretasi: Seberapa unik/langka term di seluruh corpus
```

**Mengapa IDF Penting?**
- Rare words = lebih informatif (unique untuk dokumen)
- Common words = kurang informatif (ada di semua dokumen)
- Stopwords = akan punya IDF sangat rendah

##### c) TF-IDF Combination

```
TF-IDF(term, doc) = TF(term, doc) × IDF(term)

Contoh:
Term "hunter":
- TF = 0.08 (muncul 2x dari 25 words)
- IDF = 3.5 (muncul di 200 docs dari 10000)
- TF-IDF = 0.08 × 3.5 = 0.28

Term "adventure":
- TF = 0.04 (muncul 1x dari 25 words)
- IDF = 2.32 (muncul di 2000 docs dari 10000)
- TF-IDF = 0.04 × 2.32 = 0.09

→ "hunter" lebih penting (0.28 > 0.09)
```

##### Matriks TF-IDF

```
Vocabulary:     [adventure, anime, battle, character, danger, ...]
                                                          (m dimensi)

Anime 1:        [0.25,      0.18,  0.34,   0.12,      0.28, ...]
Anime 2:        [0.18,      0.12,  0.28,   0.22,      0.15, ...]
Anime 3:        [0.30,      0.25,  0.10,   0.35,      0.05, ...]
...
(n anime)

n × m matrix (sparse untuk large vocabulary)
```

### Hybrid Feature Combination

```python
def build_combined_features(anime_data):
    """
    Kombinasikan synopsis + genre sebagai content
    """
    
    for anime in anime_data:
        synopsis = anime['synopsis']
        genres = anime['genre']  # "Action, Adventure, Comedy"
        
        # Boost genres dengan repetition (2x)
        combined = synopsis + " " + genres.replace(",", " ") * 2
        
        # Preprocessing + TF-IDF
        processed = preprocess_text(combined)
        tfidf_vector = calculate_tfidf(processed)
        
        # Genre binary vector
        genre_vector = extract_genre_vector(genres)
        
        # Final combined representation
        anime['tfidf_vector'] = tfidf_vector
        anime['genre_vector'] = genre_vector
    
    return anime_data
```

**Mengapa Boost Genre?**
- Memberikan weight lebih pada genre (explicit feature)
- Genre lebih reliable daripada text parsing
- Memastikan genre similarity dipertimbangkan

---

## 🔬 Tahap 3: Similarity Calculation

### Tujuan
Hitung seberapa mirip setiap anime dengan anime pilihan user.

### A. TF-IDF Cosine Similarity

```
Anime Pilihan: [0.25, 0.18, 0.34, 0.12, 0.28, ...]  (v1)
Anime Lain:    [0.18, 0.12, 0.28, 0.22, 0.15, ...]  (v2)

Step 1: Hitung Dot Product
v1 · v2 = (0.25×0.18) + (0.18×0.12) + (0.34×0.28) + (0.12×0.22) + (0.28×0.15) + ...
        = 0.045 + 0.0216 + 0.0952 + 0.0264 + 0.042 + ...
        = 0.2302 (sum of all products)

Step 2: Hitung Magnitude v1
||v1|| = √[(0.25)² + (0.18)² + (0.34)² + (0.12)² + (0.28)² + ...]
       = √[0.0625 + 0.0324 + 0.1156 + 0.0144 + 0.0784 + ...]
       = √0.3248
       = 0.5699

Step 3: Hitung Magnitude v2
||v2|| = √[(0.18)² + (0.12)² + (0.28)² + (0.22)² + (0.15)² + ...]
       = √[0.0324 + 0.0144 + 0.0784 + 0.0484 + 0.0225 + ...]
       = √0.2145
       = 0.4632

Step 4: Hitung Cosine Similarity
           0.2302
sim = ─────────────── = ─────────── = 0.8757
      0.5699 × 0.4632   0.2638

Similarity Score: 0.8757 (87.57% mirip)
```

### B. Genre Cosine Similarity

```
Anime Pilihan Genres: [1, 1, 1, 0, 0, 0, 0, 1, 0, 1, ...]  (g1)
                      [Action, Adventure, Comedy, Drama, Fantasy, ...]

Anime Lain Genres:    [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, ...]  (g2)

Step 1: Dot Product
g1 · g2 = (1×1) + (1×1) + (1×0) + (0×0) + ... + (1×1) + (0×0) + (1×0)
        = 1 + 1 + 0 + 0 + ... + 1 + 0 + 0
        = 3 (3 matching genres)

Step 2: Magnitude g1
||g1|| = √[1² + 1² + 1² + 0² + 0² + 0² + 0² + 1² + 0² + 1² + ...]
       = √5 = 2.236

Step 3: Magnitude g2
||g2|| = √[1² + 1² + 0² + 0² + ... + 1² + 0² + 0²]
       = √3 = 1.732

Step 4: Cosine Similarity
          3          3
sim = ──────────── = ──────── = 0.7746
      2.236 × 1.732  3.873

Genre Similarity: 0.7746 (77.46% genre cocok)
```

### C. Hybrid Similarity (Kombinasi)

```
Hybrid Similarity = (TF-IDF_sim × 0.7) + (Genre_sim × 0.3)

Dari contoh di atas:
TF-IDF_sim = 0.8757
Genre_sim = 0.7746

Hybrid = (0.8757 × 0.7) + (0.7746 × 0.3)
       = 0.6130 + 0.2324
       = 0.8454

Final Similarity Score: 0.8454 (84.54%)

Interpretasi:
- 70% dari text content similarity
- 30% dari explicit genre matching
- Balanced approach untuk akurat
```

### Matching Genres Extraction

```
Anime A Genres: [Action, Adventure, Comedy]
Anime B Genres: [Action, Fantasy, Comedy]

Matching = Genres yang SAMA di KEDUA anime
         = [Action, Comedy]  ← 2 genres cocok

Display untuk user:
"Genre Cocok: ✓ Action  ✓ Comedy"
(Ditampilkan dengan highlight/badge khusus)

Alasan: User dapat melihat MENGAPA recommendation ini diberikan
```

---

## 📊 Tahap 4: Ranking & Rekomendasi

### Ranking Algorithm

```python
def rank_recommendations(selected_anime_idx, anime_data, 
                        tfidf_vectors, genre_vectors):
    """
    ALGORITMA RANKING:
    
    1. similarities = []
    
    2. FOR i = 0 TO len(anime_data):
        IF i != selected_anime_idx:
            tfidf_sim = cosine_similarity(
                tfidf_vectors[selected_anime_idx],
                tfidf_vectors[i]
            )
            
            genre_sim = cosine_similarity(
                genre_vectors[selected_anime_idx],
                genre_vectors[i]
            )
            
            hybrid_sim = (tfidf_sim × 0.7) + (genre_sim × 0.3)
            
            matching_genres = get_matching_genres(
                genre_vectors[selected_anime_idx],
                genre_vectors[i]
            )
            
            similarities.append({
                'index': i,
                'score': hybrid_sim,
                'anime': anime_data[i],
                'matching_genres': matching_genres
            })
    
    3. SORT similarities BY score (descending)
       similarities = sorted(similarities, 
                            key=lambda x: x['score'], 
                            reverse=True)
    
    4. RETURN similarities[0:K]  (Top-K recommendations)
    """
```

### Contoh Ranking

```
Anime Pilihan: "One Piece"

Similarity Scores (descending):
1. Naruto           → 0.8847 (82.47%)  [Matching: Action, Adventure, Shounen]
2. Jujutsu Kaisen   → 0.8654 (86.54%)  [Matching: Action, Shounen]
3. Bleach           → 0.8421 (84.21%)  [Matching: Action, Adventure, Shounen]
4. Demon Slayer     → 0.8123 (81.23%)  [Matching: Action, Shounen]
5. My Hero Academia → 0.7892 (78.92%)  [Matching: Action, Shounen]
6. Code Geass       → 0.5432 (54.32%)  [Matching: Action]
7. Clannad          → 0.2891 (28.91%)  [Matching: None]

Top-5 direkomendasikan ke user dengan scores di atas
```

---

## 📋 Contoh Implementasi Step-by-Step

### Scenario: User memilih "One Piece"

#### Input
```
anime_title = "One Piece"
n_recommendations = 5
anime_data = [... 12,434 anime ...]
tf_vectors = [... 12,434 TF-IDF vectors ...]
genre_vectors = [... 12,434 genre vectors ...]
```

#### Execution

##### Step 1: Load Data & Find Selected Anime
```python
selected_anime_idx = None
for i, anime in enumerate(anime_data):
    if anime['title'].lower() == "one piece":
        selected_anime_idx = i
        break
# → selected_anime_idx = 5234

selected_anime = anime_data[5234]
# One Piece: {
#   'title': 'One Piece',
#   'score': 8.61,
#   'type': 'TV',
#   'episodes': 1100,
#   'genre': 'Action, Adventure, Comedy, Shounen, SuperPower',
#   'synopsis': '...'
# }
```

##### Step 2: Extract Vectors
```python
selected_tfidf_vector = tf_vectors[5234]
# [0.12, 0.15, 0.08, 0.21, 0.05, ..., 0.03]  (m dimensions)

selected_genre_vector = genre_vectors[5234]
# [1, 1, 1, 0, 0, 0, 0, 1, 0, 1, ..., 0]  (13 dimensions)
#  [Action, Adventure, Comedy, Drama, Fantasy, ...]
```

##### Step 3: Calculate Similarity for All Anime
```python
similarities = []

for i in range(len(anime_data)):
    if i != selected_anime_idx:
        # Anime B data
        anime_b = anime_data[i]
        tfidf_vector_b = tf_vectors[i]
        genre_vector_b = genre_vectors[i]
        
        # Calculate similarities
        tfidf_sim = cosine_similarity(selected_tfidf_vector, tfidf_vector_b)
        genre_sim = cosine_similarity(selected_genre_vector, genre_vector_b)
        
        # Hybrid similarity
        hybrid_sim = (tfidf_sim * 0.7) + (genre_sim * 0.3)
        
        # Matching genres
        matching = get_matching_genres(selected_genre_vector, 
                                      genre_vector_b, 
                                      genre_list)
        
        similarities.append({
            'index': i,
            'title': anime_b['title'],
            'score': hybrid_sim,
            'matching_genres': matching,
            'data': anime_b
        })

# After loop: similarities has 12,433 entries
```

##### Step 4: Sort & Get Top-K
```python
# Sort by score (descending)
similarities.sort(key=lambda x: x['score'], reverse=True)

# Get Top-5
top_5 = similarities[:5]

# Result:
# [
#   {'title': 'Naruto', 'score': 0.8847, 'matching_genres': [Action, Adventure, Shounen]},
#   {'title': 'Jujutsu Kaisen', 'score': 0.8654, 'matching_genres': [Action, Shounen]},
#   {'title': 'Bleach', 'score': 0.8421, 'matching_genres': [Action, Adventure, Shounen]},
#   {'title': 'Demon Slayer', 'score': 0.8123, 'matching_genres': [Action, Shounen]},
#   {'title': 'My Hero Academia', 'score': 0.7892, 'matching_genres': [Action, Shounen]}
# ]
```

##### Step 5: Format Output
```python
recommendations = []
for item in top_5:
    rec = {
        'title': item['data']['title'],
        'score': item['data']['score'],  # MyAnimeList rating
        'type': item['data']['type'],
        'episodes': item['data']['episodes'],
        'synopsis': item['data']['synopsis'],
        'genre': item['data']['genre'],
        'similarity_score': item['score'],  # Our calculated similarity
        'matching_genres': item['matching_genres']
    }
    recommendations.append(rec)

return recommendations
```

#### Output Display
```
═══════════════════════════════════════════════════════════════════════

🎌 Sistem Rekomendasi Anime 🎌
Temukan anime favorit Anda dengan Content-Based Filtering (TF-IDF + Genre)

═══════════════════════════════════════════════════════════════════════

🎬 Anime yang Anda Pilih:

🎬 One Piece
⭐ 8.61      Tipe: TV      Episodes: 1100
Genre: [Action] [Adventure] [Comedy] [Shounen] [SuperPower]
📊 Kesamaan: 100.0%
Sinopsis: Monkey D. Luffy, a young man with straw hat...

═══════════════════════════════════════════════════════════════════════

💎 Rekomendasi Untuk Anda:

#1 - Kesamaan: 88.5%

🎬 Naruto
⭐ 7.91      Tipe: TV      Episodes: 220
Genre: [Action] [Adventure] [Comedy] [Shounen] [SuperPower]
Genre Cocok: ✓ Action ✓ Adventure ✓ Shounen
📊 Kesamaan: 88.5%
Sinopsis: Naruto Uzumaki wants to become the strongest shinobi...

═══════════════════════════════════════════════════════════════════════

#2 - Kesamaan: 86.5%

🎬 Jujutsu Kaisen
⭐ 8.63      Tipe: TV      Episodes: 47
Genre: [Action] [Dark Fantasy] [Shounen] [Supernatural]
Genre Cocok: ✓ Action ✓ Shounen
📊 Kesamaan: 86.5%
Sinopsis: A high schooler swallows a cursed finger and becomes...

═══════════════════════════════════════════════════════════════════════

... (3 more recommendations)
```

---

## ⏱️ Analisis Kompleksitas

### Time Complexity

| Operation | Kompleksitas | Penjelasan |
|-----------|-------------|-----------|
| **Data Loading** | O(n) | Baca n anime dari CSV |
| **Preprocessing** | O(n × m) | n anime, m avg words per synopsis |
| **TF-IDF Calculation** | O(n × d) | n anime, d vocabulary size |
| **Genre Extraction** | O(n × g) | n anime, g genres per anime |
| **Similarity Calculation** | O(n × d) | n anime, d feature dimensions |
| **Ranking (Sort)** | O(n log n) | Sort by similarity score |
| **Total (one recommendation)** | **O(n × (m + d + log n))** | Dominated by O(n × d) |

### Space Complexity

| Data Structure | Kompleksitas | Penjelasan |
|---|---|---|
| **TF-IDF Matrix** | O(n × d) | n anime × d vocabulary terms |
| **Genre Vectors** | O(n × g) | n anime × g genres |
| **Similarity Scores** | O(n) | Store similarity untuk n anime |
| **Total** | **O(n × d)** | Dominated by TF-IDF matrix |

### Optimization Strategies

#### 1. **Caching**
```python
@st.cache_data
def load_anime_data():
    # Cache data loading
    ...

@st.cache_resource
def build_tfidf_features():
    # Cache feature extraction
    ...
```

**Benefit:** Tidak perlu rebuild features untuk setiap recommendation request

#### 2. **Approximate Nearest Neighbors (ANN)**
```
Current: O(n × d) similarity calculation
ANN (Locality Sensitive Hashing): O(log n) atau O(1) average case

Trade-off: Akurasi vs Speed
```

#### 3. **Vector Quantization**
```
Reduce dimensions menggunakan PCA/SVD
n × d → n × d' (d' << d)

Benefit: Faster similarity calculation, less memory
```

#### 4. **Batch Processing**
```python
# Instead of calculating similarity one by one
# Calculate in batches using matrix operations
similarities = tf_matrix @ selected_vector.T  # O(d) per anime
```

---

## 🎓 Kesimpulan

### Keunggulan Algoritma Content-Based Filtering

✅ **Transparansi:** User tahu alasan rekomendasi  
✅ **Cold-Start:** Bisa recommend item baru tanpa user history  
✅ **Scalability:** Linear dengan jumlah item, tidak bergantung user  
✅ **Flexibility:** Mudah incorporate fitur baru  

### Limitasi

❌ **Limited Discovery:** Hanya recommend based on existing features  
❌ **Feature Dependency:** Kualitas features = kualitas rekomendasi  
❌ **Popularity Bias:** Sulit recommend niche items  

### Improvement Suggestions

1. Hybrid dengan Collaborative Filtering (combine best of both)
2. Deep Learning (embeddings, neural networks)
3. Advanced NLP (semantic similarity, transformers)
4. User Personalization (individual preferences)

---

## 📚 Referensi

- **TF-IDF:** https://en.wikipedia.org/wiki/Tf%E2%80%93idf
- **Cosine Similarity:** https://en.wikipedia.org/wiki/Cosine_similarity
- **Content-Based Filtering:** https://en.wikipedia.org/wiki/Recommender_system#Content-based_filtering
- **NLTK Lemmatization:** https://www.nltk.org/

---

**Dibuat:** May 19, 2026  
**Version:** 1.0.0
