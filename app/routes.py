from flask import Blueprint ,request, jsonify
from app import database
from app.services.ai_service import ai_service, AIServiceError

api  = Blueprint('api', __name__, url_prefix='/api')
sayfalar = Blueprint('sayfalar', __name__)

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
    veri= request.get_json()
    isim = veri.get("isim", "")
    telefon = veri.get("telefon", "")
    mesaj = veri.get("mesaj", "")
    musteri_tipi = veri.get("musteri_tipi")

    if not isim or not telefon:
        return jsonify({"error": "İsim ve telefon alanları zorunludur"}), 400

    yeni_id = database.lead_ekle(isim, telefon, mesaj, musteri_tipi)
    return jsonify({"basari": True, "id": yeni_id}), 201


@api.route("/leads", methods=["GET"])
def leadleri_getir():
    leadler = database.tum_leadler()
    return jsonify({"basari": True, "leadler": leadler}), 200
