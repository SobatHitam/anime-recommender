# ===================================
# SISTEM REKOMENDASI ANIME - STREAMLIT APP (ULTRA-OPTIMIZED)
# Menggunakan sklearn TF-IDF + Content-Based Filtering
# ===================================

# Import library yang diperlukan
import streamlit as st
from data_loader import get_anime_data
import math
import re
from collections import defaultdict
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from PIL import Image
import os

# Download NLTK data
try:
    nltk.download('stopwords', quiet=True)
except:
    pass

# ===================================
# KONFIGURASI HALAMAN STREAMLIT
# ===================================
# Set page icon - gunakan gambar dari assets jika ada
try:
    icon_path = 'assets/icon.png'
    if os.path.exists(icon_path):
        icon = Image.open(icon_path)
        st.set_page_config(
            page_title="🎌 Anime Recommender",
            page_icon=icon,
            layout="wide",
            initial_sidebar_state="expanded"
        )
    else:
        raise FileNotFoundError
except:
    st.set_page_config(
        page_title="🎌 Anime Recommender",
        page_icon="🎌",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# ===================================
# CSS CUSTOM - ENHANCED STYLING (IMPROVED)
# ===================================
dark_anime_style = """
<style>
* {
    box-sizing: border-box;
}

:root {
    --bg-primary: #0a0e27;
    --bg-secondary: #1a1f3a;
    --accent-color: #ff006e;
    --accent-light: #ff85c0;
    --text-primary: #e0e0e0;
    --text-secondary: #a0a0a0;
    --success: #4CAF50;
    --info: #2196F3;
    --warning: #FFC107;
}

body {
    background-color: #0a0e27;
    color: #e0e0e0;
}

/* ===== METRICS & INDICATORS ===== */
[data-testid="stMetricValue"] {
    color: #ff006e;
    font-size: 2.5rem;
    font-weight: bold;
}

[data-testid="stMetric"] {
    background-color: rgba(255, 0, 110, 0.1);
    padding: 1.5rem;
    border-radius: 1rem;
    border: 1px solid rgba(255, 0, 110, 0.3);
    backdrop-filter: blur(10px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

[data-testid="stMetric"]:hover {
    background-color: rgba(255, 0, 110, 0.15);
    border-color: rgba(255, 0, 110, 0.5);
    box-shadow: 0 8px 24px rgba(255, 0, 110, 0.25);
    transform: translateY(-2px);
}

/* ===== HEADER ===== */
.header-anime {
    background: linear-gradient(135deg, #ff006e 0%, #ff85c0 100%);
    color: white;
    padding: 3rem 2.5rem;
    border-radius: 1.5rem;
    text-align: center;
    margin-bottom: 2.5rem;
    box-shadow: 0 20px 60px rgba(255, 0, 110, 0.35);
    animation: slideDown 0.6s ease-out;
}

@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.header-anime h1 {
    font-size: 3rem;
    margin: 0;
    text-shadow: 4px 4px 8px rgba(0, 0, 0, 0.4);
    letter-spacing: 2px;
    font-weight: 800;
}

.header-anime p {
    font-size: 1.15rem;
    margin: 1rem 0 0 0;
    opacity: 0.95;
    font-weight: 500;
    letter-spacing: 0.5px;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background-color: #0f1428;
    border-right: 2px solid rgba(255, 0, 110, 0.25);
}

/* ===== TYPOGRAPHY ===== */
h1, h2, h3, h4, h5, h6 {
    color: #ff006e;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
}

h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; }
h3 { font-size: 1.5rem; }

p, span, li {
    color: #e0e0e0;
    line-height: 1.6;
}

/* ===== ANIME CARD ===== */
.anime-card {
    background: linear-gradient(135deg, rgba(26, 31, 58, 0.85) 0%, rgba(15, 20, 40, 0.95) 100%);
    border: 1px solid rgba(255, 0, 110, 0.25);
    padding: 2rem;
    border-radius: 1.2rem;
    margin: 1.5rem 0;
    backdrop-filter: blur(10px);
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
}

.anime-card:hover {
    background: linear-gradient(135deg, rgba(26, 31, 58, 1) 0%, rgba(15, 20, 40, 1) 100%);
    border-color: rgba(255, 0, 110, 0.5);
    box-shadow: 0 15px 45px rgba(255, 0, 110, 0.25);
    transform: translateY(-4px);
}

/* ===== BADGES & TAGS ===== */
.rating-badge {
    display: inline-block;
    background: linear-gradient(135deg, #ff006e 0%, #ff85c0 100%);
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 0.8rem;
    font-weight: 600;
    margin: 0.6rem 0.3rem 0.6rem 0;
    box-shadow: 0 6px 20px rgba(255, 0, 110, 0.35);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    font-size: 1rem;
    letter-spacing: 0.5px;
}

.rating-badge:hover {
    box-shadow: 0 10px 30px rgba(255, 0, 110, 0.5);
    transform: scale(1.08) translateY(-2px);
}

.similarity-score {
    background: rgba(255, 0, 110, 0.12);
    border-left: 5px solid #ff006e;
    border-radius: 0.6rem;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    backdrop-filter: blur(5px);
    border-top: 1px solid rgba(255, 0, 110, 0.15);
    border-right: 1px solid rgba(255, 0, 110, 0.15);
    border-bottom: 1px solid rgba(255, 0, 110, 0.15);
    font-weight: 500;
    color: #ff85c0;
}

.genre-tag {
    display: inline-block;
    background: rgba(255, 0, 110, 0.2);
    border: 1.5px solid #ff85c0;
    color: #ff85c0;
    padding: 0.5rem 1rem;
    border-radius: 0.6rem;
    margin: 0.4rem 0.3rem;
    font-size: 0.95rem;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    letter-spacing: 0.3px;
}

.genre-tag:hover {
    background: rgba(255, 0, 110, 0.35);
    border-color: #ff006e;
    color: #ffffff;
    box-shadow: 0 4px 12px rgba(255, 0, 110, 0.3);
    transform: scale(1.05);
}

.episode-badge {
    display: inline-block;
    background: rgba(76, 175, 80, 0.2);
    border: 1.5px solid #4CAF50;
    color: #4CAF50;
    padding: 0.5rem 1rem;
    border-radius: 0.6rem;
    font-weight: 600;
    margin: 0.6rem 0.3rem;
    transition: all 0.3s ease;
    letter-spacing: 0.3px;
}

.episode-badge:hover {
    background: rgba(76, 175, 80, 0.35);
    box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
    transform: scale(1.05);
}

.type-badge {
    display: inline-block;
    background: rgba(33, 150, 243, 0.2);
    border: 1.5px solid #2196F3;
    color: #2196F3;
    padding: 0.5rem 1rem;
    border-radius: 0.6rem;
    font-weight: 600;
    margin: 0.6rem 0.3rem;
    transition: all 0.3s ease;
    letter-spacing: 0.3px;
}

.type-badge:hover {
    background: rgba(33, 150, 243, 0.35);
    box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
    transform: scale(1.05);
}

/* ===== BUTTONS ===== */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #ff006e 0%, #ff85c0 100%) !important;
    color: white !important;
    border: none !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 0.8rem !important;
    font-weight: 600 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 6px 20px rgba(255, 0, 110, 0.3) !important;
    letter-spacing: 0.5px !important;
    font-size: 1rem !important;
}

[data-testid="stButton"] > button:hover {
    box-shadow: 0 10px 30px rgba(255, 0, 110, 0.5) !important;
    transform: translateY(-2px) !important;
}

/* ===== INPUT ELEMENTS ===== */
[data-testid="stSelectbox"] > div > div {
    border-radius: 0.8rem !important;
}

[data-testid="stNumberInput"] > div > div {
    border-radius: 0.8rem !important;
}

/* ===== DIVIDERS ===== */
hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(255, 0, 110, 0.3), transparent);
    margin: 2rem 0;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #0a0e27;
}

::-webkit-scrollbar-thumb {
    background: rgba(255, 0, 110, 0.4);
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 0, 110, 0.6);
}
</style>
"""

st.markdown(dark_anime_style, unsafe_allow_html=True)

# ===================================
# FUNGSI HELPER
# ===================================

def format_episodes(episodes):
    """Format episodes untuk menghapus .0"""
    if not episodes:
        return "N/A"
    try:
        ep_float = float(episodes)
        ep_int = int(ep_float)
        if ep_float == ep_int:
            return str(ep_int)
        return str(ep_float)
    except:
        return str(episodes)


@st.cache_resource
def get_stopwords():
    """Ambil stopwords bahasa Inggris"""
    return set(stopwords.words('english'))

# ===================================
# FUNGSI PREPROCESSING TEXT (SIMPLIFIED - NO LEMMATIZATION)
# ===================================

def preprocess_text(text):
    """
    Preprocessing simplified - tanpa lemmatization (JAUH LEBIH CEPAT)
    """
    if not text:
        return ""
    
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join(text.split())
    
    stop_words = get_stopwords()
    words = text.split()
    processed_words = [word for word in words if word not in stop_words and len(word) > 2]
    
    return ' '.join(processed_words)

# ===================================
# FUNGSI GENRE FEATURE EXTRACTION
# ===================================

def extract_genres(anime_data):
    """Extract unique types dan create binary vectors"""
    all_types = set()
    for anime in anime_data:
        types_str = anime.get('type', '')
        if types_str:
            all_types.add(types_str)
    
    genre_list = sorted(list(all_types))
    
    genre_vectors = []
    for anime in anime_data:
        vector = []
        anime_type = anime.get('type', '')
        for genre in genre_list:
            vector.append(1.0 if anime_type == genre else 0.0)
        genre_vectors.append(vector)
    
    return genre_list, genre_vectors

# ===================================
# FUNGSI TF-IDF DENGAN SKLEARN (CACHED)
# ===================================

@st.cache_resource
def build_tfidf_features(anime_data_tuple):
    """
    Build TF-IDF matrix dengan sklearn (JAUH LEBIH CEPAT)
    @st.cache_resource = hanya jalan SEKALI, tidak rebuild saat rerun
    """
    anime_data = list(anime_data_tuple)
    
    # Preprocess documents
    documents = []
    for anime in anime_data:
        synopsis = anime.get('synopsis', '')
        processed = preprocess_text(synopsis)
        documents.append(processed)
    
    # Build TF-IDF dengan sklearn
    tfidf = TfidfVectorizer(
        max_features=5000,  # PENTING: Batasi vocabulary
        stop_words='english'
    )
    tfidf_matrix = tfidf.fit_transform(documents)
    
    # Extract genre vectors
    genre_list, genre_vectors = extract_genres(anime_data)
    
    return tfidf_matrix, genre_vectors, genre_list, tfidf

def hybrid_similarity(tfidf_sim, genre_sim, tfidf_weight=0.7, genre_weight=0.3):
    """Kombinasi TF-IDF dan genre similarity"""
    return (tfidf_sim * tfidf_weight) + (genre_sim * genre_weight)

def cosine_sim_vectors(vec1, vec2):
    """Calculate cosine similarity antara dua vectors"""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a ** 2 for a in vec1))
    magnitude2 = math.sqrt(sum(b ** 2 for b in vec2))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)

