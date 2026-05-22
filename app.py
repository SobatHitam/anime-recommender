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
    with open('assets/icon.png', 'rb') as icon_file:
        icon = icon_file
    st.set_page_config(
        page_title="🎌 Anime Recommender",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )
except:
    st.set_page_config(
        page_title="🎌 Anime Recommender",
        page_icon="🎌",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# ===================================
# CSS CUSTOM - ENHANCED STYLING
# ===================================
dark_anime_style = """
<style>
:root {
    --bg-primary: #0a0e27;
    --bg-secondary: #1a1f3a;
    --accent-color: #ff006e;
    --accent-light: #ff85c0;
    --text-primary: #e0e0e0;
    --text-secondary: #a0a0a0;
}

body {
    background-color: #0a0e27;
}

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
    transition: all 0.3s ease;
}

[data-testid="stMetric"]:hover {
    background-color: rgba(255, 0, 110, 0.15);
    border-color: rgba(255, 0, 110, 0.5);
    box-shadow: 0 5px 20px rgba(255, 0, 110, 0.2);
}

.header-anime {
    background: linear-gradient(135deg, #ff006e 0%, #ff85c0 100%);
    color: white;
    padding: 2.5rem;
    border-radius: 1.5rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 15px 50px rgba(255, 0, 110, 0.3);
}

.header-anime h1 {
    font-size: 2.8rem;
    margin: 0;
    text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.4);
    letter-spacing: 1px;
}

.header-anime p {
    font-size: 1.1rem;
    margin: 0.8rem 0 0 0;
    opacity: 0.98;
    font-weight: 500;
}

.anime-card {
    background: linear-gradient(135deg, rgba(26, 31, 58, 0.8) 0%, rgba(15, 20, 40, 0.9) 100%);
    border: 1px solid rgba(255, 0, 110, 0.2);
    padding: 1.5rem;
    border-radius: 1rem;
    margin: 1rem 0;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.anime-card:hover {
    background: linear-gradient(135deg, rgba(26, 31, 58, 1) 0%, rgba(15, 20, 40, 1) 100%);
    border-color: rgba(255, 0, 110, 0.4);
    box-shadow: 0 12px 35px rgba(255, 0, 110, 0.2);
    transform: translateY(-2px);
}

.title-section {
    color: #ff006e;
    font-size: 1.8rem;
    font-weight: bold;
    margin: 1.5rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(255, 0, 110, 0.3);
}

[data-testid="stSidebar"] {
    background-color: #0f1428;
    border-right: 2px solid rgba(255, 0, 110, 0.2);
}

h1, h2, h3, h4, h5, h6 {
    color: #ff006e;
    font-weight: 700;
    letter-spacing: 0.5px;
}

p, span {
    color: #e0e0e0;
}

.rating-badge {
    display: inline-block;
    background: linear-gradient(135deg, #ff006e 0%, #ff85c0 100%);
    color: white;
    padding: 0.6rem 1.2rem;
    border-radius: 0.7rem;
    font-weight: bold;
    margin: 0.5rem 0;
    box-shadow: 0 5px 15px rgba(255, 0, 110, 0.3);
    transition: all 0.3s ease;
}

.rating-badge:hover {
    box-shadow: 0 8px 20px rgba(255, 0, 110, 0.5);
    transform: scale(1.05);
}

.similarity-score {
    background: rgba(255, 0, 110, 0.15);
    border-left: 4px solid #ff006e;
    border-radius: 0.5rem;
    padding: 0.8rem;
    margin: 0.8rem 0;
    backdrop-filter: blur(5px);
}

.genre-tag {
    display: inline-block;
    background: rgba(255, 0, 110, 0.2);
    border: 1px solid #ff85c0;
    color: #ff85c0;
    padding: 0.4rem 0.9rem;
    border-radius: 0.5rem;
    margin: 0.3rem;
    font-size: 0.95rem;
    font-weight: 500;
    transition: all 0.3s ease;
}

.genre-tag:hover {
    background: rgba(255, 0, 110, 0.3);
    border-color: #ff006e;
    color: #ff006e;
}

.episode-badge {
    display: inline-block;
    background: rgba(76, 175, 80, 0.2);
    border: 1px solid #4CAF50;
    color: #4CAF50;
    padding: 0.4rem 0.9rem;
    border-radius: 0.5rem;
    font-weight: 500;
}

.type-badge {
    display: inline-block;
    background: rgba(33, 150, 243, 0.2);
    border: 1px solid #2196F3;
    color: #2196F3;
    padding: 0.4rem 0.9rem;
    border-radius: 0.5rem;
    font-weight: 500;
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
    """Display anime card dengan gambar"""
    col_img, col_info = st.columns([1, 3])
    
    with col_img:
        if image_url:
            try:
                st.image(image_url, width=120, use_container_width=False)
            except:
                st.markdown("🎬", unsafe_allow_html=True)
        else:
            st.markdown("🎬", unsafe_allow_html=True)
    
    with col_info:
        if clickable:
            st.button(f"🎬 {title}", key=f"detail_{title}", use_container_width=False, on_click=set_detail_anime, args=(title,))
        else:
            st.markdown(f"### 🎬 {title}")
        
        info_col1, info_col2, info_col3 = st.columns(3)
        with info_col1:
            st.markdown(f'<span class="rating-badge">⭐ {score}</span>', unsafe_allow_html=True)
        with info_col2:
            st.markdown(f'<span class="type-badge"> {anime_type}</span>', unsafe_allow_html=True)
        with info_col3:
            st.markdown(f'<span class="episode-badge"> {format_episodes(episodes)}</span>', unsafe_allow_html=True)
        
        if matching_types and len(matching_types) > 0:
            matching_html = ''.join([f'<span class="genre-tag" style="background: rgba(76, 175, 80, 0.2); border-color: #4CAF50; color: #4CAF50;">✓ {t}</span>' for t in matching_types])
            st.markdown(f'<div class="similarity-score"><strong>Tipe Sama:</strong> {matching_html}</div>', unsafe_allow_html=True)
        
        if similarity_score is not None:
            similarity_percent = f"{(similarity_score * 100):.1f}%"
            st.markdown(f'<div class="similarity-score">📊 Kesamaan: {similarity_percent}</div>', unsafe_allow_html=True)
        
        st.write(f"**Sinopsis:** {synopsis[:150]}...")

# ===================================
# FUNGSI DISPLAY DETAIL ANIME (HALAMAN BARU)
# ===================================

def display_anime_detail_page(anime_data, anime_title):
    """Tampilkan halaman detail lengkap anime"""
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
    
    # Layout: Poster di kiri, Detail di kanan
    col_img, col_info = st.columns([1.5, 2])
    
    with col_img:
        # Poster Anime
        if selected_anime.get('image_url'):
            try:
                st.image(selected_anime['image_url'], use_container_width=True)
            except:
                st.markdown("### 🎬")
        else:
            st.markdown("### 🎬")
    
    with col_info:
        # Judul
        st.markdown(f"# {selected_anime['title']}")
        
        st.markdown("<div style='margin: 1.5rem 0;'>", unsafe_allow_html=True)
        
        # Info Cards dalam satu baris
        detail_col1, detail_col2, detail_col3 = st.columns(3)
        
        with detail_col1:
            st.markdown("<div style='background: rgba(255, 0, 110, 0.1); padding: 1rem; border-radius: 0.8rem; text-align: center; border: 1px solid rgba(255, 0, 110, 0.3);'>", unsafe_allow_html=True)
            st.markdown("<p style='color: #a0a0a0; font-size: 0.9rem; margin-bottom: 0.5rem;'>🎭 TIPE</p>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='color: #ff006e; margin: 0;'>{selected_anime['type']}</h3>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with detail_col2:
            st.markdown("<div style='background: rgba(76, 175, 80, 0.1); padding: 1rem; border-radius: 0.8rem; text-align: center; border: 1px solid rgba(76, 175, 80, 0.3);'>", unsafe_allow_html=True)
            st.markdown("<p style='color: #a0a0a0; font-size: 0.9rem; margin-bottom: 0.5rem;'>📺 EPISODES</p>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='color: #4CAF50; margin: 0;'>{format_episodes(selected_anime['episodes'])}</h3>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with detail_col3:
            st.markdown("<div style='background: rgba(255, 193, 7, 0.1); padding: 1rem; border-radius: 0.8rem; text-align: center; border: 1px solid rgba(255, 193, 7, 0.3);'>", unsafe_allow_html=True)
            st.markdown("<p style='color: #a0a0a0; font-size: 0.9rem; margin-bottom: 0.5rem;'>⭐ RATING</p>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='color: #FFC107; margin: 0;'>{selected_anime['score']}/10</h3>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sinopsis Lengkap (Full Width)
    st.markdown("## 📖 Sinopsis Lengkap")
    st.write(selected_anime['synopsis'])
    
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
        st.markdown("**Metode:** Content-Based Filtering (TF-IDF + Type Matching)")
        
        col1, col2 = st.columns([2, 1])
        anime_titles = [anime['title'] for anime in anime_data]
        
        with col1:
            selected_anime = st.selectbox(
                "Pilih anime favorit Anda:",
                anime_titles,
                help="Pilih anime untuk mendapatkan rekomendasi"
            )
        
        with col2:
            n_recommendations = st.number_input(
                "Jumlah rekomendasi:",
                min_value=1,
                max_value=10,
                value=5
            )
        
        if st.button("💡 Tampilkan Rekomendasi", key="rec_button", use_container_width=True):
            with st.spinner("⏳ Mencari rekomendasi..."):
                recommendations = get_anime_recommendations(
                    selected_anime, anime_data, tfidf_matrix, genre_vectors, genre_list, n_recommendations
                )
                
                if recommendations:
                    st.success("✅ Rekomendasi ditemukan!")
                    
                    st.markdown("---")
                    st.markdown("#### 🎬 Anime yang Anda Pilih:")
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
                    st.markdown("#### 💎 Rekomendasi Untuk Anda:")
                    st.markdown("*Klik pada judul anime untuk melihat detail lengkap*")
                    
                    for idx, rec in enumerate(recommendations, 1):
                        st.markdown(f"**#{idx}** - Kesamaan: `{(rec['similarity_score']*100):.1f}%`")
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
        <div style="text-align: center; color: #a0a0a0; margin-top: 2rem; padding: 1rem;">
            <p>🎌 <strong>Sistem Rekomendasi Anime</strong> 🎌</p>
            <p>Dibuat dengan ❤️ menggunakan Streamlit dan sklearn TF-IDF</p>
            <p style="font-size: 0.9rem;">© 2026 - Content-Based Filtering (ULTRA-OPTIMIZED)</p>
        </div>
    """, unsafe_allow_html=True)

# Run
if __name__ == "__main__":
    main()
