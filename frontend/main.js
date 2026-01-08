async function translateText() {
    const text = document.getElementById("inputText").value;
    const source = document.getElementById("sourceLang").value;
    const target = document.getElementById("targetLang").value;

    const res = await fetch("/api/translate", {  // mismo dominio que frontend
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({text, source_lang: source, target_lang: target})
    });

    const data = await res.json();
    document.getElementById("outputText").innerText = data.translated_text;

    const audio = document.getElementById("audio");
    audio.src = "data:audio/mp3;base64," + data.audio_base64;
    audio.play();
}
document.getElementById("translateBtn").addEventListener("click", translateText);
