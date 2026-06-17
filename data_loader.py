# ===================================
# DATA LOADER - CSV BASED (NO MySQL)
# Mengganti db_utils.py untuk sistem yang lebih sederhana
# ===================================

import pandas as pd
import streamlit as st
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===================================
# LOAD DATA FROM CSV
# ===================================

@st.cache_data(ttl=3600)
def get_anime_data():
    """
    Load anime data dari CSV file
    
    Columns yang diperlukan minimal:
    - title (required)
    - score (required)
    - episodes (optional)
    - synopsis (optional)
    - type (optional)
    - image_url (optional)
    
    Returns:
        list: List of anime dictionaries
    """
    try:
        csv_path = "anime.csv"
        
        # Check jika file ada
        if not os.path.exists(csv_path):
            logger.error(f"❌ File not found: {csv_path}")
            logger.error("   Please make sure anime.csv exists in the project root")
            return []
        
        # Load CSV dengan pandas
        logger.info(f"📂 Loading anime data dari {csv_path}...")
        df = pd.read_csv(csv_path)
        
        # Data cleaning
        df = df.fillna("")  # Replace NaN dengan empty string

        # Normalisasi nama kolom agar app tetap kompatibel dengan dataset lama/baru.
        if 'title' not in df.columns and 'name' in df.columns:
            df['title'] = df['name']

        if 'start_date' not in df.columns:
            if 'premiered' in df.columns:
                df['start_date'] = df['premiered']
            else:
                df['start_date'] = ''

        optional_columns = [
            'anime_id', 'image_url', 'synopsis', 'type', 'episodes',
            'genres', 'themes', 'demographics', 'producers', 'studios', 'source',
            'duration', 'rating', 'rank', 'popularity', 'members',
            'favorites', 'scored_by', 'english_name'
        ]

        for column in optional_columns:
            if column not in df.columns:
                df[column] = ''
        
        # Ensure required columns
        required_columns = ['title', 'score']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            logger.error(f"❌ Missing required columns: {missing_columns}")
            logger.error(f"   CSV must have: {required_columns}")
            return []
        
        # Convert score ke float
        df['score'] = pd.to_numeric(df['score'], errors='coerce').fillna(0.0)
        
        # Convert episodes ke string (for consistency)
        if 'episodes' in df.columns:
            df['episodes'] = df['episodes'].astype(str).replace('nan', '')
        else:
            df['episodes'] = ''
        
        df['title'] = df['title'].astype(str)
        df['synopsis'] = df['synopsis'].astype(str)
        df['type'] = df['type'].astype(str)
        df['genres'] = df['genres'].astype(str)

        # Convert to list of dictionaries (same format as database)
        anime_data = df.to_dict(orient='records')
        
        logger.info(f"✅ Successfully loaded {len(anime_data)} anime from CSV")
        return anime_data
        
    except Exception as e:
        logger.error(f"❌ Error loading anime data: {e}")
        return []


def reload_anime_data():
    """
    Force reload anime data (clear cache)
    Gunakan ketika CSV file diupdate
    """
    st.cache_data.clear()
    logger.info("✅ Cache cleared - data will reload on next access")
    return get_anime_data()
