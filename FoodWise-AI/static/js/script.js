const predictionForm = document.getElementById("predictionForm");
const resultDiv = document.getElementById("result");

predictionForm.addEventListener("submit", function (event) {

    event.preventDefault();

    // Show loading message
    resultDiv.innerHTML = "<h3>🤖 AI is analyzing...</h3>";

    const formData = new FormData(predictionForm);

    fetch("/predict", {
        method: "POST",
        body: formData
    })

    .then(function (response) {
        return response.json();
    })

    .then(function (data) {

        console.log(data);

        if (data.success) {

            resultDiv.className = "prediction-result";

            resultDiv.innerHTML = `
                <h3>🎯 Predicted Food Demand</h3>

                <div class="prediction-number">
                    ${data.predicted_demand}
                </div>

                <p>Servings Recommended</p>

                <br>

                <p>
                    🍽️ Prepare approximately
                    <strong>${data.predicted_demand}</strong>
                    servings.
                </p>
            `;

        } else {

            resultDiv.innerHTML = `
                <h3>❌ Prediction Error</h3>
                <p>${data.error}</p>
            `;
        }

    })

    .catch(function (error) {

        console.error(error);

        resultDiv.innerHTML = `
            <h3>❌ Connection Error</h3>
            <p>Could not connect to the Flask server.</p>
        `;
    });

});