def get_matching_genres(anime1_genres, anime2_genres, genre_list):
    """Dapatkan tipe yang cocok"""
    matching_genres = []
    for i, genre in enumerate(genre_list):
        if anime1_genres[i] == 1.0 and anime2_genres[i] == 1.0:
            matching_genres.append(genre)
    return matching_genres

# ===================================
# FUNGSI REKOMENDASI (OPTIMIZED)
# ===================================

def get_anime_recommendations(anime_title, anime_data, tfidf_matrix, genre_vectors, genre_list, n_recommendations=5):
    """
    Dapatkan rekomendasi dengan sklearn cosine similarity
    OPTIMASI: Hanya hitung similarity untuk anime yang dicari, tidak semua
    """
    anime_index = None
    for i, anime in enumerate(anime_data):
        if anime['title'].lower() == anime_title.lower():
            anime_index = i
            break
    
    if anime_index is None:
        return None
    
    # Hitung similarity dengan sklearn
    similarities_tfidf = cosine_similarity(tfidf_matrix[anime_index], tfidf_matrix)[0]
    
    selected_genre_vector = genre_vectors[anime_index]
    
    similarities = []
    
    for i, anime in enumerate(anime_data):
        if i != anime_index:
            # TF-IDF similarity dari sklearn
            tfidf_sim = similarities_tfidf[i]
            
            # Genre similarity manual (karena vector kecil)
            genre_sim = cosine_sim_vectors(selected_genre_vector, genre_vectors[i])
            
            # Hybrid
            hybrid_sim = hybrid_similarity(tfidf_sim, genre_sim)
            
            # Get matching genres
            matching_types = get_matching_genres(selected_genre_vector, genre_vectors[i], genre_list)
            
            similarities.append((i, hybrid_sim, anime, matching_types))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    recommendations = []
    for idx, sim, anime, matching_types in similarities[:n_recommendations]:
        recommendations.append({
            'title': anime['title'],
            'score': anime['score'],
            'type': anime['type'],
            'episodes': anime['episodes'],
            'synopsis': anime['synopsis'],
            'similarity_score': sim,
            'matching_types': matching_types,
            'image_url': anime.get('image_url', '')
        })
    
    return recommendations

