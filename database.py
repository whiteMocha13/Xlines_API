import sqlite3

def init_db(): 
    conn = sqlite3.connect("xlines.db")  # xlines.db dosyası yoksa SQLite bu satırdan sonra dosyayı oluşturur. 
    conn.execute(                        # conn nesnesi veritabanı dosyası ile olan bağlantının nesnesidir. 
    """
    CREATE TABLE IF NOT EXISTS xlines(
    code INTEGER PRIMARY KEY,
    color TEXT NOT NULL,
    price REAL NOT NULL,
    tax_percent INTEGER NOT NULL,
    stock INTEGER NOT NULL,
    is_active INTEGER NOT NULL,
    shipping_weight REAL NOT NULL
    )
    """
    )
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect("xlines.db", check_same_thread = False) # Thread'i bloklar 
    conn.row_factory = sqlite3.Row # satırı sözlük gibi okDunabilir hale getirir. 
    try:
        yield conn # yield, conn nesnesini endpointe ödünç verip burada bekler. 
    finally:
        conn.close()


