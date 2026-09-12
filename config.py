import os 

from dotenv import load_dotenv

load_dotenv()

class Config: ## Bir tanesi anahtar adı diğeri ise varsayılan değer mesela bu isimde ayar var mı yoksa varsayılan değeri kullan
    SECRET_KEY = os.environ.get("SECRET_KEY","geliştirme-icin-gecici-anahtar")
    DATABASE_URL = os.environ.get("DATABASE_URL","cleanspin_leads.db")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY","")
    AI_PROVIDER = os.environ.get("AI_PROVIDER","groq")
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS","*")

    # Yönetim paneli (dashboard) giriş bilgileri.
    # Format: "kullanici_adi:sifre,kullanici_adi2:sifre2,..." (virgülle ayrılmış, en fazla birkaç kişi için).
    # Sunucu her başladığında bu listeden users tablosu yeniden oluşturulur/güncellenir —
    # böylece Render'ın ücretsiz planında veritabanı sıfırlansa bile giriş bilgileri kaybolmaz.
    ADMIN_USERS = os.environ.get("ADMIN_USERS", "erkin:erkin123")

    # Giriş token'ının geçerlilik süresi (saniye). Varsayılan: 8 saat.
    TOKEN_GECERLILIK_SANIYE = int(os.environ.get("TOKEN_GECERLILIK_SANIYE", "28800"))

    BUSINESS_CONTEXT ="""Kimlik — CleanSpin'in satış asistanısın
Ürün — çift hazneli, santrifüj mekanizmalı akıllı temizlik kovası
Faydalar — kirli/temiz su tamamen ayrı → kirli su ile temas yok; bezi elle sıkmaya gerek yok; nem ayarlanabilir, parkede iz bırakmaz; su ve deterjan tasarrufu
Kitle — bireysel (ev/ofis) ve kurumsal (otel, restoran, hastane, temizlik şirketi). Müşterinin hangisi olduğunu anlamaya çalış, ona göre konuş
Marka bilgisi — CleanSpin, Erkin Kubaç Altunbaş tarafından 2026 yılında kurulmuştur. Bu bilgi sorulursa yanıtla, sorulmadıkça sohbete kendiliğinden ekleme.
Ton ve görev — Türkçe konuş; sade, güvenilir, çözüm odaklı ol; bilmediğin bilgiyi 
uydurma (özellikle fiyat — henüz belirlemedik); ad veya telefon numarasını 
SOHBETTE İSTEME — bunun yerine sohbetin uygun bir yerinde kullanıcıyı sayfadaki 
"Teklif İçin Bilgilerinizi Bırakın" formunu doldurmaya yönlendir (örn: "Aşağıdaki
formu doldurursanız size en kısa sürede dönüş yaparız.")
Format — cevapların en fazla 2-4 kısa cümle olsun, düz akıcı metin halinde yaz.
Tablo, madde işareti (- ile başlayan liste), kalın yazı (**) ASLA kullanma —
bunlar sohbet kutusunda düzgün görünmüyor, sadece cümle cümle anlat.
"""
##Business Context ise markanın kimliğini, ürünün ne olduğunu, faydalarını, hedef kitlesini, marka bilgisini ve
#  tonunu belirten bir metin. Bu metin, AI modelinin yanıtlarını şekillendirmek için kullanılır.
class DevelopmentConfig(Config): ##burada Miras kullanıyoruz.Config sınıfını miras alıyoruz ve sadece DEBUG değerini değiştiriyoruz.
    DEBUG = True
class ProductionConfig(Config): ## Aynı şekilde.
    DEBUG = False




config = { #isimden sınıfa dönüştürüyoruz bunu da run.py de çağırıyoruz.
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}    


