# ===================================
# SISTEM REKOMENDASI ANIME - STREAMLIT APP
# Menggunakan sklearn TF-IDF + Content-Based Filtering
# ===================================

# Import library yang diperlukan
import streamlit as st
from data_loader import get_anime_data
import html
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

# Cek NLTK data tanpa memaksa download internet.
try:
    nltk.data.find('corpora/stopwords')
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
            page_title="Anime Recommender",
            page_icon=icon,
            layout="wide",
            initial_sidebar_state="expanded"
        )
    else:
        raise FileNotFoundError
except:
    st.set_page_config(
        page_title="Anime Recommender",
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

.poster-card {
    background: #ffffff;
    border: 1px solid rgba(160, 160, 160, 0.35);
    border-radius: 8px;
    overflow: hidden;
    min-height: 360px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.25);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}

.poster-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 28px rgba(255, 0, 110, 0.24);
    border-color: rgba(255, 0, 110, 0.55);
}

.poster-frame {
    position: relative;
    aspect-ratio: 2 / 3;
    background: rgba(255, 0, 110, 0.12);
}

.poster-frame img {
    width: 100%;
    height: 100%;
    display: block;
    object-fit: cover;
}

.poster-fallback {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ff006e;
    font-size: 2.6rem;
    background: linear-gradient(135deg, rgba(255, 0, 110, 0.14), rgba(33, 150, 243, 0.12));
}

.accuracy-badge {
    position: absolute;
    top: 8px;
    right: 8px;
    z-index: 2;
    background: linear-gradient(135deg, #ff006e 0%, #ff85c0 100%);
    color: #ffffff;
    padding: 0.35rem 0.55rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 800;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
}

.accuracy-badge span {
    display: block;
    font-size: 0.62rem;
    font-weight: 700;
    line-height: 1.1;
    opacity: 0.92;
}

.poster-meta {
    padding: 0.9rem 0.95rem 1rem;
    background: #ffffff;
}

.poster-title {
    min-height: 3.2rem;
    color: #333333;
    font-size: 1rem;
    font-weight: 650;
    line-height: 1.35;
    margin: 0;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}

.poster-submeta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    color: #777777;
    font-size: 0.95rem;
    margin-top: 0.45rem;
}

.poster-score {
    color: #ff006e;
    font-weight: 750;
}

.detail-shell {
    background: linear-gradient(135deg, rgba(26, 31, 58, 0.92), rgba(15, 20, 40, 0.98));
    border: 1px solid rgba(255, 0, 110, 0.28);
    border-radius: 1rem;
    padding: 1.35rem;
    box-shadow: 0 16px 44px rgba(0, 0, 0, 0.35);
}

.detail-title {
    color: #ffffff;
    font-size: 2rem;
    line-height: 1.18;
    font-weight: 800;
    margin: 0 0 0.35rem;
}

.detail-subtitle {
    color: #ff85c0;
    font-size: 1rem;
    line-height: 1.45;
    margin: 0 0 0.9rem;
}

.detail-link {
    display: inline-block;
    margin-top: 0.85rem;
    color: #ffffff !important;
    background: rgba(255, 0, 110, 0.22);
    border: 1px solid rgba(255, 0, 110, 0.45);
    border-radius: 0.6rem;
    padding: 0.55rem 0.8rem;
    text-decoration: none !important;
    font-weight: 700;
}

.detail-section-title {
    color: #ff85c0;
    font-size: 0.92rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    margin: 1.2rem 0 0.65rem;
    text-transform: uppercase;
}

.detail-poster {
    width: 100%;
    max-width: 260px;
    aspect-ratio: 2 / 3;
    margin: 0 auto;
    overflow: hidden;
    border-radius: 0.8rem;
    border: 1px solid rgba(255, 0, 110, 0.35);
    background: rgba(255, 0, 110, 0.12);
    box-shadow: 0 14px 34px rgba(0, 0, 0, 0.35);
}

.detail-poster img {
    width: 100%;
    height: 100%;
    display: block;
    object-fit: cover;
}

.detail-poster-fallback {
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, rgba(255, 0, 110, 0.16), rgba(33, 150, 243, 0.14));
}

.detail-meta-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.8rem;
    margin-top: 1rem;
}

.detail-meta-card {
    background: rgba(255, 255, 255, 0.055);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 0.75rem;
    padding: 0.9rem 1rem;
}

.detail-meta-label {
    color: #a0a0a0;
    font-size: 0.72rem;
    font-weight: 750;
    letter-spacing: 0.08em;
    margin: 0 0 0.35rem;
    text-transform: uppercase;
}

