import os 

from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY","geliştirme-icin-gecici-anahtar")
    DATABASE_URL = os.environ.get("DATABASE_URL","cleanspin_leads.db")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY","")
    AI_PROVIDER = os.environ.get("AI_PROVIDER","groq")
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS","*")
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
"""

class DevelopmentConfig(Config):
    DEBUG = True
class ProductionConfig(Config):
    DEBUG = False




config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}    


