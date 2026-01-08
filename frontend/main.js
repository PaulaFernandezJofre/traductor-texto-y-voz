async function translateText() {
    const text = document.getElementById("inputText").value;
    const source = document.getElementById("sourceLang").value;
    const target = document.getElementById("targetLang").value;

    if (!text) {
        alert("Escribe un mensaje primero");
        return;
    }

    try {
        const res = await fetch("/api/translate", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({text, source_lang: source, target_lang: target})
        });

        const data = await res.json();
        document.getElementById("outputText").innerText = data.translated_text;

        const audio = document.getElementById("audio");
        audio.src = "data:audio/mp3;base64," + data.audio_base64;
        audio.play();

    } catch (err) {
        console.error("Error al traducir:", err);
        alert("Hubo un error en la traducción");
    }
}

document.getElementById("translateBtn").addEventListener("click", translateText);