# ===================================
# FUNGSI FILTER & SEARCH
# ===================================

def get_top_rated_anime(anime_data, n=10):
    """Dapatkan anime dengan score tertinggi"""
    sorted_anime = sorted(anime_data, key=lambda x: float(x['score']), reverse=True)
    return sorted_anime[:min(n, 50)]

def filter_anime_by_type(anime_data, anime_type):
    """Filter berdasarkan tipe"""
    filtered = [
        anime for anime in anime_data 
        if anime_type.lower() in anime['type'].lower()
    ]
    filtered.sort(key=lambda x: float(x['score']), reverse=True)
    return filtered[:50]

def search_anime(anime_data, search_term):
    """Search berdasarkan judul atau synopsis"""
    search_lower = search_term.lower()
    results = [
        anime for anime in anime_data
        if search_lower in anime['title'].lower() or search_lower in anime['synopsis'].lower()
    ]
    return results[:20]

# ===================================
# FUNGSI DISPLAY CARD
# ===================================

def set_detail_anime(anime_title):
    """Callback untuk set detail anime"""
    st.session_state.detail_anime = anime_title
    st.session_state.show_detail = True

def go_back_to_recommendations():
    """Callback untuk kembali ke halaman rekomendasi"""
    st.session_state.show_detail = False
    st.session_state.detail_anime = None