.detail-meta-value {
    color: #ffffff;
    font-size: 1.05rem;
    font-weight: 750;
    line-height: 1.35;
    margin: 0;
    overflow-wrap: anywhere;
}

.detail-rating {
    color: #FFC107;
}

.detail-chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin: 0.5rem 0 0.25rem;
}

.detail-chip {
    display: inline-block;
    color: #ffffff;
    background: rgba(255, 0, 110, 0.16);
    border: 1px solid rgba(255, 133, 192, 0.42);
    border-radius: 999px;
    padding: 0.35rem 0.65rem;
    font-size: 0.82rem;
    font-weight: 700;
    line-height: 1.2;
}

.detail-side-card {
    max-width: 260px;
    margin: 1rem auto 0;
    background: rgba(255, 255, 255, 0.055);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 0.85rem;
    padding: 1rem;
}

.detail-side-row {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    color: #e0e0e0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding: 0.55rem 0;
}

.detail-side-row:last-child {
    border-bottom: 0;
}

.detail-side-label {
    color: #a0a0a0;
    font-size: 0.8rem;
}

.detail-side-value {
    color: #ffffff;
    font-weight: 750;
    text-align: right;
}

.detail-synopsis {
    background: rgba(255, 0, 110, 0.08);
    border: 1px solid rgba(255, 0, 110, 0.18);
    border-left: 4px solid #ff006e;
    border-radius: 0.85rem;
    padding: 1.25rem 1.35rem;
    color: #e0e0e0;
    line-height: 1.75;
    margin-top: 1rem;
}

