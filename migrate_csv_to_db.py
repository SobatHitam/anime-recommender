# ===================================
# SCRIPT MIGRASI DATA CSV KE DATABASE SQL
# Dari anime.csv ke MySQL Database
# ===================================

import csv
import mysql.connector
from mysql.connector import Error
import sys
from pathlib import Path

# ===================================
# KONFIGURASI DATABASE
# ===================================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Sesuaikan dengan password MySQL Anda
    'database': 'anime_recommender',
    'charset': 'utf8mb4',
    'use_unicode': True
}

class AnimeDataMigration:
    """Class untuk migrasi data anime dari CSV ke MySQL Database"""
    
    def __init__(self, db_config):
        """
        Initialize koneksi database
        
        Args:
            db_config (dict): Konfigurasi koneksi MySQL
        """
        self.db_config = db_config
        self.connection = None
        self.cursor = None
        self.stats = {
            'total_rows': 0,
            'inserted_animes': 0,
            'failed_rows': 0,
            'errors': []
        }
    
    def connect(self):
        """Membuat koneksi ke database"""
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            self.cursor = self.connection.cursor(dictionary=True)
            print("✓ Koneksi ke database berhasil!")
            return True
        except Error as e:
            print(f"✗ Error koneksi database: {e}")
            return False
    
    def disconnect(self):
        """Menutup koneksi database"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("✓ Koneksi database ditutup!")
    
    def create_database(self, sql_file='database_schema.sql'):
        """
        Membuat database dan tabel dari file SQL
        
        Args:
            sql_file (str): Path ke file SQL schema
        """
        try:
            print(f"\n📋 Membaca file schema: {sql_file}")
            
            # Baca file SQL
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # Split berdasarkan delimiter
            statements = sql_content.split(';')
            
            # Execute setiap statement
            executed = 0
            for statement in statements:
                statement = statement.strip()
                if statement:
                    try:
                        self.cursor.execute(statement)
                        self.connection.commit()
                        executed += 1
                    except Error as e:
                        # Ignore error jika tabel sudah ada
                        if 'already exists' not in str(e):
                            print(f"Warning: {e}")
            
            print(f"✓ Database schema berhasil dibuat/diperbarui! ({executed} statements)")
            return True
            
        except FileNotFoundError:
            print(f"✗ File {sql_file} tidak ditemukan!")
            return False
        except Error as e:
            print(f"✗ Error membuat database schema: {e}")
            return False
    
    def get_or_create_type(self, type_name):
        """
        Mendapatkan type_id, jika tidak ada dibuat yang baru
        
        Args:
            type_name (str): Nama tipe anime (TV, Movie, OVA, dll)
            
        Returns:
            int: type_id
        """
        try:
            # Cek apakah type sudah ada
            query = "SELECT type_id FROM types WHERE type_name = %s"
            self.cursor.execute(query, (type_name,))
            result = self.cursor.fetchone()
            
            if result:
                return result['type_id']
            
            # Jika tidak ada, buat yang baru
            insert_query = "INSERT INTO types (type_name) VALUES (%s)"
            self.cursor.execute(insert_query, (type_name,))
            self.connection.commit()
            
            return self.cursor.lastrowid
            
        except Error as e:
            print(f"Warning - Error getting/creating type '{type_name}': {e}")
            return None
    
    def insert_anime(self, anime_data):
        """
        Insert satu data anime ke database
        
        Args:
            anime_data (dict): Dictionary berisi data anime dari CSV
            
        Returns:
            bool: True jika berhasil, False jika gagal
        """
        try:
            # Ambil type_id berdasarkan type_name
            type_id = self.get_or_create_type(anime_data['type'])
            
            # Query insert
            insert_query = """
            INSERT INTO animes 
            (anime_id, title, score, rank, popularity, members, 
             type_id, episodes, synopsis, start_date, end_date, image_url)
            VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Prepare data
            values = (
                int(anime_data['anime_id']),
                anime_data['title'][:255],  # Limit varchar(255)
                float(anime_data['score']) if anime_data['score'] else 0.0,
                int(anime_data['rank']) if anime_data['rank'] else None,
                int(anime_data['popularity']) if anime_data['popularity'] else None,
                int(anime_data['members']) if anime_data['members'] else 0,
                type_id,
                int(anime_data['episodes']) if anime_data['episodes'] else 0,
                anime_data['synopsis'],
                anime_data['start_date'] if anime_data['start_date'] else None,
                anime_data['end_date'] if anime_data['end_date'] else None,
                anime_data['image_url']
            )
            
            self.cursor.execute(insert_query, values)
            self.connection.commit()
            
            return True
            
        except Error as e:
            self.connection.rollback()
            self.stats['errors'].append(f"Row {self.stats['total_rows']}: {str(e)}")
            return False
    
    def migrate_from_csv(self, csv_file='anime.csv', batch_size=10):
        """
        Migrasi data anime dari file CSV ke database
        
        Args:
            csv_file (str): Path ke file CSV
            batch_size (int): Jumlah rows per commit
        """
        try:
            print(f"\n📂 Membaca file CSV: {csv_file}")
            
            # Cek file exists
            if not Path(csv_file).exists():
                print(f"✗ File {csv_file} tidak ditemukan!")
                return False
            
            # Buka dan baca CSV
            with open(csv_file, 'r', encoding='utf-8') as f:
                csv_reader = csv.DictReader(f)
                
                print("\n🔄 Memulai migrasi data...\n")
                
                batch_count = 0
                for row in csv_reader:
                    self.stats['total_rows'] += 1
                    
                    # Insert anime
                    if self.insert_anime(row):
                        self.stats['inserted_animes'] += 1
                        status = "✓"
                    else:
                        self.stats['failed_rows'] += 1
                        status = "✗"
                    
                    # Progress indicator
                    if self.stats['total_rows'] % 10 == 0:
                        progress = (self.stats['total_rows'] / 100) * 10
                        print(f"  [{progress:.0f}%] {self.stats['total_rows']} rows | "
                              f"Success: {self.stats['inserted_animes']} | "
                              f"Failed: {self.stats['failed_rows']}")
                    
                    batch_count += 1
                    if batch_count >= batch_size:
                        batch_count = 0
            
            print(f"\n✓ Migrasi data selesai!")
            self.print_migration_summary()
            return True
            
        except Exception as e:
            print(f"✗ Error selama migrasi: {e}")
            return False
    
    def print_migration_summary(self):
        """Menampilkan ringkasan hasil migrasi"""
        print("\n" + "="*50)
        print("RINGKASAN MIGRASI DATA")
        print("="*50)
        print(f"Total baris CSV:      {self.stats['total_rows']}")
        print(f"Berhasil di-insert:   {self.stats['inserted_animes']}")
        print(f"Gagal di-insert:      {self.stats['failed_rows']}")
        print(f"Success rate:         {(self.stats['inserted_animes']/max(self.stats['total_rows'], 1)*100):.2f}%")
        
        if self.stats['errors']:
            print(f"\nError ({len(self.stats['errors'])}):")
            for error in self.stats['errors'][:5]:  # Tampilkan 5 error pertama
                print(f"  - {error}")
            if len(self.stats['errors']) > 5:
                print(f"  ... dan {len(self.stats['errors'])-5} error lainnya")
        
        print("="*50)
    
    def verify_migration(self):
        """Memverifikasi hasil migrasi"""
        try:
            print("\n✓ Memverifikasi hasil migrasi...\n")
            
            # Total anime
            self.cursor.execute("SELECT COUNT(*) as total FROM animes")
            total = self.cursor.fetchone()['total']
            print(f"  Total anime di database: {total}")
            
            # Anime per type
            query = """
            SELECT t.type_name, COUNT(a.anime_id) as count
            FROM animes a
            LEFT JOIN types t ON a.type_id = t.type_id
            GROUP BY t.type_id, t.type_name
            ORDER BY count DESC
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            print(f"\n  Distribusi anime per tipe:")
            for row in results:
                type_name = row['type_name'] if row['type_name'] else 'Unknown'
                print(f"    - {type_name}: {row['count']} anime")
            
            # Top rated anime
            query = """
            SELECT title, score FROM animes 
            WHERE score > 0 
            ORDER BY score DESC LIMIT 5
            """
            self.cursor.execute(query)
            top_animes = self.cursor.fetchall()
            
            print(f"\n  Top 5 anime berdasarkan score:")
            for i, anime in enumerate(top_animes, 1):
                print(f"    {i}. {anime['title']} (Score: {anime['score']})")
            
            print("\n✓ Verifikasi selesai!")
            
        except Error as e:
            print(f"✗ Error saat verifikasi: {e}")
    
    def run_full_migration(self, csv_file='anime.csv', sql_file='database_schema.sql'):
        """
        Menjalankan migrasi lengkap dari awal
        
        Args:
            csv_file (str): Path ke file CSV
            sql_file (str): Path ke file SQL schema
        """
        print("\n" + "="*50)
        print("MIGRASI DATABASE ANIME - FULL PROCESS")
        print("="*50)
        
        # Step 1: Connect
        if not self.connect():
            return False
        
        # Step 2: Create database schema
        if not self.create_database(sql_file):
            self.disconnect()
            return False
        
        # Step 3: Migrate data
        if not self.migrate_from_csv(csv_file):
            self.disconnect()
            return False
        
        # Step 4: Verify
        self.verify_migration()
        
        # Step 5: Disconnect
        self.disconnect()
        
        print("\n✓ Semua proses selesai!")
        return True


# ===================================
# MAIN EXECUTION
# ===================================
if __name__ == "__main__":
    # Create migration instance
    migration = AnimeDataMigration(DB_CONFIG)
    
    # Run full migration
    success = migration.run_full_migration(
        csv_file='anime.csv',
        sql_file='database_schema.sql'
    )
    
    # Exit dengan status code
    sys.exit(0 if success else 1)
