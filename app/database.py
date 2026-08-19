import sqlite3
from config import Config

def get_db():
    conn = sqlite3.connect(Config.DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(app):
    sql = """CREATE TABLE IF NOT EXISTS leads(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    isim TEXT NOT NULL,
    telefon TEXT NOT NULL,
    mesaj TEXT,
    musteri_tipi TEXT,
    tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
          """

    conn= get_db()
    conn.execute(sql)
    conn.commit()
    conn.close()

def lead_ekle(isim, telefon, mesaj, musteri_tipi=None):
    sql = """INSERT INTO leads (isim, telefon, mesaj, musteri_tipi)
             VALUES (?, ?, ?, ?)"""

    conn = get_db()
    cursor = conn.execute(sql, (isim, telefon, mesaj, musteri_tipi))
    yeni_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return yeni_id

def tum_leadler():
    sql ="SELECT * FROM leads ORDER BY id DESC"

    conn = get_db()
    cursor = conn.execute(sql)
    leadler = cursor.fetchall()
    conn.close()
    return [dict(satir) for satir in leadler]