@media (max-width: 760px) {
    .detail-meta-grid {
        grid-template-columns: 1fr;
    }

    .detail-title {
        font-size: 1.5rem;
    }
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
        return "N/A"  # Jika data episode kosong, tampilkan N/A
    try:
        ep_float = float(episodes)  # Konversi nilai episode ke float
        ep_int = int(ep_float)  # Konversi ulang ke integer untuk pengecekan
        if ep_float == ep_int:
            return str(ep_int)  # Jika angka bulat, tampilkan tanpa .0
        return str(ep_float)  # Jika bukan bulat, tampilkan nilai float
    except:
        return str(episodes)  # Jika konversi gagal, gunakan string asli

def get_release_year(anime):
    """Ambil tahun dari start_date jika tersedia."""
    start_date = str(anime.get('start_date', '')).strip()  # Ambil field tanggal
    year_match = re.search(r'\b(19|20)\d{2}\b', start_date)  # Cari tahun 1900-2099
    if year_match:
        return year_match.group(0)  # Kembalikan tahun pertama yang cocok
    return ""  # Tidak ditemukan tahun

def format_number(value):
    """Format angka besar agar mudah dibaca."""
    try:
        number = float(value)  # Ubah input ke float untuk pengolahan
        if number.is_integer():
            return f"{int(number):,}".replace(",", ".")  # Format dengan titik ribuan
        return f"{number:,.1f}".replace(",", ".")  # Format desimal satu angka
    except:
        return str(value) if value not in (None, '') else "N/A"  # Kembalikan fallback

def format_rank_value(value):
    """Format rank/popularity dengan tanda # jika datanya tersedia."""
    formatted = format_number(value)  # Format angka rank/popularity
    return f"#{formatted}" if formatted != "N/A" else "N/A"  # Tambahkan prefix # jika valid

def clean_display_value(value, fallback="N/A"):
    """Bersihkan nilai kosong/NaN dari CSV untuk tampilan."""
    if value is None:
        return fallback  # Nilai None dianggap kosong
    text = str(value).strip()  # Ubah ke string dan hilangkan spasi
    if not text or text.lower() in {"nan", "none", "null"}:
        return fallback  # Angka NaN/None/null dianggap kosong
    return text  # Kembalikan nilai bersih

def safe_display(value, fallback="N/A"):
    """Escape nilai sebelum masuk HTML."""
    return html.escape(clean_display_value(value, fallback))  # Escape HTML untuk keamanan

def build_detail_card(label, value, extra_class=""):
    """Render satu kartu metadata detail."""
    value_class = f"detail-meta-value {extra_class}".strip()  # Gabungkan class tambahan bila ada
    return f"""
    <div class="detail-meta-card">
        <p class="detail-meta-label">{html.escape(label)}</p>
        <p class="{value_class}">{value}</p>
    </div>
    """  # Kembalikan HTML kartu metadata sebagai string

def build_chip_row(label, value):
    """Render list CSV sebagai chip yang rapi."""
    items = split_list_field(value)  # Pecah daftar CSV menjadi array bersih
    if not items:
        return build_detail_card(label, "N/A")  # Jika kosong, tampilkan N/A

    chips = ''.join(f'<span class="detail-chip">{html.escape(item)}</span>' for item in items)
    return f"""
    <div class="detail-meta-card">
        <p class="detail-meta-label">{html.escape(label)}</p>
        <div class="detail-chip-row">{chips}</div>
    </div>
    """  # Buat baris chip HTML dari setiap item

def get_accuracy_level(similarity_score):
    """Ubah skor similarity menjadi tingkat akurasi yang mudah dipahami."""
    percent = (similarity_score or 0) * 100  # Konversi skor menjadi persentase
    if percent >= 45:
        return "Sangat Cocok"  # Skor sangat tinggi
    if percent >= 30:
        return "Cocok"  # Skor cukup tinggi
    if percent >= 18:
        return "Cukup Cocok"  # Skor moderat
    return "Rendah"  # Skor rendah

def split_list_field(value):
    """Pisahkan field CSV seperti genres/themes menjadi list bersih."""
    if not value:
        return []  # Tidak ada item bila input kosong
    return [item.strip() for item in str(value).split(',') if item.strip()]  # Pisah dan bersihkan tiap item

def get_anime_feature_tags(anime):
    """Gabungkan detail MAL penting untuk similarity berbasis metadata."""
    tags = []  # Fitur metadata yang akan memengaruhi skor rekomendasi
    for field in ['genres', 'themes', 'demographics', 'studios']:
        tags.extend([f"{field}:{item}" for item in split_list_field(anime.get(field, ''))])
        # Setiap genre/theme/studio/demographic menjadi token unik

    anime_type = str(anime.get('type', '')).strip()  # Ambil tipe anime
    if anime_type:
        tags.append(f"type:{anime_type}")  # Tambahkan tipe anime sebagai fitur

    source = str(anime.get('source', '')).strip()  # Ambil source anime
    if source:
        tags.append(f"source:{source}")  # Sumber membantu menentukan kecocokan

    rating = str(anime.get('rating', '')).strip()  # Ambil rating konten
    if rating:
        tags.append(f"rating:{rating}")  # Rating konten membantu memfilter

    year = get_release_year(anime)  # Ambil tahun rilis
    if year:
        tags.append(f"year:{year}")  # Tahun rilis sebagai fitur temporal

    return sorted(set(tags))

def build_similarity_document(anime):
    """Gabungkan sinopsis dan detail dataset baru untuk TF-IDF."""
    fields = [
        anime.get('synopsis', ''),
        anime.get('title', ''),
        anime.get('english_name', ''),
        anime.get('genres', ''),
        anime.get('genres', ''),
        anime.get('themes', ''),
        anime.get('themes', ''),
        anime.get('demographics', ''),
        anime.get('type', ''),
        anime.get('studios', ''),
        anime.get('producers', ''),
        anime.get('source', ''),
        anime.get('rating', ''),
        anime.get('duration', ''),
        anime.get('start_date', ''),
    ]
    return ' '.join(str(field) for field in fields if field)


@st.cache_resource
def get_stopwords():
    """Ambil stopwords bahasa Inggris"""
    try:
        return set(stopwords.words('english'))  # Ambil stopwords NLTK
    except LookupError:
        return {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'were', 'will', 'with', 'their', 'they', 'this'
        }  # Gunakan daftar fallback jika data NLTK tidak ada

# ===================================
# FUNGSI PREPROCESSING TEXT
# ===================================

def preprocess_text(text):
    """
    Preprocessing simplified - tanpa lemmatization (JAUH LEBIH CEPAT)
    """
    if not text:
        return ""  # Teks kosong tidak perlu diproses
    
    text = text.lower()  # Normalisasi semua karakter ke huruf kecil
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)  # Hapus URL
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Hapus karakter non-alfabet
    text = ' '.join(text.split())  # Hapus whitespace ganda
    
    stop_words = get_stopwords()  # Ambil daftar stopwords
    words = text.split()  # Pisah kata-kata menjadi list
    processed_words = [word for word in words if word not in stop_words and len(word) > 2]
    # Hanya sisakan kata penting untuk TF-IDF
    
    return ' '.join(processed_words)  # Gabungkan kembali menjadi string

# ===================================
# FUNGSI GENRE FEATURE EXTRACTION
# ===================================

