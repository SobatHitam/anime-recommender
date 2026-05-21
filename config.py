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
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'anime_recommender'),
    'charset': 'utf8mb4',
    'use_unicode': True,
    'autocommit': True
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
