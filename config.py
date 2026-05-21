# ===================================
# KONFIGURASI DATABASE
# File ini menyimpan konfigurasi koneksi ke MySQL Database
# ===================================

import os
from dotenv import load_dotenv

# Load environment variables dari .env file
load_dotenv()

# ===================================
# KONFIGURASI DATABASE MYSQL
# ===================================

# Try load dari Streamlit secrets dulu (untuk production), fallback ke .env
try:
    import streamlit as st
    DB_HOST = st.secrets.get("DB_HOST", os.getenv('DB_HOST', 'localhost'))
    DB_PORT = int(st.secrets.get("DB_PORT", os.getenv('DB_PORT', '3306')))
    DB_USER = st.secrets.get("DB_USER", os.getenv('DB_USER', 'root'))
    DB_PASSWORD = st.secrets.get("DB_PASSWORD", os.getenv('DB_PASSWORD', ''))
    DB_NAME = st.secrets.get("DB_NAME", os.getenv('DB_NAME', 'anime_recommender'))
except:
    # Fallback jika streamlit tidak available
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', '3306'))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'anime_recommender')

DB_CONFIG = {
    'host': DB_HOST,
    'port': DB_PORT,  # ✅ PENTING: Port harus terpisah dari host!
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_NAME,
    'charset': 'utf8mb4',
    'use_unicode': True,
    'autocommit': True,
    'connection_timeout': 10,  # ✅ Prevent hang jika network lambat
    'ssl_disabled': False  # ✅ WAJIB untuk Railway MySQL
}

# ===================================
# QUERY CONSTANTS
# ===================================
QUERIES = {
    # Load semua anime
    'load_all_animes': """
        SELECT a.*, t.type_name 
        FROM animes a 
        LEFT JOIN types t ON a.type_id = t.type_id
        ORDER BY a.score DESC
    """,
    
    # Search anime by title atau synopsis
    'search_anime': """
        SELECT a.*, t.type_name
        FROM animes a
        LEFT JOIN types t ON a.type_id = t.type_id
        WHERE MATCH(a.title, a.synopsis) AGAINST(%s IN BOOLEAN MODE)
           OR a.title LIKE CONCAT('%', %s, '%')
        ORDER BY a.score DESC
        LIMIT %s
    """,
    
    # Get top rated anime
    'get_top_rated': """
        SELECT a.*, t.type_name
        FROM animes a
        LEFT JOIN types t ON a.type_id = t.type_id
        WHERE a.score > 0
        ORDER BY a.score DESC
        LIMIT %s
    """,
    
    # Get anime by type
    'get_by_type': """
        SELECT a.*, t.type_name
        FROM animes a
        LEFT JOIN types t ON a.type_id = t.type_id
        WHERE t.type_name = %s
        ORDER BY a.score DESC
    """,
    
    # Get specific anime by ID
    'get_anime_by_id': """
        SELECT a.*, t.type_name
        FROM animes a
        LEFT JOIN types t ON a.type_id = t.type_id
        WHERE a.anime_id = %s
    """,
    
    # Get all unique types
    'get_all_types': """
        SELECT * FROM types ORDER BY type_name
    """,
    
    # Get anime statistics
    'get_statistics': """
        SELECT * FROM anime_statistics
    """,
    
    # Get similar anime by score range
    'get_similar_score_range': """
        SELECT a.*, t.type_name
        FROM animes a
        LEFT JOIN types t ON a.type_id = t.type_id
        WHERE a.score BETWEEN %s AND %s
          AND a.anime_id != %s
        ORDER BY a.score DESC, a.popularity DESC
        LIMIT %s
    """
}

# ===================================
# CACHE SETTINGS
# ===================================
CACHE_SETTINGS = {
    # TTL dalam detik untuk cache data
    'ttl_anime_data': 3600,      # 1 jam
    'ttl_types': 7200,            # 2 jam
    'ttl_statistics': 3600,       # 1 jam
    
    # Cache key prefix
    'prefix': 'anime_'
}

# ===================================
# FEATURE FLAGS
# ===================================
FEATURES = {
    'use_database': True,
    'use_cache': True,
    'enable_user_activity': False,  # Ubah ke True jika ingin track user activity
    'enable_personalization': False, # Untuk rekomendasi yang dipersonalisasi
}

# ===================================
# LOGGING CONFIG
# ===================================
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'logs/database.log'
}
