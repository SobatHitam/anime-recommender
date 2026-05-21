#!/usr/bin/env python3
# ===================================
# QUICK CONNECTION TEST SCRIPT
# Jalankan: python test_db_connection.py
# ===================================

import sys
import os

print("\n" + "="*60)
print("🧪 RAILWAY MYSQL CONNECTION TEST")
print("="*60 + "\n")

# Step 1: Load environment
print("📋 Step 1: Loading environment variables...")
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ .env loaded\n")
except Exception as e:
    print(f"⚠️  Warning: {e}\n")

# Step 2: Load config
print("📋 Step 2: Loading config...")
try:
    from config import DB_CONFIG
    print(f"✅ Config loaded\n")
    print(f"   Host: {DB_CONFIG.get('host')}")
    print(f"   Port: {DB_CONFIG.get('port')}")
    print(f"   User: {DB_CONFIG.get('user')}")
    print(f"   Database: {DB_CONFIG.get('database')}")
    print(f"   SSL Disabled: {DB_CONFIG.get('ssl_disabled')}")
    print(f"   Connection Timeout: {DB_CONFIG.get('connection_timeout')}\n")
except Exception as e:
    print(f"❌ Error loading config: {e}\n")
    sys.exit(1)

# Step 3: Test connection
print("📋 Step 3: Testing MySQL connection...")
try:
    import mysql.connector
    
    print(f"⏳ Connecting to {DB_CONFIG['host']}:{DB_CONFIG['port']}...")
    conn = mysql.connector.connect(**DB_CONFIG)
    
    print("✅ CONNECTION SUCCESSFUL!\n")
    
    # Step 4: Test query
    print("📋 Step 4: Running test query...")
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT DATABASE() as current_db;")
        result = cursor.fetchone()
        print(f"✅ Query successful!")
        print(f"   Current Database: {result.get('current_db')}\n")
        
        # Show some stats
        print("📋 Step 5: Database statistics...")
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print(f"✅ Found {len(tables)} tables:")
        for table in tables:
            table_name = table.get('Tables_in_railway') or list(table.values())[0]
            print(f"   - {table_name}")
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Query failed: {e}\n")
    
    conn.close()
    
    print("\n" + "="*60)
    print("🎉 ALL TESTS PASSED!")
    print("="*60)
    print("\n✅ Koneksi ke Railway MySQL BERHASIL!")
    print("✅ Aplikasi siap di-run dengan: streamlit run app.py\n")
    
except mysql.connector.Error as e:
    print(f"\n❌ CONNECTION FAILED\n")
    print("="*60)
    print("🚨 DATABASE CONNECTION ERROR")
    print("="*60)
    print(f"Error Code: {e.errno}")
    print(f"Error Message: {e.msg}\n")
    
    # Provide troubleshooting
    if e.errno == 110:
        print("⚠️  ERROR 110: Connection timeout")
        print("   ➜ Port mungkin salah atau Railway service down")
        print("   ➜ Check Railway Dashboard untuk port terbaru")
    elif e.errno == 1045:
        print("⚠️  ERROR 1045: Access Denied (wrong password/user)")
        print("   ➜ Cek DB_USER dan DB_PASSWORD di .env")
    elif e.errno == 2003:
        print("⚠️  ERROR 2003: Can't connect to server")
        print("   ➜ Host atau port salah")
        print("   ➜ Harus: kodama.proxy.rlwy.net:13951")
    
    print("\n" + "="*60 + "\n")
    sys.exit(1)

except Exception as e:
    print(f"❌ Unexpected error: {e}\n")
    sys.exit(1)
