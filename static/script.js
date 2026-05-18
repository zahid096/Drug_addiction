document.getElementById('predictionForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData(this);

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            const resultCard = document.getElementById('resultCard');
            const resultDiv = document.getElementById('result');

            resultCard.style.display = 'block';

            if (data.error) {
                resultDiv.innerHTML = `<p style="color:red">${data.error}</p>`;
                return;
            }

            let riskClass = data.prediction === 1 ? 'high-risk' : 'low-risk';
            let riskText = data.prediction === 1 ? '⚠️ Addicted' : '✅ Not Addicted';
            let confidence = data.confidence ? (data.confidence * 100).toFixed(2) : 'N/A';

            resultDiv.innerHTML = `
            <div class="${riskClass}">${riskText}</div>
            <p>Confidence: ${confidence}%</p>
        `;
        })
        .catch(() => {
            alert('Server Error!');
        });
});