def display_anime_card(title, score, anime_type, episodes, synopsis, image_url=None, similarity_score=None, matching_types=None, clickable=False):
    """Display anime card dengan layout yang diperbaiki"""
    col_img, col_info = st.columns([0.8, 2.2], gap="medium")
    
    with col_img:
        if image_url:
            try:
                st.image(image_url, width=150, use_container_width=True, caption="")
            except:
                st.markdown(
                    '<div style="width: 150px; height: 220px; background: rgba(255, 0, 110, 0.2); display: flex; align-items: center; justify-content: center; border-radius: 0.8rem; border: 2px solid rgba(255, 0, 110, 0.3); font-size: 3rem;">🎬</div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                '<div style="width: 150px; height: 220px; background: rgba(255, 0, 110, 0.2); display: flex; align-items: center; justify-content: center; border-radius: 0.8rem; border: 2px solid rgba(255, 0, 110, 0.3); font-size: 3rem;">🎬</div>',
                unsafe_allow_html=True
            )
    
    with col_info:
        if clickable:
            st.markdown(f'<h3 style="color: #ff006e; margin: 0 0 1rem 0; cursor: pointer;">🎬 {title}</h3>', unsafe_allow_html=True)
            st.button(f"Lihat Detail", key=f"detail_{title}_{hash(title) % 10000}", use_container_width=False, on_click=set_detail_anime, args=(title,))
        else:
            st.markdown(f'<h3 style="color: #ff006e; margin: 0 0 1rem 0;">🎬 {title}</h3>', unsafe_allow_html=True)
        
        # Info badges dalam satu baris
        badge_col1, badge_col2, badge_col3 = st.columns(3, gap="small")
        with badge_col1:
            st.markdown(f'<div style="text-align: center; background: rgba(255, 193, 7, 0.15); padding: 0.8rem; border-radius: 0.6rem; border: 1px solid rgba(255, 193, 7, 0.4);"><span style="color: #a0a0a0; font-size: 0.8rem;">⭐ RATING</span><br><span style="color: #FFC107; font-weight: bold; font-size: 1.3rem;">{score}</span></div>', unsafe_allow_html=True)
        
        with badge_col2:
            st.markdown(f'<div style="text-align: center; background: rgba(33, 150, 243, 0.15); padding: 0.8rem; border-radius: 0.6rem; border: 1px solid rgba(33, 150, 243, 0.4);"><span style="color: #a0a0a0; font-size: 0.8rem;">🎭 TIPE</span><br><span style="color: #2196F3; font-weight: bold; font-size: 1.3rem;">{anime_type}</span></div>', unsafe_allow_html=True)
        
        with badge_col3:
            st.markdown(f'<div style="text-align: center; background: rgba(76, 175, 80, 0.15); padding: 0.8rem; border-radius: 0.6rem; border: 1px solid rgba(76, 175, 80, 0.4);"><span style="color: #a0a0a0; font-size: 0.8rem;">📺 EP</span><br><span style="color: #4CAF50; font-weight: bold; font-size: 1.3rem;">{format_episodes(episodes)}</span></div>', unsafe_allow_html=True)
        
        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        
        # Matching types
        if matching_types and len(matching_types) > 0:
            matching_html = ''.join([f'<span class="genre-tag" style="background: rgba(76, 175, 80, 0.2); border-color: #4CAF50; color: #4CAF50;">✓ {t}</span>' for t in matching_types])
            st.markdown(f'<div style="margin-bottom: 0.8rem;"><strong style="color: #ff85c0;">✓ Tipe Cocok:</strong><br>{matching_html}</div>', unsafe_allow_html=True)
        
        # Similarity score
        if similarity_score is not None:
            similarity_percent = f"{(similarity_score * 100):.1f}%"
            st.markdown(f'<div class="similarity-score"><strong>📊 Kesamaan Konten:</strong> <span style="color: #ff006e; font-weight: bold; font-size: 1.1rem;">{similarity_percent}</span></div>', unsafe_allow_html=True)
        
        # Synopsis
        st.markdown(f'<p style="color: #a0a0a0; line-height: 1.5; margin-top: 1rem;"><strong style="color: #ff85c0;">📖 Sinopsis:</strong><br>{synopsis[:180]}...</p>', unsafe_allow_html=True)

