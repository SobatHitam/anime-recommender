# 🚀 QUICK START - DATABASE SETUP

## 5 Langkah Setup (< 5 menit)

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Setup Database Configuration
```bash
# Copy template env ke actual env
copy .env.example .env

# Edit .env dengan text editor (e.g., Notepad, VS Code)
# Sesuaikan dengan konfigurasi MySQL Anda:
# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=your_password
```

### 3️⃣ Create Database Schema
```bash
# Option A: Using MySQL CLI (jika MySQL sudah diinstall)
mysql -u root -p < database_schema.sql

# Option B: Otomatis via migration script (lihat step 4)
```

### 4️⃣ Migrate Data dari CSV
```bash
python migrate_csv_to_db.py
```

**Output yang diharapkan:**
```
✓ Koneksi ke database berhasil!
✓ Database schema berhasil dibuat!
🔄 Memulai migrasi data...
✓ Migrasi data selesai!
✓ [database stats ditampilkan]
```

### 5️⃣ Verify Koneksi Database
```python
# Run dari Python shell atau create test file
from db_utils import check_database_health

health = check_database_health()
print(health)
```

**Expected output:**
```
{'connected': True, 'total_animes': 100, 'total_types': 6, 'average_score': 8.5, 'error': None}
```

---

## 🎮 Test di Streamlit

```bash
streamlit run app.py
```

✅ Selesai! Database siap digunakan.

---

## 📝 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| `Access denied for user 'root'` | Update password di `.env` |
| `Unknown database` | Jalankan `database_schema.sql` via MySQL |
| `Table doesn't exist` | Jalankan `migrate_csv_to_db.py` |
| `Connection refused` | Pastikan MySQL server running |

---

## 📚 Dokumentasi Lengkap

Untuk dokumentasi lebih detail, lihat: **DATABASE_SETUP.md**

---

## 🔄 Update Data dari CSV

Jika ada update di `anime.csv`:
```bash
# Clear data lama
mysql -u root -p -e "TRUNCATE TABLE anime_recommender.animes;"

# Migrasi lagi
python migrate_csv_to_db.py
```

---

**Need help?** Lihat DATABASE_SETUP.md section "Troubleshooting"
