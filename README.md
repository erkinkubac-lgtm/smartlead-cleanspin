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
    ├── routes.py           # HTTP uç noktaları (yönlendirme, SQL/AI/giriş kodu yok)
    └── services/
        ├── ai_service.py   # Groq API çağrıları (SADECE burada AI çağrısı var)
        └── auth_service.py # Giriş (login) token'larının üretimi/doğrulanması
```

Her dosyanın tek bir sorumluluğu vardır (Separation of Concerns). Katmanlar birbirinin işini yapmaz — `routes.py` sadece `database.py` ve `ai_service.py`'deki hazır fonksiyonları çağırır.

## API Uç Noktaları

| Yöntem | Yol | Açıklama |
|---|---|---|
| `GET` | `/health` | Sunucu canlılık kontrolü |
| `POST` | `/api/sohbet` | Kullanıcı mesajını yapay zekâya iletir, cevap döner |
| `POST` | `/api/leads` | Yeni bir lead (isim, telefon) kaydeder — herkese açık (ziyaretçi formu) |
| `POST` | `/api/login` | Kullanıcı adı/şifre doğrularsa bir giriş token'ı döner |
| `GET` | `/api/leads` | Kayıtlı tüm lead'leri listeler — **korumalı**, geçerli bir `Authorization: Bearer <token>` başlığı gerektirir |

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
ADMIN_USERS=erkin:sifre1,ayse:sifre2,mehmet:sifre3   # dashboard'a girecek kişiler, virgülle ayrılmış "kullanici_adi:sifre" ikilileri
TOKEN_GECERLILIK_SANIYE=28800   # giriş token'ının geçerlilik süresi (varsayılan 8 saat)
```

`ADMIN_USERS` içindeki kullanıcılar, sunucu her başladığında `users` tablosuna (yeniden) yazılır — böylece Render'ın ücretsiz planında veritabanı sıfırlansa bile giriş bilgileri kaybolmaz. Bir kişinin şifresini değiştirmek için bu ortam değişkenini güncelleyip sunucuyu yeniden başlatmak yeterlidir.

Sonra çalıştır:

```powershell
python run.py
```

`http://127.0.0.1:5050/health` adresinde `{"durum": "ayakta"}` görürsen backend hazır demektir.

## Güvenlik Notları

- Tüm SQL sorguları `?` yer tutucusuyla parametreli çalışır (SQL Injection koruması).
- `.env` dosyası `.gitignore` içinde, GitHub'a hiç yüklenmez.
- Render'da ortam değişkenleri panelden ayrı ayarlanır, kodda gizli bilgi yoktur.
- `GET /api/leads` artık girişsiz çalışmaz: şifreler veritabanında düz metin değil, hash'lenmiş olarak (`werkzeug.security`) saklanır; giriş başarılı olduğunda süreli, imzalı bir token (`itsdangerous`) üretilir ve her istekte `Authorization: Bearer <token>` başlığıyla doğrulanır.

## Bilinen Sınırlamalar

- Render'ın ücretsiz planı kalıcı disk sağlamadığı için, sunucu 15 dakika hareketsiz kalıp yeniden başladığında SQLite veritabanı sıfırlanır. Gerçek üretimde kalıcı bir veritabanı (PostgreSQL) kullanılırdı. `users` tablosu bu sıfırlanmadan etkilenmez çünkü her başlangıçta `ADMIN_USERS`'tan yeniden kurulur; ancak sıfırlanma anında kaydedilmiş `leads` verileri kaybolur.
- `CORS_ORIGINS` hâlâ varsayılan olarak `*` (tüm kaynaklara açık); bir sonraki adım olarak bunun sadece Wix sitesinin adresine (`https://erkinkubac.wixstudio.com`) daraltılması önerilir.
