# ===================================
# SISTEM REKOMENDASI ANIME - STREAMLIT APP (ULTRA-OPTIMIZED)
# Menggunakan sklearn TF-IDF + Content-Based Filtering
# ===================================

# Import library yang diperlukan
import streamlit as st
from db_utils import get_cached_anime_data
import csv
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
st.set_page_config(
    page_title="🎌 Anime Recommender",
    page_icon="🎌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================================
# CSS CUSTOM
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

[data-testid="stMetricValue"] {
    color: #ff006e;
    font-size: 2.5rem;
}

[data-testid="stMetric"] {
    background-color: rgba(255, 0, 110, 0.1);
    padding: 1rem;
    border-radius: 1rem;
    border: 1px solid rgba(255, 0, 110, 0.3);
}

.header-anime {
    background: linear-gradient(135deg, #ff006e 0%, #ff85c0 100%);
    color: white;
    padding: 2rem;
    border-radius: 1rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px rgba(255, 0, 110, 0.2);
}

.header-anime h1 {
    font-size: 2.5rem;
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.header-anime p {
    font-size: 1rem;
    margin: 0.5rem 0 0 0;
    opacity: 0.95;
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
}

p, span {
    color: #e0e0e0;
}

.rating-badge {
    display: inline-block;
    background: linear-gradient(135deg, #ff006e 0%, #ff85c0 100%);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    font-weight: bold;
    margin: 0.5rem 0;
}

.similarity-score {
    background: rgba(255, 0, 110, 0.1);
    border-left: 3px solid #ff006e;
    padding: 0.5rem;
    border-radius: 0.3rem;
    margin: 0.5rem 0;
}

.genre-tag {
    display: inline-block;
    background: rgba(255, 0, 110, 0.2);
    border: 1px solid #ff85c0;
    color: #ff85c0;
    padding: 0.3rem 0.8rem;
    border-radius: 0.3rem;
    margin: 0.2rem;
    font-size: 0.9rem;
}
</style>
"""

st.markdown(dark_anime_style, unsafe_allow_html=True)

# ===================================
# FUNGSI DATA LOADING & CACHING
# ===================================

@st.cache_data(ttl=3600)


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

def display_anime_card(title, score, anime_type, episodes, synopsis, image_url=None, similarity_score=None, matching_types=None):
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
        st.markdown(f"### 🎬 {title}")
        
        info_col1, info_col2, info_col3 = st.columns(3)
        with info_col1:
            st.markdown(f'<span class="rating-badge">⭐ {score}</span>', unsafe_allow_html=True)
        with info_col2:
            st.caption(f"Tipe: {anime_type}")
        with info_col3:
            st.caption(f"Episodes: {episodes if episodes else 'N/A'}")
        
        if matching_types and len(matching_types) > 0:
            matching_html = ''.join([f'<span class="genre-tag" style="background: rgba(76, 175, 80, 0.2); border-color: #4CAF50; color: #4CAF50;">✓ {t}</span>' for t in matching_types])
            st.markdown(f'<div class="similarity-score"><strong>Tipe Sama:</strong> {matching_html}</div>', unsafe_allow_html=True)
        
        if similarity_score is not None:
            similarity_percent = f"{(similarity_score * 100):.1f}%"
            st.markdown(f'<div class="similarity-score">📊 Kesamaan: {similarity_percent}</div>', unsafe_allow_html=True)
        
        st.write(f"**Sinopsis:** {synopsis[:150]}...")

# ===================================
# MAIN APPLICATION
# ===================================

def main():
    """Main app"""
    
    # Load data
    anime_data = get_cached_anime_data()
    
    if not anime_data:
        st.error("❌ Tidak bisa load dataset!")
        return
    
    # Build TF-IDF (CACHED - hanya jalan sekali!)
    with st.spinner("⏳ Memproses dataset anime..."):
        anime_data_tuple = tuple(anime_data)
        tfidf_matrix, genre_vectors, genre_list, tfidf_model = build_tfidf_features(anime_data_tuple)
    
    # Header
    st.markdown("""
        <div class="header-anime">
            <h1>🎌 Sistem Rekomendasi Anime 🎌</h1>
            <p>Temukan anime favorit dengan Content-Based Filtering (sklearn TF-IDF)</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Menu Navigasi")
        page = st.radio(
            "Pilih Halaman:",
            ["🎯 Rekomendasi Anime", "⭐ Top Rating", "🔥 Populer", "🔍 Search & Filter", "📊 Statistics"]
        )
        
        st.markdown("---")
        st.markdown("### 📊 Database Info")
        st.metric("📚 Total Anime", len(anime_data))
        
        st.markdown("---")
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.rerun()
    
    # PAGE 1: REKOMENDASI
    if page == "🎯 Rekomendasi Anime":
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
                            selected_anime_data.get('image_url', '')
                        )
                    
                    st.markdown("---")
                    st.markdown("#### 💎 Rekomendasi Untuk Anda:")
                    
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
                            rec.get('matching_types', None)
                        )
                        st.markdown("---")
    
    # PAGE 2: TOP RATING
    elif page == "⭐ Top Rating":
        st.markdown("### ⭐ Anime Dengan Rating Tertinggi")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("Anime-anime dengan rating terbaik di database kami.")
        
        with col2:
            n_top = st.number_input("Tampilkan", min_value=5, max_value=50, value=10)
        
        top_anime = get_top_rated_anime(anime_data, n_top)
        
        for idx, anime in enumerate(top_anime, 1):
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else "⭐"
            st.markdown(f"### #{idx} {medal}")
            display_anime_card(anime['title'], anime['score'], anime['type'], anime['episodes'], anime['synopsis'], anime.get('image_url', ''))
            st.markdown("---")
    
    # PAGE 3: POPULER
    elif page == "🔥 Populer":
        st.markdown("### 🔥 Anime Populer")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("Anime populer berdasarkan rating.")
        
        with col2:
            n_popular = st.number_input("Tampilkan", min_value=5, max_value=50, value=10, key="popular_num")
        
        popular_anime = get_top_rated_anime(anime_data, n_popular)
        
        for idx, anime in enumerate(popular_anime, 1):
            st.markdown(f"### 🌟 #{idx} - {anime['title']}")
            display_anime_card(anime['title'], anime['score'], anime['type'], anime['episodes'], anime['synopsis'], anime.get('image_url', ''))
            st.markdown("---")
    
    # PAGE 4: SEARCH & FILTER
    elif page == "🔍 Search & Filter":
        st.markdown("### 🔍 Search dan Filter Anime")
        
        tab1, tab2 = st.tabs(["🔎 Search", "📂 Filter Genre"])
        
        with tab1:
            search_term = st.text_input(
                "🔍 Cari anime berdasarkan judul atau sinopsis:",
                placeholder="Masukkan kata kunci..."
            )
            
            if search_term:
                with st.spinner("⏳ Mencari anime..."):
                    search_results = search_anime(anime_data, search_term)
                    
                    if search_results:
                        st.success(f"✅ Ditemukan {len(search_results)} hasil!")
                        for anime in search_results:
                            display_anime_card(anime['title'], anime['score'], anime['type'], anime['episodes'], anime['synopsis'], anime.get('image_url', ''))
                            st.markdown("---")
                    else:
                        st.warning("❌ Tidak ada anime yang sesuai.")
        
        with tab2:
            anime_types = set()
            for anime in anime_data:
                if anime.get('type'):
                    anime_types.add(anime['type'])
            
            anime_types = sorted(list(anime_types))
            selected_types = st.multiselect("📂 Pilih tipe anime:", anime_types)
            
            if selected_types:
                with st.spinner("⏳ Filter anime..."):
                    filtered_anime = []
                    
                    for anime_type in selected_types:
                        filtered_anime.extend(filter_anime_by_type(anime_data, anime_type))
                    
                    seen_titles = set()
                    unique_anime = []
                    for anime in filtered_anime:
                        if anime['title'] not in seen_titles:
                            unique_anime.append(anime)
                            seen_titles.add(anime['title'])
                    
                    st.success(f"✅ Ditemukan {len(unique_anime)} anime!")
                    
                    for anime in unique_anime:
                        display_anime_card(anime['title'], anime['score'], anime['type'], anime['episodes'], anime['synopsis'], anime.get('image_url', ''))
                        st.markdown("---")
    
    # PAGE 5: STATISTICS
    elif page == "📊 Statistics":
        st.markdown("### 📊 Statistik Database Anime")
        
        scores = [float(anime['score']) for anime in anime_data if anime['score']]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📚 Total Anime", len(anime_data))
        
        with col2:
            avg_score = sum(scores) / len(scores) if scores else 0
            st.metric("⭐ Score Rata-rata", f"{avg_score:.2f}")
        
        with col3:
            max_score = max(scores) if scores else 0
            st.metric("🎯 Score Tertinggi", f"{max_score:.2f}")
        
        with col4:
            min_score = min(scores) if scores else 0
            st.metric("📉 Score Terendah", f"{min_score:.2f}")
        
        st.markdown("---")
        st.markdown("#### 🎭 Tipe Anime Paling Banyak")
        
        type_count = defaultdict(int)
        for anime in anime_data:
            anime_type = anime.get('type', 'Unknown')
            type_count[anime_type] += 1
        
        sorted_types = sorted(type_count.items(), key=lambda x: x[1], reverse=True)
        
        for name, count in sorted_types[:10]:
            st.markdown(f"- **{name}**: {count} anime")
    
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
