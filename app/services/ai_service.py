import requests
import re
from config import Config

class AIServiceError(Exception):
    pass
class AIService:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.provider = Config.AI_PROVIDER
        self.business_context = Config.BUSINESS_CONTEXT
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model="openai/gpt-oss-20b"
    def _sistem_mesaji_olustur(self):
        return {"role": "system", "content": self.business_context}

    def _cevabi_temizle(self, metin):
        # ** kalın yazı ** işaretlerini kaldır, içindeki yazıyı koru
        metin = re.sub(r"\*\*(.*?)\*\*", r"\1", metin)

        # Tablo satırlarını (| ... | ve |---|---| gibi) kaldır
        satirlar = metin.split("\n")
        satirlar = [s for s in satirlar if not re.match(r"^[\|\-\s]+$", s)]
        metin = "\n".join(satirlar).replace("|", " ")

        # Yarım kalan son cümleyi kes, son tam noktada bitir
        son_nokta = max(metin.rfind("."), metin.rfind("!"), metin.rfind("?"))
        if son_nokta != -1:
            metin = metin[:son_nokta + 1]

        metin = metin.strip()
        if not metin:
            return "Bu konuda size yardımcı olmak isterim — daha spesifik bir soru sorar mısınız?"
        return metin
    


    def _grog_istegi_at(self, mesajlar):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "model": self.model,
            "messages": mesajlar,
            "temperature": 0.4,
            "max_tokens": 300,
            "reasoning_effort": "low"
        }
        try:
            yanit = requests.post(self.api_url, headers=headers, json=body, timeout=10)
        except requests.exceptions.RequestException as hata:
            raise AIServiceError(f"Groq API isteği başarısız oldu: {hata}")

        if yanit.status_code != 200:
            raise AIServiceError(f"Groq API isteği başarısız oldu: {yanit.status_code} - {yanit.text}")

        veri = yanit.json()
        return veri.get("choices", [{}])[0].get("message", {}).get("content", "")
    def yanit_uret(self, mesaj, gecmis=None):
        if gecmis is None:
            gecmis = []

        if not self.api_key:
            return "Şu an demo modundayım; sohbet özelliğim tam aktif değil. Ama size CleanSpin'in çift hazneli, kirli-temiz suyu ayıran akıllı temizlik kovası hakkında bilgi verebilirim — dilerseniz iletişim bilgilerinizi bırakın, size dönüş yapalım."


        mesajlar = [self._sistem_mesaji_olustur()] + gecmis + [{"role": "user", "content": mesaj}]
        ham_cevap = self._grog_istegi_at(mesajlar)
        return self._cevabi_temizle(ham_cevap)

        


ai_service = AIService()