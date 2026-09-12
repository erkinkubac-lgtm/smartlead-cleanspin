from functools import wraps
from flask import Blueprint, request, jsonify
from app import database
from app.services.ai_service import ai_service, AIServiceError
from app.services import auth_service

api  = Blueprint('api', __name__, url_prefix='/api')
sayfalar = Blueprint('sayfalar', __name__)


def giris_gerekli(fonksiyon):
    """Bu decorator ile işaretlenen uç noktalar, geçerli bir Authorization: Bearer <token>
    başlığı olmadan çalışmaz. Token yoksa veya geçersizse 401 döner."""
    @wraps(fonksiyon)
    def sarmalayici(*args, **kwargs):
        auth_basligi = request.headers.get("Authorization", "")
        token = auth_basligi.replace("Bearer ", "", 1).strip()
        kullanici_adi = auth_service.token_dogrula(token)
        if not kullanici_adi:
            return jsonify({"basari": False, "mesaj": "Yetkisiz erişim, lütfen giriş yapın"}), 401
        return fonksiyon(*args, **kwargs)
    return sarmalayici


@api.route("/sohbet", methods=["POST"])
def sohbet():

    veri = request.get_json()
    mesaj = veri.get("mesaj", "")
    gecmis = veri.get("gecmis", [])

    if not mesaj:
        return jsonify({"error": "Mesaj boş olamaz"}), 400

    try:
        cevap = ai_service.yanit_uret(mesaj, gecmis)
    except AIServiceError:
        return jsonify({"basari": False, "mesaj": "AI servisi ile iletişim kurulamadı"}), 503

    return jsonify({"basari": True, "cevap": cevap})
@api.route("/leads", methods=["POST"])
def lead_kaydet():
    veri = request.get_json()
    isim = veri.get("isim", "")
    telefon = veri.get("telefon", "")
    eposta = veri.get("eposta", "")





    if not isim or not telefon:
        return jsonify({"error": "İsim ve telefon alanları zorunludur"}), 400

    yeni_id = database.lead_ekle(isim, telefon, eposta)
    return jsonify({"basari": True, "id": yeni_id}), 201


@api.route("/login", methods=["POST"])
def giris_yap():
    veri = request.get_json() or {}
    kullanici_adi = veri.get("kullanici_adi", "")
    sifre = veri.get("sifre", "")

    if not database.kullanici_dogrula(kullanici_adi, sifre):
        return jsonify({"basari": False, "mesaj": "Kullanıcı adı veya şifre hatalı"}), 401

    token = auth_service.token_uret(kullanici_adi)
    return jsonify({"basari": True, "token": token}), 200


@api.route("/leads", methods=["GET"])
@giris_gerekli
def leadleri_getir():
    leadler = database.tum_leadler()
    return jsonify({"basari": True, "leadler": leadler}), 200
