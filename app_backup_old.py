# ===================================
# SISTEM REKOMENDASI ANIME - STREAMLIT APP (SIMPLIFIED)
# Menggunakan Content-Based Filtering dengan TF-IDF dan Cosine Similarity
# Versi tanpa Pandas/Numpy (untuk kompatibilitas Python 3.14)
# ===================================

# Import library yang diperlukan
import streamlit as st
import csv
import math
import re
from collections import defaultdict
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK data yang diperlukan untuk text preprocessing
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
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
# CSS CUSTOM UNTUK DARK MODE ANIME STYLE
# ===================================
dark_anime_style = """
<style>
/* Warna background dan text */
:root {
    --bg-primary: #0a0e27;
    --bg-secondary: #1a1f3a;
    --accent-color: #ff006e;
    --accent-light: #ff85c0;
    --text-primary: #e0e0e0;
    --text-secondary: #a0a0a0;
}

/* Custom styling untuk Streamlit */
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

/* Header styling */
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

/* Title styling */
.title-section {
    color: #ff006e;
    font-size: 1.8rem;
    font-weight: bold;
    margin: 1.5rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(255, 0, 110, 0.3);
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #0f1428;
    border-right: 2px solid rgba(255, 0, 110, 0.2);
}

/* Text styling */
h1, h2, h3, h4, h5, h6 {
    color: #ff006e;
}

p, span {
    color: #e0e0e0;
}

/* Rating display */
.rating-badge {
    display: inline-block;
    background: linear-gradient(135deg, #ff006e 0%, #ff85c0 100%);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    font-weight: bold;
    margin: 0.5rem 0;
}

/* Similarity score */
.similarity-score {
    background: rgba(255, 0, 110, 0.1);
    border-left: 3px solid #ff006e;
    padding: 0.5rem;
    border-radius: 0.3rem;
    margin: 0.5rem 0;
}

/* Genre tag */
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
def load_anime_data():
    """
    Load dataset anime dari CSV
    """
    anime_data = []
    try:
        with open('anime.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row['score'] = float(row['score'])
                    anime_data.append(row)
                except:
                    continue
    except FileNotFoundError:
        st.error("❌ File anime.csv tidak ditemukan!")
        return []
    
    return anime_data

@st.cache_resource
def get_stopwords():
    """
    Mengambil list stopwords bahasa Inggris untuk filtering
    """
    return set(stopwords.words('english'))

# ===================================
# FUNGSI PREPROCESSING TEXT
# ===================================

def preprocess_text(text):
    """
    Melakukan preprocessing pada text:
    - Ubah ke lowercase
    - Hapus karakter khusus
    - Hapus stopwords
    - Lemmatization
    """
    # Ubah ke lowercase
    text = text.lower()
    
    # Hapus URL
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Hapus karakter khusus dan angka
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Hapus spasi berlebih
    text = ' '.join(text.split())
    
    # Hapus stopwords dan lakukan lemmatization
    stop_words = get_stopwords()
    lemmatizer = WordNetLemmatizer()
    
    words = text.split()
    processed_words = []
    for word in words:
        if word not in stop_words and len(word) > 2:  # Filter stopwords dan kata pendek
            lemma = lemmatizer.lemmatize(word)
            processed_words.append(lemma)
    
    return ' '.join(processed_words)

# ===================================
# FUNGSI GENRE FEATURE EXTRACTION (TYPE-BASED)
# ===================================

def extract_genres(anime_data):
    """
    Extract dan buat binary encoding untuk anime types
    Karena dataset tidak memiliki genre column, kita gunakan type sebagai feature
    Mengembalikan: genre_list, genre_vectors
    """
    # Collect all unique types
    all_types = set()
    for anime in anime_data:
        types_str = anime.get('type', '')
        if types_str:
            all_types.add(types_str)
    
    genre_list = sorted(list(all_types))
    
    # Create binary vectors for types
    genre_vectors = []
    for anime in anime_data:
        vector = []
        anime_type = anime.get('type', '')
        
        for genre in genre_list:
            vector.append(1.0 if anime_type == genre else 0.0)
        
        genre_vectors.append(vector)
    
    return genre_list, genre_vectors

# ===================================
# FUNGSI TF-IDF MANUAL IMPLEMENTATION
# ===================================

def build_tfidf_features(anime_data):
    """
    Build TF-IDF features untuk semua anime
    Menggabungkan synopsis sebagai content
    Mengembalikan: documents, vocabulary, tf_vectors, genre_vectors, genre_list
    """
    # Prepare content untuk setiap anime (gunakan synopsis)
    documents = []
    for anime in anime_data:
        # Gunakan synopsis sebagai main content
        synopsis = anime.get('synopsis', '')
        processed_content = preprocess_text(synopsis)
        documents.append(processed_content)
    
    # Build vocabulary
    vocabulary = set()
    for doc in documents:
        vocabulary.update(doc.split())
    
    vocabulary = sorted(list(vocabulary))
    
    # Calculate IDF
    idf = {}
    n_docs = len(documents)
    
    for term in vocabulary:
        doc_count = sum(1 for doc in documents if term in doc.split())
        if doc_count > 0:
            idf[term] = math.log(n_docs / doc_count)
        else:
            idf[term] = 0
    
    # Calculate TF-IDF vectors
    tf_vectors = []
    for doc in documents:
        vector = []
        terms = doc.split()
        
        for term in vocabulary:
            # Calculate TF
            tf = terms.count(term) / max(len(terms), 1)
            
            # TF-IDF
            tfidf_value = tf * idf.get(term, 0)
            vector.append(tfidf_value)
        
        tf_vectors.append(vector)
    
    # Extract type vectors (since no genre column)
    genre_list, genre_vectors = extract_genres(anime_data)
    
    return documents, vocabulary, tf_vectors, genre_vectors, genre_list

def cosine_similarity(vec1, vec2):
    """
    Calculate cosine similarity between two vectors
    """
    if len(vec1) != len(vec2):
        return 0.0
    
    # Dot product
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    
    # Magnitudes
    magnitude1 = math.sqrt(sum(a ** 2 for a in vec1))
    magnitude2 = math.sqrt(sum(b ** 2 for b in vec2))
    
    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)

def hybrid_similarity(tfidf_sim, genre_sim, tfidf_weight=0.7, genre_weight=0.3):
    """
    Menghitung hybrid similarity dengan kombinasi TF-IDF dan Genre
    """
    return (tfidf_sim * tfidf_weight) + (genre_sim * genre_weight)

def get_matching_genres(anime1_genres, anime2_genres, genre_list):
    """
    Dapatkan tipe yang cocok antara dua anime
    (Karena dataset tidak punya genre, ini menggunakan type matching)
    """
    matching_genres = []
    for i, genre in enumerate(genre_list):
        if anime1_genres[i] == 1.0 and anime2_genres[i] == 1.0:
            matching_genres.append(genre)
    return matching_genres

# ===================================
# FUNGSI REKOMENDASI
# ===================================

def get_anime_recommendations(anime_title, anime_data, tf_vectors, genre_vectors, genre_list, n_recommendations=5):
    """
    Mendapatkan rekomendasi anime berdasarkan anime yang dipilih
    Menggunakan hybrid similarity (TF-IDF + Type Matching)
    """
    # Cari index anime yang dipilih
    anime_index = None
    for i, anime in enumerate(anime_data):
        if anime['title'].lower() == anime_title.lower():
            anime_index = i
            break
    
    if anime_index is None:
        return None
    
    # Hitung similaritas dengan semua anime lain
    selected_tfidf_vector = tf_vectors[anime_index]
    selected_genre_vector = genre_vectors[anime_index]
    
    similarities = []
    
    for i, anime in enumerate(anime_data):
        if i != anime_index:
            # Hitung TF-IDF similarity
            tfidf_sim = cosine_similarity(selected_tfidf_vector, tf_vectors[i])
            
            # Hitung Type similarity
            genre_sim = cosine_similarity(selected_genre_vector, genre_vectors[i])
            
            # Hitung hybrid similarity
            hybrid_sim = hybrid_similarity(tfidf_sim, genre_sim)
            
            # Get matching types
            matching_types = get_matching_genres(selected_genre_vector, genre_vectors[i], genre_list)
            
            similarities.append((i, hybrid_sim, anime, matching_types))
    
    # Sort by similarity
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Return top-N
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
    """
    Mendapatkan anime dengan score tertinggi dari MyAnimeList
    """
    sorted_anime = sorted(anime_data, key=lambda x: float(x['score']), reverse=True)
    return sorted_anime[:n]

def filter_anime_by_type(anime_data, anime_type):
    """
    Filter anime berdasarkan tipe (TV, Movie, OVA, dll)
    """
    filtered = [
        anime for anime in anime_data 
        if anime_type.lower() in anime['type'].lower()
    ]
    filtered.sort(key=lambda x: float(x['score']), reverse=True)
    return filtered

def search_anime(anime_data, search_term):
    """
    Search anime berdasarkan judul atau sinopsis
    """
    search_lower = search_term.lower()
    results = [
        anime for anime in anime_data
        if search_lower in anime['title'].lower() or search_lower in anime['synopsis'].lower()
    ]
    return results[:10]

# ===================================
# FUNGSI DISPLAY CARD ANIME
# ===================================

def display_anime_card(title, score, anime_type, episodes, synopsis, image_url=None, similarity_score=None, matching_types=None):
    """
    Display anime dalam format card yang menarik dengan gambar
    Menampilkan matching types jika ada
    """
    col_img, col_info = st.columns([1, 3])
    
    # Kolom gambar
    with col_img:
        if image_url:
            try:
                st.image(image_url, width=120, use_container_width=False)
            except:
                st.markdown("🎬", unsafe_allow_html=True)
        else:
            st.markdown("🎬", unsafe_allow_html=True)
    
    # Kolom info
    with col_info:
        st.markdown(f"### 🎬 {title}")
        
        # Info baris 1: Score, Type, Episodes
        info_col1, info_col2, info_col3 = st.columns(3)
        with info_col1:
            st.markdown(f'<span class="rating-badge">⭐ {score}</span>', unsafe_allow_html=True)
        with info_col2:
            st.caption(f"Tipe: {anime_type}")
        with info_col3:
            st.caption(f"Episodes: {episodes if episodes else 'N/A'}")
        
        # Matching types display
        if matching_types and len(matching_types) > 0:
            matching_html = ''.join([f'<span class="genre-tag" style="background: rgba(76, 175, 80, 0.2); border-color: #4CAF50; color: #4CAF50;">✓ {t}</span>' for t in matching_types])
            st.markdown(f'<div class="similarity-score"><strong>Tipe Sama:</strong> {matching_html}</div>', 
                       unsafe_allow_html=True)
        
        # Similarity score jika ada
        if similarity_score is not None:
            similarity_percent = f"{(similarity_score * 100):.1f}%"
            st.markdown(f'<div class="similarity-score">📊 Kesamaan: {similarity_percent}</div>', 
                       unsafe_allow_html=True)
        
        # Display synopsis
        st.write(f"**Sinopsis:** {synopsis[:150]}...")

# ===================================
# MAIN APPLICATION
# ===================================

def main():
    """
    Fungsi utama aplikasi Streamlit
    """
    
    # Load dataset
    anime_data = load_anime_data()
    
    if not anime_data:
        st.error("❌ Tidak bisa load dataset. Pastikan anime.csv ada di folder yang benar.")
        return
    
    # Build TF-IDF features dan genre vectors
    documents, vocabulary, tf_vectors, genre_vectors, genre_list = build_tfidf_features(anime_data)
    
    # ===================================
    # HEADER
    # ===================================
    st.markdown("""
        <div class="header-anime">
            <h1>🎌 Sistem Rekomendasi Anime 🎌</h1>
            <p>Temukan anime favorit Anda dengan Content-Based Filtering (TF-IDF + Genre)</p>
        </div>
    """, unsafe_allow_html=True)
    
    # ===================================
    # SIDEBAR
    # ===================================
    with st.sidebar:
        st.markdown("### ⚙️ Menu Navigasi")
        page = st.radio(
            "Pilih Halaman:",
            ["🎯 Rekomendasi Anime", "⭐ Top Rating", "🔥 Populer", "🔍 Search & Filter", "📊 Statistics"]
        )
        
        st.markdown("---")
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    # ===================================
    # HALAMAN 1: REKOMENDASI ANIME
    # ===================================
    if page == "🎯 Rekomendasi Anime":
        st.markdown("### 🎯 Dapatkan Rekomendasi Anime")
        st.markdown("**Metode:** Content-Based Filtering dengan kombinasi TF-IDF (Synopsis) dan Type Matching")
        
        col1, col2 = st.columns([2, 1])
        
        anime_titles = [anime['title'] for anime in anime_data]
        
        with col1:
            selected_anime = st.selectbox(
                "Pilih anime favorit Anda:",
                anime_titles,
                help="Pilih anime untuk mendapatkan rekomendasi yang mirip berdasarkan konten dan tipe"
            )
        
        with col2:
            n_recommendations = st.number_input(
                "Jumlah rekomendasi:",
                min_value=1,
                max_value=20,
                value=5
            )
        
        if st.button("💡 Tampilkan Rekomendasi", key="rec_button", use_container_width=True):
            with st.spinner("⏳ Mencari rekomendasi anime terbaik..."):
                recommendations = get_anime_recommendations(
                    selected_anime, anime_data, tf_vectors, genre_vectors, genre_list, n_recommendations
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
    
    # ===================================
    # HALAMAN 2: TOP RATING
    # ===================================
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
    
    # ===================================
    # HALAMAN 3: POPULER
    # ===================================
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
    
    # ===================================
    # HALAMAN 4: SEARCH & FILTER
    # ===================================
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
            # Get unique anime types from dataset
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
    
    # ===================================
    # HALAMAN 5: STATISTICS
    # ===================================
    elif page == "📊 Statistics":
        st.markdown("### 📊 Statistik Database Anime")
        
        scores = [float(anime['score']) for anime in anime_data]
        
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
    
    # ===================================
    # FOOTER
    # ===================================
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #a0a0a0; margin-top: 2rem; padding: 1rem;">
            <p>🎌 <strong>Sistem Rekomendasi Anime</strong> 🎌</p>
            <p>Dibuat dengan ❤️ menggunakan Streamlit dan TF-IDF Cosine Similarity</p>
            <p style="font-size: 0.9rem;">© 2026 Anime Recommender System - Content-Based Filtering</p>
        </div>
    """, unsafe_allow_html=True)

# ===================================
# RUN APPLICATION
# ===================================
if __name__ == "__main__":
    main()
