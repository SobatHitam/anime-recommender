# ===================================
# DATABASE UTILITIES & QUERY FUNCTIONS
# Module ini menyediakan fungsi untuk query database
# Dioptimalkan untuk digunakan dengan Streamlit
# ===================================

import mysql.connector
from mysql.connector import Error
import logging
from config import DB_CONFIG, QUERIES, CACHE_SETTINGS, LOGGING_CONFIG
import json
from functools import lru_cache
from typing import List, Dict, Optional, Tuple
import streamlit as st

# ===================================
# LOGGING SETUP
# ===================================
logging.basicConfig(
    level=logging.INFO,
    format=LOGGING_CONFIG['format']
)
logger = logging.getLogger(__name__)


class DatabaseConnection:
    """
    Class untuk mengelola koneksi ke MySQL database
    Menggunakan connection pooling untuk efisiensi
    """
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        """Singleton pattern untuk database connection"""
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize database connection"""
        if self._connection is None:
            self.connect()
    
    def connect(self) -> bool:
        """
        Membuat koneksi ke database
        
        Returns:
            bool: True jika berhasil connect, False jika gagal
        """
        try:
            self._connection = mysql.connector.connect(**DB_CONFIG)
            logger.info("✓ Koneksi database berhasil")
            return True
        except Error as e:
            logger.error(f"✗ Error koneksi database: {e}")
            return False
    
    def disconnect(self):
        """Menutup koneksi database"""
        if self._connection:
            self._connection.close()
            self._connection = None
            logger.info("✓ Koneksi database ditutup")
    
    def get_connection(self):
        """
        Mendapatkan koneksi aktif
        
        Returns:
            mysql.connector.MySQLConnection: Koneksi database
        """
        if self._connection is None or not self._connection.is_connected():
            self.connect()
        return self._connection
    
    def execute_query(self, query: str, params: Tuple = None, fetch_all: bool = True) -> Optional[List[Dict]]:
        """
        Execute query ke database
        
        Args:
            query (str): SQL query string
            params (tuple): Parameter untuk query (untuk prepared statement)
            fetch_all (bool): True jika ingin fetch semua hasil
            
        Returns:
            list: List of dictionaries berisi hasil query
        """
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            # Execute query
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Fetch results
            if fetch_all:
                results = cursor.fetchall()
            else:
                results = cursor.fetchone()
            
            cursor.close()
            return results
            
        except Error as e:
            logger.error(f"✗ Error execute query: {e}")
            logger.error(f"  Query: {query}")
            logger.error(f"  Params: {params}")
            return None


# ===================================
# QUERY FUNCTIONS - MAIN OPERATIONS
# ===================================

def load_anime_data() -> List[Dict]:
    """
    Load semua data anime dari database
    Replaces: load_anime_data() di app.py
    
    Returns:
        list: List of anime dictionaries
    """
    db = DatabaseConnection()
    animes = db.execute_query(QUERIES['load_all_animes'])
    logger.info(f"✓ Loaded {len(animes) if animes else 0} animes from database")
    return animes or []


def search_anime(keyword: str, limit: int = 50) -> List[Dict]:
    """
    Search anime berdasarkan keyword di title dan synopsis
    Replaces: search_anime() di app.py
    
    Args:
        keyword (str): Search keyword
        limit (int): Maksimal hasil
        
    Returns:
        list: List of matching animes
    """
    db = DatabaseConnection()
    
    # Prepare fulltext search query
    fulltext_query = ' '.join(f'+{word}*' for word in keyword.split())
    
    results = db.execute_query(
        QUERIES['search_anime'],
        (fulltext_query, keyword, limit)
    )
    
    logger.info(f"✓ Search '{keyword}' returned {len(results) if results else 0} results")
    return results or []


def get_top_rated_anime(limit: int = 10) -> List[Dict]:
    """
    Get top rated anime
    Replaces: get_top_rated_anime() di app.py
    
    Args:
        limit (int): Jumlah anime yang diambil
        
    Returns:
        list: List of top rated animes
    """
    db = DatabaseConnection()
    results = db.execute_query(QUERIES['get_top_rated'], (limit,))
    logger.info(f"✓ Retrieved top {limit} rated animes")
    return results or []


def get_anime_by_type(anime_type: str) -> List[Dict]:
    """
    Get anime berdasarkan type (TV, Movie, OVA, dll)
    Replaces: filter_by_type() di app.py
    
    Args:
        anime_type (str): Tipe anime
        
    Returns:
        list: List of animes with specified type
    """
    db = DatabaseConnection()
    results = db.execute_query(QUERIES['get_by_type'], (anime_type,))
    logger.info(f"✓ Retrieved {len(results) if results else 0} animes of type '{anime_type}'")
    return results or []


def get_anime_by_id(anime_id: int) -> Optional[Dict]:
    """
    Get detail anime by ID
    
    Args:
        anime_id (int): ID anime
        
    Returns:
        dict: Anime data
    """
    db = DatabaseConnection()
    result = db.execute_query(
        QUERIES['get_anime_by_id'],
        (anime_id,),
        fetch_all=False
    )
    return result


def get_all_types() -> List[Dict]:
    """
    Get semua tipe anime
    
    Returns:
        list: List of anime types
    """
    db = DatabaseConnection()
    results = db.execute_query(QUERIES['get_all_types'])
    logger.info(f"✓ Retrieved {len(results) if results else 0} anime types")
    return results or []


def get_statistics() -> List[Dict]:
    """
    Get statistik anime per type
    
    Returns:
        list: List of statistics
    """
    db = DatabaseConnection()
    results = db.execute_query(QUERIES['get_statistics'])
    return results or []


def get_similar_anime(anime_id: int, score_range: float = 0.5, limit: int = 10) -> List[Dict]:
    """
    Get anime yang mirip berdasarkan score range
    
    Args:
        anime_id (int): ID anime referensi
        score_range (float): Range score (+/-)
        limit (int): Limit hasil
        
    Returns:
        list: List of similar animes
    """
    db = DatabaseConnection()
    
    # Get score dari anime referensi
    anime = get_anime_by_id(anime_id)
    if not anime:
        return []
    
    score = anime['score']
    min_score = max(0, score - score_range)
    max_score = min(10, score + score_range)
    
    results = db.execute_query(
        QUERIES['get_similar_score_range'],
        (min_score, max_score, anime_id, limit)
    )
    
    return results or []


# ===================================
# ACTIVITY LOGGING (Opsional)
# ===================================

def log_user_activity(user_id: str, anime_id: int, activity_type: str, search_query: Optional[str] = None):
    """
    Log user activity untuk tracking dan personalisasi
    
    Args:
        user_id (str): Unique identifier untuk user
        anime_id (int): ID anime yang diakses
        activity_type (str): Tipe activity (search, view, recommendation, rating)
        search_query (str): Query jika activity adalah search
    """
    try:
        db = DatabaseConnection()
        query = """
        INSERT INTO user_activity (user_id, anime_id, activity_type, search_query)
        VALUES (%s, %s, %s, %s)
        """
        
        connection = db.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (user_id, anime_id, activity_type, search_query))
        connection.commit()
        cursor.close()
        
        logger.debug(f"✓ Logged activity: {user_id} - {activity_type}")
        
    except Error as e:
        logger.warning(f"⚠ Could not log activity: {e}")


# ===================================
# DATA PREPARATION FOR ML
# ===================================

def get_all_synopses() -> Dict[int, str]:
    """
    Get semua synopsis untuk TF-IDF processing
    
    Returns:
        dict: {anime_id: synopsis}
    """
    animes = load_anime_data()
    synopses = {anime['anime_id']: anime['synopsis'] for anime in animes if anime['synopsis']}
    logger.info(f"✓ Retrieved {len(synopses)} synopses for TF-IDF")
    return synopses


def get_anime_ids_mapping() -> Dict[int, str]:
    """
    Get mapping anime_id ke title untuk recommendation
    
    Returns:
        dict: {anime_id: title}
    """
    animes = load_anime_data()
    mapping = {anime['anime_id']: anime['title'] for anime in animes}
    return mapping


# ===================================
# STREAMLIT SPECIFIC HELPERS
# ===================================

@st.cache_resource(ttl=CACHE_SETTINGS['ttl_anime_data'])
def get_cached_anime_data():
    """
    Get anime data dengan Streamlit cache
    Cache berlaku selama TTL_ANIME_DATA detik
    """
    return load_anime_data()


@st.cache_resource(ttl=CACHE_SETTINGS['ttl_types'])
def get_cached_types():
    """Get anime types dengan Streamlit cache"""
    return get_all_types()


@st.cache_resource(ttl=CACHE_SETTINGS['ttl_statistics'])
def get_cached_statistics():
    """Get statistics dengan Streamlit cache"""
    return get_statistics()


# ===================================
# HEALTH CHECK & UTILITIES
# ===================================

def check_database_health() -> Dict[str, any]:
    """
    Check kesehatan database
    
    Returns:
        dict: Health status information
    """
    db = DatabaseConnection()
    
    health = {
        'connected': False,
        'total_animes': 0,
        'total_types': 0,
        'average_score': 0,
        'error': None
    }
    
    try:
        # Check connection
        if db.get_connection().is_connected():
            health['connected'] = True
        
        # Count animes
        result = db.execute_query("SELECT COUNT(*) as count FROM animes", fetch_all=False)
        if result:
            health['total_animes'] = result['count']
        
        # Count types
        result = db.execute_query("SELECT COUNT(*) as count FROM types", fetch_all=False)
        if result:
            health['total_types'] = result['count']
        
        # Average score
        result = db.execute_query("SELECT AVG(score) as avg_score FROM animes WHERE score > 0", fetch_all=False)
        if result:
            health['average_score'] = float(result['avg_score'] or 0)
        
    except Error as e:
        health['error'] = str(e)
        logger.error(f"✗ Database health check failed: {e}")
    
    return health


def export_to_dict() -> List[Dict]:
    """
    Export semua anime data untuk analisis
    
    Returns:
        list: List of anime dictionaries
    """
    return load_anime_data()


def export_to_json(filename: str = 'anime_export.json') -> bool:
    """
    Export anime data ke JSON file
    
    Args:
        filename (str): Nama file output
        
    Returns:
        bool: True jika berhasil
    """
    try:
        data = load_anime_data()
        # Convert to JSON serializable format
        json_data = json.dumps(data, indent=2, default=str)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(json_data)
        
        logger.info(f"✓ Exported {len(data)} animes to {filename}")
        return True
        
    except Exception as e:
        logger.error(f"✗ Export failed: {e}")
        return False


# ===================================
# INITIALIZATION
# ===================================

if __name__ == "__main__":
    # Test database connection
    db = DatabaseConnection()
    health = check_database_health()
    
    print("\n" + "="*50)
    print("DATABASE HEALTH CHECK")
    print("="*50)
    for key, value in health.items():
        print(f"{key}: {value}")
    print("="*50)