def extract_genres(anime_data):
    """Extract unique feature tags dan create binary vectors."""
    all_tags = set()  # Kumpulan semua fitur metadata
    for anime in anime_data:
        all_tags.update(get_anime_feature_tags(anime))  # Tambahkan fitur dari setiap anime
    
    genre_list = sorted(list(all_tags))  # Urutkan daftar fitur agar konsisten
    
    genre_vectors = []  # Simpan vektor biner untuk setiap anime
    for anime in anime_data:
        anime_tags = set(get_anime_feature_tags(anime))  # Fitur metadata anime saat ini
        vector = []
        for genre in genre_list:
            vector.append(1.0 if genre in anime_tags else 0.0)
            # 1 jika fitur ada, 0 jika tidak
        genre_vectors.append(vector)
    
    return genre_list, genre_vectors  # Kembalikan daftar fitur dan vektornya

# ===================================
# FUNGSI TF-IDF DENGAN SKLEARN
# ===================================

@st.cache_resource
def build_tfidf_features(anime_data_tuple):
    """
    Build TF-IDF matrix dengan sklearn (JAUH LEBIH CEPAT)
    @st.cache_resource = hanya jalan SEKALI, tidak rebuild saat rerun
    """
    anime_data = list(anime_data_tuple)  # Convert tuple ke list agar dapat diiterasi
    
    # Preprocess documents
    documents = []  # List dokumen teks yang diproses
    for anime in anime_data:
        processed = preprocess_text(build_similarity_document(anime))  # Buat dokument teks dari field anime
        documents.append(processed)  # Tambahkan ke daftar dokumen
        # Dokumen teks sudah dibersihkan dan siap dimasukkan ke TF-IDF
    
    # Build TF-IDF dengan sklearn
    tfidf = TfidfVectorizer(
        max_features=5000,  # PENTING: Batasi vocabulary untuk reduksi noise
        stop_words='english'  # Hapus stopwords internal sklearn
    )
    tfidf_matrix = tfidf.fit_transform(documents)  # Fit TF-IDF pada semua dokumen
    # tfidf_matrix berisi representasi numerik teks yang menentukan similarity
    
    # Extract genre vectors
    genre_list, genre_vectors = extract_genres(anime_data)  # Buat vektor metadata genre
    # Genre vectors dipakai sebagai fitur metadata tambahan
    
    return tfidf_matrix, genre_vectors, genre_list, tfidf  # Kembalikan model dan fitur

def hybrid_similarity(tfidf_sim, genre_sim, tfidf_weight=0.55, genre_weight=0.45):
    """Kombinasi TF-IDF dan similarity detail metadata."""
    return (tfidf_sim * tfidf_weight) + (genre_sim * genre_weight)  # Hitung skor gabungan
    # Perbandingan bobot menentukan seberapa besar pengaruh teks vs metadata

def cosine_sim_vectors(vec1, vec2):
    """Calculate cosine similarity antara dua vectors"""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))  # Hitung dot product
    magnitude1 = math.sqrt(sum(a ** 2 for a in vec1))  # Norm pertama
    magnitude2 = math.sqrt(sum(b ** 2 for b in vec2))  # Norm kedua
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0  # Vektor nol tidak bisa dibandingkan
    
    return dot_product / (magnitude1 * magnitude2)  # Return cosine similarity
    # Ini menghitung seberapa besar sudut vektor; semakin kecil sudut, semakin mirip

def get_matching_genres(anime1_genres, anime2_genres, genre_list):
    """Dapatkan tipe yang cocok"""
    matching_genres = []  # Daftar fitur metadata yang sama
    for i, genre in enumerate(genre_list):
        if anime1_genres[i] == 1.0 and anime2_genres[i] == 1.0:
            matching_genres.append(genre)  # Tambahkan genre yang cocok
    # Matching genres menjadi penjelasan tambahan untuk output rekomendasi
    return matching_genres

# ===================================
# FUNGSI REKOMENDASI
# ===================================

