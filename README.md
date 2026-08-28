# SmartLead AI — CleanSpin

Ziyaretçilerle yapay zekâ üzerinden sohbet eden ve iletişim bilgilerini (lead) toplayan bir satış asistanı sistemi. **CleanSpin** markası için özelleştirilmiştir — çift hazneli, santrifüj mekanizmalı akıllı temizlik kovası üreten bir marka.

Sistem iki arayüzden oluşur:
- **Karşılama sayfası** — ziyaretçi yapay zekâ ile sohbet eder, ilgilenirse ad/telefon formunu doldurur.
- **Yönetim paneli** — işletme sahibi, toplanan lead kayıtlarını bir listede görür.

## Canlı bağlantılar

- **Backend (Render):** https://cleanspin-backend.onrender.com
- **Wix sitesi:** https://erkinkubac.wixstudio.com/cleanspinhijyen

## Teknoloji yığını

| Katman | Teknoloji |
|---|---|
| Backend | Python, Flask |
| Veritabanı | SQLite |
| Yapay zekâ | Groq API (`openai/gpt-oss-20b`) |
| Frontend | Wix Studio + Velo (JavaScript) |
| Barındırma | Render (backend), Wix (frontend) |

## Mimari

```
smartlead_ai/
├── config.py              # Ayarlar (ortam değişkenleri, BUSINESS_CONTEXT)
├── run.py                 # Giriş noktası
└── app/
    ├── __init__.py         # Uygulama fabrikası (create_app)
    ├── database.py         # SQLite işlemleri (SADECE burada SQL var)
    ├── routes.py           # HTTP uç noktaları (yönlendirme, SQL/AI kodu yok)
    └── services/
        └── ai_service.py   # Groq API çağrıları (SADECE burada AI çağrısı var)
```

Her dosyanın tek bir sorumluluğu vardır (Separation of Concerns). Katmanlar birbirinin işini yapmaz — `routes.py` sadece `database.py` ve `ai_service.py`'deki hazır fonksiyonları çağırır.

## API Uç Noktaları

| Yöntem | Yol | Açıklama |
|---|---|---|
| `GET` | `/health` | Sunucu canlılık kontrolü |
| `POST` | `/api/sohbet` | Kullanıcı mesajını yapay zekâya iletir, cevap döner |
| `POST` | `/api/leads` | Yeni bir lead (isim, telefon) kaydeder |
| `GET` | `/api/leads` | Kayıtlı tüm lead'leri listeler |

## Yerelde Çalıştırma

```powershell
git clone https://github.com/erkinkubac-lgtm/smartlead-cleanspin.git
cd smartlead-cleanspin
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Proje kökünde bir `.env` dosyası oluştur (`.env.example` yoksa aşağıdaki gibi):

```
SECRET_KEY=rastgele-bir-anahtar
GROQ_API_KEY=gsk_...           # console.groq.com'dan alınır
AI_PROVIDER=groq
DATABASE_URL=cleanspin_leads.db
CORS_ORIGINS=*
FLASK_ENV=development
```

Sonra çalıştır:

```powershell
python run.py
```

`http://127.0.0.1:5050/health` adresinde `{"durum": "ayakta"}` görürsen backend hazır demektir.

## Güvenlik Notları

- Tüm SQL sorguları `?` yer tutucusuyla parametreli çalışır (SQL Injection koruması).
- `.env` dosyası `.gitignore` içinde, GitHub'a hiç yüklenmez.
- Render'da ortam değişkenleri panelden ayrı ayarlanır, kodda gizli bilgi yoktur.

## Bilinen Sınırlamalar

- Render'ın ücretsiz planı kalıcı disk sağlamadığı için, sunucu 15 dakika hareketsiz kalıp yeniden başladığında SQLite veritabanı sıfırlanır. Gerçek üretimde kalıcı bir veritabanı (PostgreSQL) kullanılırdı.
