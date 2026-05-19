const form = document.getElementById("predictionForm");
const predictBtn = document.getElementById("predictBtn");
const resultCard = document.getElementById("resultCard");
const resultValue = document.getElementById("resultValue");
const confidenceSpan = document.getElementById("confidence");
const errorMessageDiv = document.getElementById("errorMessage");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Show loading state
    predictBtn.disabled = true;
    predictBtn.innerHTML = 'Processing... <span class="loader"></span>';
    resultCard.classList.remove("show");
    errorMessageDiv.classList.remove("show");

    // Collect form data
    const formData = new FormData(form);

    try {
        const response = await fetch("/predict", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();

        if (response.ok) {
            // Display result
            if (data.prediction === 1) {
                resultValue.innerHTML = "⚠️ Addicted";
                resultValue.className = "result-value result-addicted";
            } else {
                resultValue.innerHTML = "✅ Not Addicted";
                resultValue.className = "result-value result-not-addicted";
            }

            if (data.confidence) {
                confidenceSpan.innerHTML = `Confidence: ${(data.confidence * 100).toFixed(1)}%`;
            }

            resultCard.classList.add("show");
        } else {
            errorMessageDiv.innerHTML =
                data.error || "An error occurred. Please try again.";
            errorMessageDiv.classList.add("show");
        }
    } catch (error) {
        errorMessageDiv.innerHTML =
            "Network error. Please check if the server is running.";
        errorMessageDiv.classList.add("show");
    } finally {
        predictBtn.disabled = false;
        predictBtn.innerHTML = "🔮 Predict Addiction Risk";
    }
});