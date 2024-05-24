document.addEventListener("DOMContentLoaded", function() {
    const recordButton = document.getElementById('recordButton');
    const stopButton = document.getElementById('stopButton');
    const uploadButton = document.getElementById('uploadButton');
    const statusDiv = document.getElementById('status');
    const audioForm = document.getElementById('audioForm');
    let mediaRecorder;
    let audioChunks = [];

    recordButton.addEventListener('click', async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();
        statusDiv.textContent = "Recording...";

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            audioChunks = [];

            const audioFile = new File([audioBlob], 'audio.wav', {
                type: 'audio/wav',
                lastModified: Date.now()
            });

            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(audioFile);
            document.querySelector('input[name="audio"]').files = dataTransfer.files;

            uploadButton.disabled = false;
            statusDiv.textContent = "Recording stopped.";
        };

        recordButton.disabled = true;
        stopButton.disabled = false;
    });

    stopButton.addEventListener('click', () => {
        mediaRecorder.stop();
        recordButton.disabled = false;
        stopButton.disabled = true;
    });
});
