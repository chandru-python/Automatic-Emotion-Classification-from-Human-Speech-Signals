let mediaRecorder;
let audioChunks = [];
let stream;   // 🔥 IMPORTANT

/* =========================
   START RECORDING
========================= */
function startRecording() {

    if (mediaRecorder && mediaRecorder.state === "recording") {
        return;
    }

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(s => {
            stream = s;   // 🔥 SAVE STREAM

            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.ondataavailable = e => {
                if (e.data.size > 0) {
                    audioChunks.push(e.data);
                }
            };

            mediaRecorder.start();

            document.querySelector(".status").innerText =
                "🎙️ Recording... Speak now";
        })
        .catch(err => {
            alert("Microphone access denied!");
            console.error(err);
        });
}

/* =========================
   STOP RECORDING
========================= */
function stopRecording() {

    if (!mediaRecorder || mediaRecorder.state !== "recording") {
        return;
    }

    mediaRecorder.stop();

    // 🔥 THIS LINE TURNS OFF MIC ICON
    stream.getTracks().forEach(track => track.stop());

    document.querySelector(".status").innerText =
        "⏳ Processing voice...";

    mediaRecorder.onstop = () => {

        // ❗ Browser records WebM, NOT WAV
        const blob = new Blob(audioChunks, { type: "audio/webm" });

        const formData = new FormData();
        formData.append("audio", blob, "voice.webm");

        fetch("/voice-emotion", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {

            const emotionText =
                data.emotion ? data.emotion.toUpperCase() : "SILENCE";

            const confidenceText =
                data.confidence ? data.confidence : "0";

            document.getElementById("emotion").innerText =
                "Emotion: " + emotionText;

            document.getElementById("confidence").innerText =
                "Confidence: " + confidenceText + "%";

            if (typeof updateExplanation === "function") {
                updateExplanation(emotionText);
            }

            document.querySelector(".status").innerText =
                "✅ Analysis complete";
        })
        .catch(err => {
            console.error("Error:", err);

            document.getElementById("emotion").innerText =
                "Emotion: ERROR";

            document.getElementById("confidence").innerText =
                "Confidence: ---";

            if (typeof updateExplanation === "function") {
                updateExplanation("SILENCE");
            }

            document.querySelector(".status").innerText =
                "❌ Error processing audio";
        });
    };
}
