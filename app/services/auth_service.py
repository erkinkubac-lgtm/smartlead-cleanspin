from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from config import Config

_TUZ = "smartlead-dashboard-girisi"  # imza tuzu; token'ın amacını ayırt eder


def _serializer():
    return URLSafeTimedSerializer(Config.SECRET_KEY, salt=_TUZ)


def token_uret(kullanici_adi):
    """Giriş başarılı olduğunda çağrılır; imzalı, süreli bir token döner."""
    return _serializer().dumps({"kullanici_adi": kullanici_adi})


def token_dogrula(token):
    """Token geçerliyse içindeki kullanıcı adını, değilse None döner."""
    if not token:
        return None
    try:
        veri = _serializer().loads(token, max_age=Config.TOKEN_GECERLILIK_SANIYE)
    except (BadSignature, SignatureExpired):
        return None
    return veri.get("kullanici_adi")
