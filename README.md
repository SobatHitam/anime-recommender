# 🎌 Sistem Rekomendasi Anime - Streamlit App

Sebuah aplikasi web multi-fitur untuk merekomendasikan anime menggunakan algoritma **Content-Based Filtering** dengan metode **TF-IDF** dan **Cosine Similarity**.

## 📋 Daftar Isi

- [Fitur Utama](#fitur-utama)
- [Teknologi yang Digunakan](#teknologi-yang-digunakan)
- [Instalasi](#instalasi)
- [Cara Menjalankan](#cara-menjalankan)
- [Struktur Project](#struktur-project)
- [Penjelasan Algoritma](#penjelasan-algoritma)
- [Screenshots](#screenshots)

## ✨ Fitur Utama

### 1. **🎯 Rekomendasi Anime**
- Pilih anime favorit dari dropdown
- Dapatkan rekomendasi anime yang mirip secara otomatis
- Tampilkan hingga 20 rekomendasi
- Lihat similarity score untuk setiap rekomendasi

### 2. **⭐ Top Rating**
- Lihat anime dengan rating tertinggi
- Sorting otomatis berdasarkan rating
- Tampilkan hingga 50 anime terbaik

### 3. **🔥 Anime Populer**
- Lihat anime populer berdasarkan rating dan keberagaman genre
- Sistem scoring popularity otomatis

### 4. **🔍 Search & Filter**
- Search anime berdasarkan judul atau sinopsis
- Filter anime berdasarkan satu atau lebih genre
- Multi-select genre filter

### 5. **📊 Statistics**
- Total anime dalam database
- Rating rata-rata, tertinggi, dan terendah
- Statistik genre paling banyak
- Visualisasi chart genre

### 6. **🎨 Design Modern**
- Dark mode anime style UI
- Gradient colors dengan accent pink (#ff006e)
- Responsive card layout
- Smooth animations dan transitions
- Emoji icons untuk visual appeal

## 🛠️ Teknologi yang Digunakan

### Backend
- **Streamlit**: Framework untuk membuat web app interaktif
- **Pandas**: Data manipulation dan analysis
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning library
  - TfidfVectorizer: Konversi text ke TF-IDF matrix
  - Cosine Similarity: Hitung kesamaan antar item
- **NLTK**: Natural Language Toolkit untuk text preprocessing

### Algoritma
- **TF-IDF (Term Frequency-Inverse Document Frequency)**
  - Konversi text sinopsis dan genre menjadi nilai numerik
  - Memberikan bobot lebih pada kata-kata unik
  
- **Cosine Similarity**
  - Mengukur kesamaan antara anime berdasarkan vektornya
  - Range 0-1 (0 = tidak mirip, 1 = sangat mirip)

### Text Preprocessing
- Konversi ke lowercase
- Hapus URL dan karakter khusus
- Hapus stopwords bahasa Inggris
- Tokenization dan normalisasi

## 📦 Instalasi

### Prerequisites
- Python 3.8 atau lebih tinggi
- pip (Python package manager)

### Step 1: Clone atau Download Project
```bash
# Jika menggunakan git
git clone <repository-url>
cd SRIPSI

# Atau ekstrak file project ke folder SRIPSI
```

### Step 2: Install Dependencies
```bash
# Install library dari requirements.txt
pip install -r requirements.txt
```

Perintah ini akan menginstall:
- `streamlit`: Web framework
- `pandas`: Data processing
- `numpy`: Numerical operations
- `scikit-learn`: Machine learning
- `nltk`: Text preprocessing

### Step 3: Download NLTK Data
Library NLTK memerlukan data tambahan. Jalankan Python dan download:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

Atau biarkan aplikasi mengunduhnya secara otomatis saat pertama kali dijalankan.

## 🚀 Cara Menjalankan

### Opsi 1: Menggunakan Terminal
```bash
# Navigate ke project folder
cd d:\Documents\Coding\SRIPSI

# Jalankan aplikasi Streamlit
streamlit run app.py
```

### Opsi 2: Menggunakan VS Code
1. Buka project di VS Code
2. Buka terminal (Ctrl + `)
3. Jalankan: `streamlit run app.py`

### Hasil
- Aplikasi akan membuka di browser default pada `http://localhost:8501`
- Gunakan sidebar untuk navigasi antar halaman
- Aplikasi siap untuk digunakan

### Tips untuk Berjalan Lancar
- **Pertama kali jalankan**: Mungkin sedikit lambat karena loading model TF-IDF
- **Caching**: Streamlit akan cache data dan model untuk kecepatan selanjutnya
- **Port alternatif**: `streamlit run app.py --server.port 8502`
- **Public access**: `streamlit run app.py --server.headless true`

## 📁 Struktur Project

```
SRIPSI/
├── app.py                 # File utama aplikasi Streamlit
├── anime.csv             # Dataset anime (50 anime)
├── requirements.txt      # Dependencies Python
├── README.md            # Dokumentasi project
└── assets/              # Folder untuk assets (jika diperluas)
```

### File Penting

#### app.py
File utama yang berisi:
- Konfigurasi Streamlit
- CSS styling dark mode anime
- Fungsi preprocessing text
- Fungsi load dan cache data
- Implementasi TF-IDF dan Cosine Similarity
- Fungsi-fungsi utility (search, filter, ranking)
- Tampilan UI untuk setiap halaman
- Logic rekomendasi anime

#### anime.csv
Dataset dengan 50 anime populer berisi:
- `anime_id`: ID unik anime
- `title`: Judul anime (Inggris)
- `genre`: Genre-genre anime (dipisahkan |)
- `synopsis`: Sinopsis singkat anime
- `rating`: Rating dari 1-10

#### requirements.txt
Daftar semua library Python yang diperlukan beserta versinya.

## 🧠 Penjelasan Algoritma

### Content-Based Filtering

Sistem ini menggunakan **Content-Based Filtering** yang bekerja berdasarkan karakteristik (konten) dari setiap anime.

#### Langkah-Langkah:

1. **Data Preparation**
   ```
   Ambil genre + synopsis → Gabung menjadi "content"
   ```

2. **Text Preprocessing**
   ```
   content 
   → Lowercase 
   → Hapus URL & simbol 
   → Hapus stopwords 
   → content_processed
   ```

3. **TF-IDF Vectorization**
   ```
   Konversi content_processed menjadi vector numerik
   TfidfVectorizer(max_features=500, min_df=1, max_df=0.8)
   ```

4. **Similarity Calculation**
   ```
   Hitung cosine_similarity antara:
   - Anime yang dipilih user
   - Semua anime lain di database
   ```

5. **Ranking & Return**
   ```
   Sort berdasarkan similarity score (tertinggi ke terendah)
   Return top-N rekomendasi
   ```

### Formula Cosine Similarity

```
similarity = (A · B) / (||A|| × ||B||)

Dimana:
- A · B = dot product vector A dan B
- ||A|| = magnitude/norm vector A
- ||B|| = magnitude/norm vector B
- Result: 0 (sangat berbeda) hingga 1 (identik)
```

## 📊 Contoh Penggunaan

### Skenario: User memilih "Attack on Titan"

1. Sistem akan ambil vektor TF-IDF dari "Attack on Titan"
2. Hitung cosine similarity dengan semua anime lain
3. Sort berdasarkan similarity score
4. Return top-5 anime yang paling mirip

**Contoh hasil:**
- Jujutsu Kaisen (0.87 similarity)
- Demon Slayer (0.85 similarity)
- Bleach (0.82 similarity)
- My Hero Academia (0.80 similarity)
- Naruto (0.78 similarity)

## ⚙️ Optimasi Performance

### Caching
- Dataset dan model TF-IDF di-cache menggunakan `@st.cache_data` dan `@st.cache_resource`
- Pertama kali run lebih lambat, selanjutnya sangat cepat
- Hanya re-compute jika data berubah

### Text Preprocessing
- Dilakukan hanya satu kali saat load data
- Hasil disimpan di kolom `content_processed`

### TF-IDF Matrix
- Pre-computed saat aplikasi start
- Di-reuse untuk semua rekomendasi

### Optimasi Query
- Menggunakan pandas operations yang efisien
- Minimal loop, maximum vectorization

## 🎨 Customization

### Mengubah Warna Theme
Edit bagian `dark_anime_style` di `app.py`:
```python
--accent-color: #ff006e;     # Warna accent (saat ini pink)
--bg-primary: #0a0e27;       # Background utama
--bg-secondary: #1a1f3a;     # Background secondary
```

### Menambah Dataset
1. Edit `anime.csv` dengan format sama
2. Tambahkan baris baru dengan anime_id, title, genre, synopsis, rating
3. Simpan file
4. Restart aplikasi

### Mengubah Jumlah Top Features
Di `app.py` baris TfidfVectorizer:
```python
TfidfVectorizer(max_features=500, ...)  # Ubah 500 menjadi nilai yang diinginkan
```

## 📝 Penjelasan Kode

### Struktur Kode
```
1. Import Library
2. Konfigurasi Streamlit
3. CSS Styling
4. Fungsi Preprocessing
5. Fungsi Load & Cache Data
6. Fungsi Content-Based Filtering
7. Fungsi Utility (Filter, Search, etc)
8. Fungsi Display UI
9. Main Application
10. Run Application
```

### Naming Convention
- Fungsi: `snake_case` (contoh: `preprocess_text()`)
- Variable: `snake_case` (contoh: `anime_title`)
- Constant: `UPPER_CASE` (contoh opsional)
- Class (jika ada): `PascalCase`

### Komentar
- Setiap fungsi punya docstring
- Setiap section punya header komentar
- Komentar dalam Bahasa Indonesia untuk kemudahan

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named..."
**Solusi**: Install dependencies yang hilang
```bash
pip install -r requirements.txt
```

### Error: "No such file or directory: anime.csv"
**Solusi**: Pastikan anime.csv berada di folder yang sama dengan app.py

### Aplikasi Loading Lama Pertama Kali
**Normal**: NLTK sedang download data stopwords
- Tunggu hingga selesai
- Selanjutnya akan lebih cepat

### Port 8501 Sudah Digunakan
**Solusi**: Gunakan port berbeda
```bash
streamlit run app.py --server.port 8502
```

### Rekomendasi Tidak Muncul
**Kemungkinan**: Pilih anime yang benar-benar ada di dropdown

## 📚 Dataset

Database saat ini berisi 50 anime populer dengan kategori:
- Action/Adventure
- Slice of Life
- Comedy
- Drama
- Romance
- Sci-Fi
- Psychological
- Supernatural

Rating berkisar dari 7.5 hingga 9.1

## 🎓 Untuk Skripsi

Fitur yang cocok untuk dokumentasi skripsi:
- Algoritma TF-IDF dengan penjelasan formula
- Cosine Similarity implementation
- Text preprocessing pipeline
- UI/UX implementation
- Caching strategy
- Performance optimization

## 📄 Lisensi

Project ini dibuat untuk tujuan pendidikan dan skripsi.

## 👨‍💻 Author

Dibuat sebagai sistem rekomendasi anime untuk keperluan skripsi.

---

**Happy Recommending! 🎌**

Jika ada pertanyaan atau isu, silakan check troubleshooting section di atas.