# ===================================
# FUNGSI DISPLAY DETAIL ANIME (HALAMAN BARU)
# ===================================

def display_anime_detail_page(anime_data, anime_title):
    """Tampilkan halaman detail lengkap anime dengan layout yang diperbaiki"""
    # Cari anime berdasarkan judul
    selected_anime = next(
        (a for a in anime_data if a['title'] == anime_title),
        None
    )
    
    if not selected_anime:
        st.error("❌ Anime tidak ditemukan!")
        return
    
    # Button kembali
    col1, col2 = st.columns([1, 10])
    with col1:
        st.button("⬅️ Kembali", use_container_width=True, on_click=go_back_to_recommendations)
    
    st.markdown("---")
    
    # Layout: Poster di kiri (sedang), Detail di kanan
    col_img, col_info = st.columns([1.2, 1.5], gap="large")
    
    with col_img:
        # Poster Anime dengan ukuran sedang
        if selected_anime.get('image_url'):
            try:
                st.image(selected_anime['image_url'], width=250, use_container_width=False)
            except:
                st.markdown(
                    '<div style="width: 250px; height: 350px; background: rgba(255, 0, 110, 0.2); display: flex; align-items: center; justify-content: center; border-radius: 1rem; border: 2px solid rgba(255, 0, 110, 0.3); font-size: 3rem;">🎬</div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                '<div style="width: 250px; height: 350px; background: rgba(255, 0, 110, 0.2); display: flex; align-items: center; justify-content: center; border-radius: 1rem; border: 2px solid rgba(255, 0, 110, 0.3); font-size: 3rem;">🎬</div>',
                unsafe_allow_html=True
            )
    
    with col_info:
        # Judul
        st.markdown(f"<h2 style='color: #ff006e; margin-bottom: 1.5rem;'>🎬 {selected_anime['title']}</h2>", unsafe_allow_html=True)
        
        # Info Cards - Label dan Value terpisah dengan styling yang lebih baik
        st.markdown("<div style='margin: 1rem 0;'>", unsafe_allow_html=True)
        
        # TYPE
        st.markdown(
            f"""<div style='background: linear-gradient(135deg, rgba(33, 150, 243, 0.15) 0%, rgba(33, 150, 243, 0.08) 100%); 
            padding: 1.3rem; border-radius: 0.9rem; text-align: center; border: 1.5px solid rgba(33, 150, 243, 0.4); 
            margin-bottom: 0.9rem; transition: all 0.3s ease;'>
            <p style='color: #a0a0a0; font-size: 0.8rem; margin: 0; letter-spacing: 1px; font-weight: 600;'>🎭 TIPE</p>
            <h3 style='color: #2196F3; margin: 0.6rem 0 0 0; font-size: 1.5rem; font-weight: 800;'>{selected_anime['type']}</h3>
            </div>""",
            unsafe_allow_html=True
        )
        
        # EPISODES
        st.markdown(
            f"""<div style='background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(76, 175, 80, 0.08) 100%); 
            padding: 1.3rem; border-radius: 0.9rem; text-align: center; border: 1.5px solid rgba(76, 175, 80, 0.4); 
            margin-bottom: 0.9rem; transition: all 0.3s ease;'>
            <p style='color: #a0a0a0; font-size: 0.8rem; margin: 0; letter-spacing: 1px; font-weight: 600;'>📺 EPISODE</p>
            <h3 style='color: #4CAF50; margin: 0.6rem 0 0 0; font-size: 1.5rem; font-weight: 800;'>{format_episodes(selected_anime['episodes'])}</h3>
            </div>""",
            unsafe_allow_html=True
        )
        
        # RATING
        st.markdown(
            f"""<div style='background: linear-gradient(135deg, rgba(255, 193, 7, 0.15) 0%, rgba(255, 193, 7, 0.08) 100%); 
            padding: 1.3rem; border-radius: 0.9rem; text-align: center; border: 1.5px solid rgba(255, 193, 7, 0.4);'>
            <p style='color: #a0a0a0; font-size: 0.8rem; margin: 0; letter-spacing: 1px; font-weight: 600;'>⭐ RATING</p>
            <h3 style='color: #FFC107; margin: 0.6rem 0 0 0; font-size: 1.5rem; font-weight: 800;'>{selected_anime['score']}/10</h3>
            </div>""",
            unsafe_allow_html=True
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sinopsis Lengkap (Full Width)
    st.markdown("## 📖 Sinopsis Lengkap")
    st.markdown(
        f"""<div style='background: rgba(255, 0, 110, 0.08); padding: 1.5rem; border-radius: 0.9rem; 
        border-left: 4px solid #ff006e; line-height: 1.8; color: #e0e0e0;'>
        {selected_anime['synopsis']}
        </div>""",
        unsafe_allow_html=True
    )
    
    st.markdown("---")

# ===================================
# MAIN APPLICATION
# ===================================

def main():
    """Main app"""
    
    # Initialize session state
    if 'show_detail' not in st.session_state:
        st.session_state.show_detail = False
    if 'detail_anime' not in st.session_state:
        st.session_state.detail_anime = None
    
    # Load data dari CSV (bukan database)
    anime_data = get_anime_data()
    
    if not anime_data:
        st.error("❌ Tidak bisa load dataset! Pastikan anime.csv ada di folder project.")
        return
    
    # Header
    st.markdown("""
        <div class="header-anime">
            <h1>🎌 Sistem Rekomendasi Anime 🎌</h1>
            <p>Temukan anime favorit dengan Content-Based Filtering (sklearn TF-IDF)</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Jika user klik untuk melihat detail, tampilkan halaman detail
    if st.session_state.show_detail and st.session_state.detail_anime:
        display_anime_detail_page(anime_data, st.session_state.detail_anime)
        return
    
    # Build TF-IDF (CACHED - hanya jalan sekali!)
    with st.spinner("⏳ Memproses dataset anime..."):
        anime_data_tuple = tuple(anime_data)
        tfidf_matrix, genre_vectors, genre_list, tfidf_model = build_tfidf_features(anime_data_tuple)
    
    # MAIN PAGE: REKOMENDASI ANIME SESUAI DOKUMENTASI DESAIN
    if True:
        st.markdown("### 🎯 Dapatkan Rekomendasi Anime")
        st.markdown("**Metode:** Content-Based Filtering dengan TF-IDF + Type Matching")
        
        col1, col2 = st.columns([2, 1], gap="medium")
        anime_titles = [anime['title'] for anime in anime_data]
        
        with col1:
            selected_anime = st.selectbox(
                "Pilih anime favorit Anda:",
                anime_titles,
                help="Pilih anime untuk mendapatkan rekomendasi yang mirip"
            )
        
        with col2:
            n_recommendations = st.number_input(
                "Jumlah rekomendasi:",
                min_value=1,
                max_value=10,
                value=5,
                help="Berapa banyak rekomendasi yang ingin ditampilkan?"
            )
        
        if st.button("💡 Tampilkan Rekomendasi", key="rec_button", use_container_width=True):
            with st.spinner("⏳ Mencari rekomendasi anime yang cocok..."):
                recommendations = get_anime_recommendations(
                    selected_anime, anime_data, tfidf_matrix, genre_vectors, genre_list, n_recommendations
                )
                
                if recommendations:
                    st.success("✅ Rekomendasi ditemukan!")
                    
                    st.markdown("---")
                    
                    # Anime yang dipilih
                    st.markdown("#### 🎬 Anime yang Anda Pilih")
                    selected_anime_data = next((a for a in anime_data if a['title'] == selected_anime), None)
                    
                    if selected_anime_data:
                        display_anime_card(
                            selected_anime_data['title'],
                            selected_anime_data['score'],
                            selected_anime_data['type'],
                            selected_anime_data['episodes'],
                            selected_anime_data['synopsis'],
                            selected_anime_data.get('image_url', ''),
                            clickable=True
                        )
                    
                    st.markdown("---")
                    st.markdown("#### 💎 Rekomendasi Untuk Anda")
                    st.markdown("*Klik 'Lihat Detail' pada kartu anime untuk informasi lengkap*")
                    st.markdown("")
                    
                    for idx, rec in enumerate(recommendations, 1):
                        col_num, col_sim = st.columns([3, 1])
                        with col_num:
                            st.markdown(f"**#{idx}** - {rec['title']}")
                        with col_sim:
                            sim_percent = f"{(rec['similarity_score']*100):.0f}%"
                            st.markdown(f'<span style="background: rgba(255, 0, 110, 0.2); padding: 0.4rem 0.8rem; border-radius: 0.5rem; color: #ff85c0; font-weight: bold;">{sim_percent}</span>', unsafe_allow_html=True)
                        
                        display_anime_card(
                            rec['title'],
                            rec['score'],
                            rec['type'],
                            rec['episodes'],
                            rec['synopsis'],
                            rec.get('image_url', ''),
                            rec.get('similarity_score', None),
                            rec.get('matching_types', None),
                            clickable=True
                        )
                        st.markdown("---")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #a0a0a0; margin-top: 3rem; padding: 2rem 1rem; border-top: 1px solid rgba(255, 0, 110, 0.15);">
            <p style="font-size: 1.2rem; font-weight: bold; color: #ff006e; margin-bottom: 0.5rem;">🎌 Sistem Rekomendasi Anime 🎌</p>
            <p style="margin: 0.3rem 0; color: #e0e0e0;">Temukan anime favorit dengan teknologi Content-Based Filtering</p>
            <p style="margin: 0.5rem 0; font-size: 0.95rem;">Dibuat dengan ❤️ menggunakan <strong style="color: #ff85c0;">Streamlit</strong> & <strong style="color: #ff85c0;">sklearn TF-IDF</strong></p>
            <p style="font-size: 0.85rem; margin-top: 1rem;">© 2026 - Content-Based Filtering (ULTRA-OPTIMIZED)</p>
        </div>
    """, unsafe_allow_html=True)

# Run
if __name__ == "__main__":
    main()
