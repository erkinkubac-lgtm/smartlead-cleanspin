import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
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
    eposta TEXT,
    mesaj TEXT,
    musteri_tipi TEXT,
    tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
          """

    conn = get_db()
    conn.execute(sql)

    # Tablo daha önce eposta kolonu olmadan oluşturulmuşsa, ekle
    kolonlar = [satir["name"] for satir in conn.execute("PRAGMA table_info(leads)").fetchall()]
    if "eposta" not in kolonlar:
        conn.execute("ALTER TABLE leads ADD COLUMN eposta TEXT")

    # Yönetim paneli (dashboard) giriş yapabilecek kullanıcılar
    sql_users = """CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kullanici_adi TEXT UNIQUE NOT NULL,
    sifre_hash TEXT NOT NULL
    )
          """
    conn.execute(sql_users)

    # ADMIN_USERS ortam değişkenindeki kullanıcıları (yeniden) oluştur.
    # Render'ın ücretsiz planında sunucu 15 dk hareketsizlikten sonra yeniden başladığında
    # SQLite dosyası sıfırlanabiliyor; bu yüzden users tablosu her başlangıçta ortam
    # değişkeninden yeniden kurulur, böylece giriş bilgileri her zaman aynı kalır.
    admin_users_ham = app.config.get("ADMIN_USERS", "")
    for parca in admin_users_ham.split(","):
        parca = parca.strip()
        if not parca or ":" not in parca:
            continue
        kullanici_adi, sifre = parca.split(":", 1)
        kullanici_adi = kullanici_adi.strip()
        sifre = sifre.strip()
        if not kullanici_adi or not sifre:
            continue
        sifre_hash = generate_password_hash(sifre)
        conn.execute(
            """INSERT INTO users (kullanici_adi, sifre_hash) VALUES (?, ?)
               ON CONFLICT(kullanici_adi) DO UPDATE SET sifre_hash=excluded.sifre_hash""",
            (kullanici_adi, sifre_hash)
        )

    conn.commit()
    conn.close()

def lead_ekle(isim, telefon, eposta):
    sql = """INSERT INTO leads (isim, telefon, eposta)
             VALUES (?, ?, ?)"""

    conn = get_db()
    cursor = conn.execute(sql, (isim, telefon, eposta))
    yeni_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return yeni_id

def tum_leadler():
    sql = "SELECT * FROM leads ORDER BY id DESC"

    conn = get_db()
    cursor = conn.execute(sql)
    leadler = cursor.fetchall()
    conn.close()
    return [dict(satir) for satir in leadler]

def kullanici_dogrula(kullanici_adi, sifre):
    """Kullanıcı adı/şifre doğruysa True, değilse False döner."""
    if not kullanici_adi or not sifre:
        return False

    conn = get_db()
    satir = conn.execute(
        "SELECT sifre_hash FROM users WHERE kullanici_adi = ?", (kullanici_adi,)
    ).fetchone()
    conn.close()

    if satir is None:
        return False
    return check_password_hash(satir["sifre_hash"], sifre)
