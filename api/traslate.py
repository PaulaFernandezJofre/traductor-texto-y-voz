from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from gtts import gTTS
import base64
import tempfile
import os

app = FastAPI()

@app.post("/translate")
async def translate(req: Request):
    data = await req.json()
    text = data.get("text", "")
    target_lang = data.get("target_lang", "en")

    # Generar audio en base64
    tts = gTTS(text, lang=target_lang)
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp_file.name)
    with open(tmp_file.name, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode()
    os.unlink(tmp_file.name)

    return JSONResponse({"translated_text": text, "audio_base64": audio_b64})
