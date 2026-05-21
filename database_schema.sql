-- ===============================================
-- SISTEM REKOMENDASI ANIME - DATABASE SCHEMA
-- Dioptimalkan untuk Streamlit App dengan TF-IDF
-- ===============================================

-- 1. Tabel Master Tipe Anime
-- Menyimpan kategori format anime
CREATE TABLE IF NOT EXISTS types (
    type_id INT PRIMARY KEY AUTO_INCREMENT,
    type_name VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabel Utama Anime
-- Menyimpan semua data anime dengan relasi ke tabel types
CREATE TABLE IF NOT EXISTS animes (
    anime_id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    score DECIMAL(4,2) DEFAULT 0.0,
    rank INT,
    popularity INT,
    members INT DEFAULT 0,
    type_id INT,
    episodes INT DEFAULT 0,
    synopsis LONGTEXT,
    start_date DATE,
    end_date DATE,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Index untuk pencarian cepat
    INDEX idx_title (title),
    INDEX idx_score (score DESC),
    INDEX idx_type_id (type_id),
    INDEX idx_rank (rank),
    INDEX idx_popularity (popularity),
    
    -- Full-text index untuk pencarian synopsis dan title
    FULLTEXT INDEX idx_search (title, synopsis),
    
    -- Foreign Key constraint ke tabel types
    CONSTRAINT fk_anime_type FOREIGN KEY (type_id) 
        REFERENCES types(type_id) ON DELETE SET NULL
);

-- 3. Tabel User Activity (Opsional untuk pengembangan)
-- Menyimpan histori pencarian dan interaksi user
CREATE TABLE IF NOT EXISTS user_activity (
    activity_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(100) NOT NULL,
    anime_id INT,
    activity_type ENUM('search', 'view', 'recommendation', 'rating') NOT NULL,
    search_query VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Index untuk query histori
    INDEX idx_user_id (user_id),
    INDEX idx_anime_id (anime_id),
    INDEX idx_timestamp (timestamp DESC),
    
    CONSTRAINT fk_activity_anime FOREIGN KEY (anime_id) 
        REFERENCES animes(anime_id) ON DELETE CASCADE
);

-- ===============================================
-- INSERSI DATA TIPE ANIME DASAR
-- ===============================================
INSERT IGNORE INTO types (type_name) VALUES 
('TV'),
('Movie'),
('OVA'),
('Special'),
('ONA'),
('Music');

-- ===============================================
-- TRIGGER untuk Update Timestamp
-- ===============================================
DELIMITER $$

CREATE TRIGGER update_anime_timestamp 
BEFORE UPDATE ON animes
FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END$$

DELIMITER ;

-- ===============================================
-- VIEW untuk Statistik Anime
-- ===============================================
CREATE OR REPLACE VIEW anime_statistics AS
SELECT 
    t.type_name,
    COUNT(a.anime_id) as total_anime,
    ROUND(AVG(a.score), 2) as avg_score,
    MAX(a.score) as highest_score,
    MIN(a.score) as lowest_score,
    ROUND(AVG(a.episodes), 0) as avg_episodes
FROM animes a
LEFT JOIN types t ON a.type_id = t.type_id
GROUP BY t.type_id, t.type_name;

-- ===============================================
-- NOTES UNTUK OPTIMASI
-- ===============================================
-- 1. Indeks pada 'title' dan 'score' digunakan untuk:
--    - search_anime(): WHERE title LIKE '%keyword%'
--    - get_top_rated_anime(): ORDER BY score DESC
-- 
-- 2. FULLTEXT INDEX pada 'title' dan 'synopsis':
--    - Digunakan untuk pencarian dengan MATCH AGAINST
--    - Lebih cepat dari LIKE untuk text panjang
-- 
-- 3. Foreign Key pada type_id:
--    - Menjaga integritas referensial
--    - Memastikan setiap anime memiliki tipe yang valid
-- 
-- 4. User Activity table:
--    - Opsional, untuk tracking user behavior
--    - Dapat digunakan untuk personalisasi rekomendasi di masa depan
--
-- 5. Timestamp columns:
--    - Berguna untuk audit trail dan analytics
-- ===============================================
