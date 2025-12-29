const micButton = document.getElementById("mic-button");
const chatBox = document.getElementById("chat-box");

let mediaRecorder;
let audioChunks = [];

micButton.addEventListener("click", async () => {
  if (!mediaRecorder || mediaRecorder.state === "inactive") {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);

    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
      audioChunks = [];

      appendMessage("Recording sent...", "user");

      const formData = new FormData();
      formData.append("file", audioBlob, "audio.webm");

      const res = await fetch("http://localhost:8001/upload-audio", {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      appendMessage(data.response, "bot");
    };

    mediaRecorder.start();
    micButton.textContent = "⏹️";
    setTimeout(() => {
      mediaRecorder.stop();
      micButton.textContent = "🎤";
    }, 5000); // Record for 5 seconds
  }
});

function appendMessage(text, sender) {
  const div = document.createElement("div");
  div.className = `message ${sender}`;
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}
