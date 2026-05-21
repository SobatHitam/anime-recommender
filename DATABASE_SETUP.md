# 📦 SISTEM DATABASE ANIME - DOKUMENTASI SETUP

## 📋 Daftar Isi
1. [Overview](#overview)
2. [Prasyarat](#prasyarat)
3. [Instalasi Database](#instalasi-database)
4. [Migrasi Data](#migrasi-data)
5. [Integrasi dengan Streamlit](#integrasi-dengan-streamlit)
6. [Query Reference](#query-reference)
7. [Troubleshooting](#troubleshooting)

---

## Overview

Sistem database ini dibangun dengan **MySQL** untuk menggantikan pembacaan CSV langsung dalam aplikasi Streamlit. Dengan database, aplikasi Anda akan:

✅ **Lebih cepat** - Query hanya data yang diperlukan  
✅ **Lebih scalable** - Siap untuk dataset besar (>100.000 data)  
✅ **Lebih efisien** - Caching berbasis database  
✅ **Lebih fleksibel** - Kemampuan filtering dan searching yang lebih baik  

### Struktur Database

```
anime_recommender/
├── types (Master Data)
│   ├── type_id (PK)
│   └── type_name (TV, Movie, OVA, etc)
│
├── animes (Main Data)
│   ├── anime_id (PK)
│   ├── title
│   ├── score
│   ├── type_id (FK → types)
│   ├── synopsis (untuk TF-IDF)
│   ├── episodes
│   ├── image_url
│   └── ... (other fields)
│
└── user_activity (Optional - Untuk tracking)
    ├── activity_id (PK)
    ├── user_id
    ├── anime_id (FK → animes)
    ├── activity_type
    └── timestamp
```

---

## Prasyarat

### 1. MySQL Server
Pastikan MySQL sudah terinstall dan berjalan:

```bash
# Windows - Cek dari Command Prompt
mysql --version

# Jika belum install, download dari: https://dev.mysql.com/downloads/mysql/
```

### 2. Python Packages
Pastikan sudah install package yang diperlukan:

```bash
pip install mysql-connector-python python-dotenv streamlit scikit-learn nltk
```

---

## Instalasi Database

### Step 1: Membuat Database

Ada 2 cara untuk membuat database:

#### **Cara A: Menggunakan File SQL (Recommended)**

1. Buka MySQL Client:
```bash
mysql -u root -p
```

2. Jalankan script SQL:
```sql
source database_schema.sql;
```

3. Verifikasi database terbuat:
```sql
SHOW DATABASES;
USE anime_recommender;
SHOW TABLES;
```

#### **Cara B: Manual via Migration Script**

Script `migrate_csv_to_db.py` akan membuat database otomatis.

### Step 2: Setup Environment Variables

1. Copy file `.env.example` menjadi `.env`:
```bash
copy .env.example .env
```

2. Sesuaikan konfigurasi di `.env`:
```ini
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=anime_recommender
```

---

## Migrasi Data

### Step 1: Persiapan
Pastikan:
- ✅ `anime.csv` ada di direktori yang sama
- ✅ MySQL server sudah berjalan
- ✅ `.env` sudah dikonfigurasi
- ✅ Database dan tabel sudah terbuat

### Step 2: Jalankan Migration Script

```bash
python migrate_csv_to_db.py
```

### Output yang Diharapkan

```
==================================================
MIGRASI DATABASE ANIME - FULL PROCESS
==================================================
✓ Koneksi ke database berhasil!
📋 Membaca file schema: database_schema.sql
✓ Database schema berhasil dibuat/diperbarui! (13 statements)

📂 Membaca file CSV: anime.csv
🔄 Memulai migrasi data...

  [10%] 10 rows | Success: 10 | Failed: 0
  [20%] 20 rows | Success: 20 | Failed: 0
  ...
  [100%] 100 rows | Success: 100 | Failed: 0

✓ Migrasi data selesai!

==================================================
RINGKASAN MIGRASI DATA
==================================================
Total baris CSV:      100
Berhasil di-insert:   100
Gagal di-insert:      0
Success rate:         100.00%
==================================================

✓ Memverifikasi hasil migrasi...

  Total anime di database: 100

  Distribusi anime per tipe:
    - TV: 45 anime
    - Movie: 30 anime
    - OVA: 15 anime
    - Special: 10 anime

  Top 5 anime berdasarkan score:
    1. Sousou no Frieren (Score: 9.29)
    2. Chainsaw Man Movie: Reze-hen (Score: 9.18)
    ...

✓ Verifikasi selesai!
✓ Koneksi database ditutup!
✓ Semua proses selesai!
```

---

## Integrasi dengan Streamlit

### Update `app.py`

Ganti function import dan load data:

#### **Sebelum (CSV Based):**
```python
import csv

def load_anime_data():
    animes = []
    with open('anime.csv', 'r') as f:
        reader = csv.DictReader(f)
        animes = list(reader)
    return animes
```

#### **Sesudah (Database Based):**
```python
from db_utils import (
    load_anime_data, 
    search_anime, 
    get_top_rated_anime,
    get_anime_by_type,
    get_cached_anime_data,
    get_cached_types
)

# Langsung gunakan function dari db_utils
# Tidak perlu modifikasi logika, hanya ganti import
```

### Contoh Integrasi Lengkap

```python
import streamlit as st
from db_utils import (
    get_cached_anime_data,
    get_cached_types,
    search_anime,
    get_top_rated_anime,
    get_anime_by_type,
    log_user_activity,
    check_database_health
)

# Display database status
health = check_database_health()
col1, col2, col3 = st.columns(3)
col1.metric("Database", "✓ Connected" if health['connected'] else "✗ Disconnected")
col2.metric("Total Anime", health['total_animes'])
col3.metric("Avg Score", f"{health['average_score']:.2f}")

# Load data dengan cache
animes = get_cached_anime_data()

# Search anime
keyword = st.text_input("Search anime...")
if keyword:
    results = search_anime(keyword, limit=50)
    st.write(f"Found {len(results)} results")
```

---

## Query Reference

### Fungsi-Fungsi Database

| Fungsi | Deskripsi | Return |
|--------|-----------|--------|
| `load_anime_data()` | Load semua anime | `List[Dict]` |
| `search_anime(keyword, limit)` | Search by keyword | `List[Dict]` |
| `get_top_rated_anime(limit)` | Get top rated | `List[Dict]` |
| `get_anime_by_type(type)` | Filter by type | `List[Dict]` |
| `get_anime_by_id(id)` | Get detail anime | `Dict` |
| `get_all_types()` | Get semua types | `List[Dict]` |
| `get_similar_anime(id, range, limit)` | Get similar anime | `List[Dict]` |
| `get_cached_anime_data()` | Load dengan Streamlit cache | `List[Dict]` |

### Contoh Query Custom

Jika butuh custom query, gunakan `DatabaseConnection`:

```python
from db_utils import DatabaseConnection

db = DatabaseConnection()

# Simple query
results = db.execute_query(
    "SELECT * FROM animes WHERE score > %s",
    (8.5,)
)

# Get single result
single = db.execute_query(
    "SELECT * FROM animes WHERE anime_id = %s",
    (28977,),
    fetch_all=False
)
```

---

## Troubleshooting

### Error: "Access denied for user 'root'@'localhost'"

**Solusi:** Sesuaikan password di `.env`:
```ini
DB_PASSWORD=your_actual_password
```

### Error: "Unknown database 'anime_recommender'"

**Solusi:** Jalankan script schema terlebih dahulu:
```bash
mysql -u root -p < database_schema.sql
```

### Error: "Table 'anime_recommender.animes' doesn't exist"

**Solusi:** Pastikan migration sudah selesai:
```bash
python migrate_csv_to_db.py
```

### Aplikasi Streamlit Lambat

**Solusi:** 
1. Pastikan cache aktif:
   - `get_cached_anime_data()` bukan `load_anime_data()`
2. Cek database indices:
   ```sql
   SHOW INDEXES FROM animes;
   ```

### Migration Gagal di Tengah Jalan

**Solusi:**
1. Lihat error message
2. Clear data lama:
   ```sql
   TRUNCATE TABLE animes;
   ```
3. Jalankan migration lagi

---

## Performance Tips

### 1. Optimize Queries
```python
# ❌ Jangan load semua, filter di Python
all_animes = load_anime_data()
filtered = [a for a in all_animes if a['score'] > 8.5]

# ✅ Filter di database
results = db.execute_query(
    "SELECT * FROM animes WHERE score > %s",
    (8.5,)
)
```

### 2. Use Cache
```python
# ❌ Query setiap render Streamlit
animes = load_anime_data()

# ✅ Cache result
@st.cache_resource(ttl=3600)
def get_animes():
    return load_anime_data()

animes = get_animes()
```

### 3. Limit Results
```python
# Selalu gunakan LIMIT untuk search results
results = search_anime(keyword, limit=50)
```

### 4. Add Proper Indices
Database sudah punya index pada:
- `title` - Untuk search
- `score` - Untuk sorting
- `type_id` - Untuk filtering
- `anime_id` - Primary key

---

## Monitoring Database

### Health Check
```python
from db_utils import check_database_health

health = check_database_health()
print(health)
# Output:
# {
#     'connected': True,
#     'total_animes': 12450,
#     'total_types': 6,
#     'average_score': 6.85,
#     'error': None
# }
```

### Database Statistics
```sql
SELECT * FROM anime_statistics;
```

---

## Untuk Pengembangan Lebih Lanjut

### Tambah User Activity Tracking
```python
from db_utils import log_user_activity

# Track saat user search
log_user_activity(
    user_id="user_123",
    anime_id=28977,
    activity_type="search",
    search_query="gintama"
)
```

### Export Data
```python
from db_utils import export_to_json

# Export semua anime ke JSON
export_to_json('anime_backup.json')
```

---

## File Reference

| File | Deskripsi |
|------|-----------|
| `database_schema.sql` | SQL schema untuk membuat database |
| `migrate_csv_to_db.py` | Script untuk migrasi data CSV → DB |
| `db_utils.py` | Module utilities untuk query database |
| `config.py` | Konfigurasi database dan constants |
| `.env.example` | Template environment variables |
| `DATABASE_SETUP.md` | Dokumentasi ini |

---

## Support & Resources

- **MySQL Documentation**: https://dev.mysql.com/doc/
- **MySQL Connector Python**: https://dev.mysql.com/doc/connector-python/en/
- **Streamlit Caching**: https://docs.streamlit.io/library/advanced-features/caching

---

**Last Updated:** 2026-05-21  
**Database Version:** 1.0  
**Python Version:** 3.8+