def get_anime_recommendations(anime_title, anime_data, tfidf_matrix, genre_vectors, genre_list, n_recommendations=5):
    """
    Dapatkan rekomendasi dengan sklearn cosine similarity
    OPTIMASI: Hanya hitung similarity untuk anime yang dicari, tidak semua
    """
    anime_index = None  # Indeks anime yang dipilih
    for i, anime in enumerate(anime_data):
        if str(anime.get('title', '')).lower() == str(anime_title).lower():
            anime_index = i  # Temukan anime dari judul yang dipilih
            break
    
    if anime_index is None:
        return None  # Jika judul tidak ditemukan, tidak ada output rekomendasi
    
    # Hitung similarity dengan sklearn untuk dokumen TF-IDF
    similarities_tfidf = cosine_similarity(tfidf_matrix[anime_index], tfidf_matrix)[0]
    # Simpan similarity TF-IDF terhadap semua anime lain
    
    selected_genre_vector = genre_vectors[anime_index]  # Vektor metadata anime terpilih
    # Ambil vektor metadata dari anime yang dipilih
    
    similarities = []  # Simpan skor similarity kombinasi
    
    for i, anime in enumerate(anime_data):
        if i != anime_index:
            tfidf_sim = similarities_tfidf[i]  # Skor similarity teks/narasi
            # Similarity teks/narasi dari TF-IDF
            
            genre_sim = cosine_sim_vectors(selected_genre_vector, genre_vectors[i])
            # Similarity metadata genre/type/source
            
            hybrid_sim = hybrid_similarity(tfidf_sim, genre_sim)
            # Gabungkan skor TF-IDF dan metadata menjadi skor akhir
            
            matching_types = get_matching_genres(selected_genre_vector, genre_vectors[i], genre_list)
            # Jenis metadata yang cocok untuk menjelaskan output
            
            similarities.append((i, hybrid_sim, anime, matching_types))  # Tambahkan data rekomendasi
    
    similarities.sort(key=lambda x: x[1], reverse=True)  # Urutkan rekomendasi berdasarkan skor hybrid terbesar
    
    recommendations = []  # Siapkan list hasil
    for idx, sim, anime, matching_types in similarities[:n_recommendations]:
        recommendations.append({
            'anime_id': anime.get('anime_id', ''),
            'anime_url': anime.get('anime_url', ''),
            'title': anime.get('title', 'Tanpa Judul'),
            'english_name': anime.get('english_name', ''),
            'japanese_names': anime.get('japanese_names', ''),
            'score': anime.get('score', 'N/A'),
            'type': anime.get('type', 'N/A'),
            'episodes': anime.get('episodes', ''),
            'synopsis': anime.get('synopsis', ''),
            'start_date': anime.get('start_date', ''),
            'genres': anime.get('genres', ''),
            'themes': anime.get('themes', ''),
            'demographics': anime.get('demographics', ''),
            'studios': anime.get('studios', ''),
            'producers': anime.get('producers', ''),
            'source': anime.get('source', ''),
            'duration': anime.get('duration', ''),
            'rating': anime.get('rating', ''),
            'rank': anime.get('rank', ''),
            'popularity': anime.get('popularity', ''),
            'members': anime.get('members', ''),
            'favorites': anime.get('favorites', ''),
            'scored_by': anime.get('scored_by', ''),
            'similarity_score': sim,
            'matching_types': matching_types,
            'image_url': anime.get('image_url', '')
        })
    
    return recommendations  # Output akhir berisi daftar rekomendasi berdasar skor model

# ===================================
# FUNGSI FILTER & SEARCH
# ===================================

def get_top_rated_anime(anime_data, n=10):
    """Dapatkan anime dengan score tertinggi"""
    sorted_anime = sorted(anime_data, key=lambda x: float(x.get('score', 0) or 0), reverse=True)
    return sorted_anime[:min(n, 50)]

def filter_anime_by_type(anime_data, anime_type):
    """Filter berdasarkan tipe"""
    filtered = [
        anime for anime in anime_data 
        if anime_type.lower() in str(anime.get('type', '')).lower()
        or anime_type.lower() in str(anime.get('genres', '')).lower()
    ]
    filtered.sort(key=lambda x: float(x.get('score', 0) or 0), reverse=True)
    return filtered[:50]

