# backend/app.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from gtts import gTTS
import base64
import tempfile
import os
import requests

app = FastAPI()

# =========================
# IDIOMAS
LANGUAGES = {
    "Español": "es",
    "English": "en",
    "Français": "fr",
    "Deutsch": "de",
    "Italiano": "it",
    "Português": "pt",
    "中文": "zh",
    "日本語": "ja",
    "한국어": "ko",
    "العربية": "ar"
}

# =========================
# MODELO DE REQUEST
class TranslateRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str

# =========================
# FUNCIÓN OLLAMA
def ollama_translate(text, source, target):
    prompt = f"Translate the following text from {source} to {target}.\n{text}"
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.1:8b", "prompt": prompt, "stream": False},
            timeout=60
        )
        r.raise_for_status()
        return r.json().get("response", "").strip()
    except:
        return text

# =========================
# RUTA DE API
@app.post("/translate")
def translate(req: TranslateRequest):
    translated = ollama_translate(req.text, LANGUAGES[req.source_lang], LANGUAGES[req.target_lang])
    text = req.get("text", "")
    target_lang = req.get("target_lang", "en")

    

    # gTTS a base64
    tts = gTTS(translated, lang=LANGUAGES[req.target_lang])
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp_file.name)
    with open(tmp_file.name, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode()
    os.unlink(tmp_file.name)

    return {"translated_text": translated, "audio_base64": audio_b64}