def search_anime(anime_data, search_term):
    """Search berdasarkan judul atau synopsis"""
    search_lower = search_term.lower()
    results = [
        anime for anime in anime_data
        if search_lower in str(anime.get('title', '')).lower()
        or search_lower in str(anime.get('synopsis', '')).lower()
        or search_lower in str(anime.get('genres', '')).lower()
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

def display_anime_card(title, score, anime_type, episodes, synopsis, image_url=None, similarity_score=None, matching_types=None, clickable=False, detail_key=None):
    """Display anime card dengan layout yang diperbaiki"""
    col_img, col_info = st.columns([0.8, 2.2], gap="medium")
    
    with col_img:
        if image_url:
            try:
                st.image(image_url, width=150, use_container_width=True, caption="")
            except:
                st.markdown(
                    '<div style="width: 150px; height: 220px; background: rgba(255, 0, 110, 0.2); display: flex; align-items: center; justify-content: center; border-radius: 0.8rem; border: 2px solid rgba(255, 0, 110, 0.3); font-size: 3rem;"></div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                '<div style="width: 150px; height: 220px; background: rgba(255, 0, 110, 0.2); display: flex; align-items: center; justify-content: center; border-radius: 0.8rem; border: 2px solid rgba(255, 0, 110, 0.3); font-size: 3rem;"></div>',
                unsafe_allow_html=True
            )
    
    with col_info:
        if clickable:
            st.markdown(f'<h3 style="color: #ff006e; margin: 0 0 1rem 0; cursor: pointer;">{title}</h3>', unsafe_allow_html=True)
            st.button(f"Lihat Detail", key=f"detail_{title}_{hash(str(detail_key or title)) % 10000}", use_container_width=False, on_click=set_detail_anime, args=(detail_key or title,))
        else:
            st.markdown(f'<h3 style="color: #ff006e; margin: 0 0 1rem 0;">{title}</h3>', unsafe_allow_html=True)
        
        # Info badges dalam satu baris
        badge_col1, badge_col2, badge_col3 = st.columns(3, gap="small")
        with badge_col1:
            st.markdown(f'<div style="text-align: center; background: rgba(255, 193, 7, 0.15); padding: 0.8rem; border-radius: 0.6rem; border: 1px solid rgba(255, 193, 7, 0.4);"><span style="color: #a0a0a0; font-size: 0.8rem;">RATING</span><br><span style="color: #FFC107; font-weight: bold; font-size: 1.3rem;">★ {score}</span></div>', unsafe_allow_html=True)
        
        with badge_col2:
            st.markdown(f'<div style="text-align: center; background: rgba(33, 150, 243, 0.15); padding: 0.8rem; border-radius: 0.6rem; border: 1px solid rgba(33, 150, 243, 0.4);"><span style="color: #a0a0a0; font-size: 0.8rem;">TIPE</span><br><span style="color: #2196F3; font-weight: bold; font-size: 1.3rem;">{anime_type}</span></div>', unsafe_allow_html=True)
        
        with badge_col3:
            st.markdown(f'<div style="text-align: center; background: rgba(76, 175, 80, 0.15); padding: 0.8rem; border-radius: 0.6rem; border: 1px solid rgba(76, 175, 80, 0.4);"><span style="color: #a0a0a0; font-size: 0.8rem;">EPISODE</span><br><span style="color: #4CAF50; font-weight: bold; font-size: 1.3rem;">{format_episodes(episodes)}</span></div>', unsafe_allow_html=True)
        
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

def display_recommendation_grid(recommendations, cards_per_row=5):
    """Tampilkan rekomendasi sebagai grid poster ringkas."""
    if not recommendations:
        return

    cards_per_row = max(1, min(cards_per_row, 5))

    for row_start in range(0, len(recommendations), cards_per_row):
        row_items = recommendations[row_start:row_start + cards_per_row]
        cols = st.columns(cards_per_row, gap="small")

        for offset, rec in enumerate(row_items):
            idx = row_start + offset + 1
            with cols[offset]:
                title = html.escape(str(rec.get('title', 'Tanpa Judul')))
                image_url = html.escape(str(rec.get('image_url', '')).strip())
                detail_key = rec.get('anime_id') or rec.get('title', '')
                year = get_release_year(rec)
                score = rec.get('score', 'N/A')
                similarity = rec.get('similarity_score', 0) or 0
                accuracy = f"{similarity * 100:.0f}%"
                accuracy_level = html.escape(get_accuracy_level(similarity))

                if image_url:
                    poster_html = f'<img src="{image_url}" alt="{title} poster">'
                else:
                    poster_html = '<div class="poster-fallback"></div>'

                st.markdown(
                    f"""
                    <div class="poster-card">
                        <div class="poster-frame">
                            <div class="accuracy-badge">{accuracy}<span>{accuracy_level}</span></div>
                            {poster_html}
                        </div>
                        <div class="poster-meta">
                            <p class="poster-title">{title}</p>
                            <div class="poster-submeta">
                                <span>{html.escape(year) if year else 'Tahun N/A'}</span>
                                <span class="poster-score">★ {score}</span>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.button(
                    "Lihat Detail",
                    key=f"poster_detail_{idx}_{hash(str(detail_key)) % 100000}",
                    use_container_width=True,
                    on_click=set_detail_anime,
                    args=(detail_key,)
                )

# ===================================
# FUNGSI DISPLAY DETAIL ANIME (HALAMAN BARU) - DIPERBAIKI TOTAL
# ===================================

def display_anime_detail_page(anime_data, anime_title):
    """Tampilkan halaman detail lengkap anime dengan layout yang diperbaiki"""
    anime_key = str(anime_title)
    selected_anime = next(
        (
            a for a in anime_data
            if str(a.get('anime_id', '')) == anime_key or str(a.get('title', '')) == anime_key
        ),
        None
    )
    
    if not selected_anime:
        st.error("❌ Anime tidak ditemukan!")
        return
    
    title = safe_display(selected_anime.get('title', 'Tanpa Judul'), 'Tanpa Judul')
    english_name = safe_display(selected_anime.get('english_name', ''), '')
    japanese_names = safe_display(selected_anime.get('japanese_names', ''), '')
    anime_type = safe_display(selected_anime.get('type', ''))
    episodes = html.escape(format_episodes(selected_anime.get('episodes', '')))
    score = safe_display(selected_anime.get('score', ''))
    synopsis = safe_display(selected_anime.get('synopsis', 'Sinopsis belum tersedia.'), 'Sinopsis belum tersedia.')
    image_url = html.escape(str(selected_anime.get('image_url', '')).strip())
    anime_url = html.escape(str(selected_anime.get('anime_url', '')).strip())
    anime_id = safe_display(selected_anime.get('anime_id', ''))
    premiered = safe_display(selected_anime.get('start_date', ''))
    producers = safe_display(selected_anime.get('producers', ''))
    studios = safe_display(selected_anime.get('studios', ''))
    source = safe_display(selected_anime.get('source', ''))
    duration = safe_display(selected_anime.get('duration', ''))
    age_rating = safe_display(selected_anime.get('rating', ''))
    rank = html.escape(format_rank_value(selected_anime.get('rank', '')))
    popularity = html.escape(format_rank_value(selected_anime.get('popularity', '')))
    members = html.escape(format_number(selected_anime.get('members', '')))
    favorites = html.escape(format_number(selected_anime.get('favorites', '')))
    scored_by = html.escape(format_number(selected_anime.get('scored_by', '')))
    subtitle_parts = [part for part in [english_name, japanese_names] if part]
    subtitle_html = " / ".join(subtitle_parts)
    mal_link = f'<a class="detail-link" href="{anime_url}" target="_blank" rel="noopener noreferrer">Buka di MyAnimeList</a>' if anime_url else ''

    overview_cards = ''.join([
        build_detail_card("Rating", f"★ {score}", "detail-rating"),
        build_detail_card("Tipe", anime_type),
        build_detail_card("Episode", episodes),
        build_detail_card("Premiered", premiered),
        build_detail_card("Durasi", duration),
        build_detail_card("Age Rating", age_rating),
    ])

    classification_cards = ''.join([
        build_chip_row("Genre", selected_anime.get('genres', '')),
        build_chip_row("Themes", selected_anime.get('themes', '')),
        build_chip_row("Demographic", selected_anime.get('demographics', '')),
        build_detail_card("Source", source),
    ])

    production_cards = ''.join([
        build_detail_card("Studio", studios),
        build_detail_card("Producers", producers),
    ])

    popularity_cards = ''.join([
        build_detail_card("Anime ID", anime_id),
        build_detail_card("Rank", rank),
        build_detail_card("Popularity", popularity),
        build_detail_card("Members", members),
        build_detail_card("Favorites", favorites),
        build_detail_card("Scored By", scored_by),
    ])

    st.button("⬅️ Kembali", use_container_width=False, on_click=go_back_to_recommendations)
    st.markdown("---")

    col_img, col_info = st.columns([0.9, 2.1], gap="large")

    with col_img:
        poster_html = f'<img src="{image_url}" alt="{title} poster">' if image_url else '<div class="detail-poster-fallback"></div>'
        st.markdown(
            f"""
            <div class="detail-poster">
                {poster_html}
            </div>
            <div class="detail-side-card">
                <div class="detail-side-row"><span class="detail-side-label">Score</span><span class="detail-side-value">★ {score}</span></div>
                <div class="detail-side-row"><span class="detail-side-label">Rank</span><span class="detail-side-value">{rank}</span></div>
                <div class="detail-side-row"><span class="detail-side-label">Popularity</span><span class="detail-side-value">{popularity}</span></div>
                <div class="detail-side-row"><span class="detail-side-label">Members</span><span class="detail-side-value">{members}</span></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_info:
        st.markdown(
            f"""
            <div class="detail-shell">
                <h2 class="detail-title">{title}</h2>
                <p class="detail-subtitle">{subtitle_html}</p>
                {mal_link}
                <p class="detail-section-title">Overview</p>
                <div class="detail-meta-grid">{overview_cards}</div>
                <p class="detail-section-title">Classification</p>
                <div class="detail-meta-grid">{classification_cards}</div>
                <p class="detail-section-title">Production</p>
                <div class="detail-meta-grid">{production_cards}</div>
                <p class="detail-section-title">Popularity</p>
                <div class="detail-meta-grid">{popularity_cards}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### Sinopsis Lengkap")
    st.markdown(
        f"""
        <div class="detail-synopsis">
            {synopsis}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ============ PASTIKAN SCROLL KE ATAS ============
    st.components.v1.html(
        """
        <script>
            (function() {
                // Hapus hash dari URL jika ada
                if (window.location.hash) {
                    history.replaceState(null, null, window.location.pathname + window.location.search);
                }
                // Scroll ke atas
                window.scrollTo(0, 0);
            })();
        </script>
        """,
        height=0,
    )

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
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []
    if 'recommendation_source' not in st.session_state:
        st.session_state.recommendation_source = None
    
    # Load data dari CSV (bukan database)
    anime_data = get_anime_data()
    filtered_anime_data = [anime for anime in anime_data if 'hentai' not in str(anime.get('genres', '')).lower()]
    if not anime_data:
        st.error("❌ Tidak bisa load dataset! Pastikan anime.csv ada di folder project.")
        return
    
    # Header
    st.markdown("""
        <div class="header-anime">
            <h1>🎌 Sistem Rekomendasi Anime 🎌</h1>
            <p>Temukan anime favorit Anda dengan metode Content-Based Filtering</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Jika user klik untuk melihat detail, tampilkan halaman detail
    if st.session_state.show_detail and st.session_state.detail_anime:
        display_anime_detail_page(anime_data, st.session_state.detail_anime)
        return
    
    # Build TF-IDF (CACHED - hanya jalan sekali!)
    with st.spinner("⏳ Memproses dataset anime..."):
        anime_data_tuple = tuple(filtered_anime_data)
        tfidf_matrix, genre_vectors, genre_list, tfidf_model = build_tfidf_features(anime_data_tuple)
    
    # MAIN PAGE: REKOMENDASI ANIME SESUAI DOKUMENTASI DESAIN
    if True:
        st.markdown("### Dapatkan Rekomendasi Anime")
        st.markdown("**Metode:** Content-Based Filtering dengan TF-IDF + Cosine Similarity")
        
        col1, col2 = st.columns([2, 1], gap="medium")
        anime_titles = [anime.get('title', 'Tanpa Judul') for anime in filtered_anime_data]
        
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
                    selected_anime, filtered_anime_data, tfidf_matrix, genre_vectors, genre_list, n_recommendations
                )
                st.session_state.recommendations = recommendations or []
                st.session_state.recommendation_source = selected_anime

        if st.session_state.recommendations:
            st.success("✅ Rekomendasi ditemukan!")

            st.markdown("---")

            # Anime yang dipilih
            st.markdown("#### Anime yang Anda Pilih")
            selected_anime_data = next((a for a in filtered_anime_data if a.get('title') == st.session_state.recommendation_source), None)

            if selected_anime_data:
                display_anime_card(
                    selected_anime_data.get('title', 'Tanpa Judul'),
                    selected_anime_data.get('score', 'N/A'),
                    selected_anime_data.get('type', 'N/A'),
                    selected_anime_data.get('episodes', ''),
                    selected_anime_data.get('synopsis', ''),
                    selected_anime_data.get('image_url', ''),
                    clickable=True,
                    detail_key=selected_anime_data.get('anime_id') or selected_anime_data.get('title', '')
                )

            st.markdown("---")
            st.markdown("#### Rekomendasi Untuk Anda")
            st.caption("Klik tombol Lihat Detail pada poster anime untuk membuka informasi lengkap.")
            display_recommendation_grid(st.session_state.recommendations)
        elif st.session_state.recommendation_source:
            st.warning("Rekomendasi belum ditemukan untuk anime tersebut.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #a0a0a0; margin-top: 3rem; padding: 2rem 1rem; border-top: 1px solid rgba(255, 0, 110, 0.15);">
            <p style="font-size: 1.2rem; font-weight: bold; color: #ff006e; margin-bottom: 0.5rem;">🎌 Sistem Rekomendasi Anime 🎌</p>
            <p style="margin: 0.3rem 0; color: #e0e0e0;">Temukan anime favorit dengan teknologi Content-Based Filtering</p>
            <p style="margin: 0.5rem 0; font-size: 0.95rem;">Dibuat dengan ❤️ menggunakan <strong style="color: #ff85c0;">Streamlit</strong></p>
            <p style="font-size: 0.85rem; margin-top: 1rem;">© 2026 - Content-Based Filtering</p>
        </div>
    """, unsafe_allow_html=True)

# Run
if __name__ == "__main__":
    main()
