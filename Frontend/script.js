document.getElementById("predictionForm").addEventListener("submit", async function(event) {

    event.preventDefault();

    const time = document.getElementById("time").value;
    const hour = parseInt(time.split(":")[0]);

    const traffic = document.getElementById("traffic").value;
    const weather = document.getElementById("weather").value;
    const road = document.getElementById("road").value;

    const data = {

        Number_of_Vehicles:
            traffic === "low"
                ? 1
                : traffic === "medium"
                ? 3
                : 5,

        Number_of_Casualties:
            Number(document.getElementById("casualties").value),

        Day_of_Week: 2,

        Hour: hour,

        Road_Type: "Single carriageway",

        Speed_limit:
            parseInt(document.getElementById("speed").value),

        Junction_Control:
            "Give way or uncontrolled",

        Light_Conditions:
            "Daylight: Street light present",

        Weather_Conditions:
            weather === "rain"
                ? "Raining without high winds"
                : weather === "fog"
                ? "Fog or mist"
                : weather === "storm"
                ? "Raining with high winds"
                : "Fine without high winds",

        Road_Surface_Conditions:
            road === "poor"
                ? "Wet or damp"
                : road === "normal"
                ? "Wet or damp"
                : "Dry",

        Urban_or_Rural_Area: "Urban",

        Latitude: 51.5,

        Longitude: -0.1,

        Year: 2020
    };

    try {

        const response = await fetch(
            "/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)
            }
        );

        const result = await response.json();

        let message = "";

        if (result.risk === "High Risk") {

            message = "🔴 High Risk – Severe Accident Risk";

        }
        else if (result.risk === "Medium Risk") {

            message = "🟠 Medium Risk – Moderate Accident Risk";

        }
        else {

            message = "🟢 Low Risk – Slight Accident Risk";

        }

        document.getElementById("result").innerHTML = `
            <div class="result-icon">🚦</div>
            <h3>${message}</h3>
            <p>Risk Score: ${result.risk_score}%</p>
        `;

    }

    catch (error) {

        document.getElementById("result").innerHTML = `
            <div class="result-icon">❌</div>
            <p>Unable to connect to the prediction server.</p>
        `;

        console.error(error);

    }

});


// Set current time

function setCurrentTime() {

    const now = new Date();

    const hours =
        String(now.getHours()).padStart(2, "0");

    const minutes =
        String(now.getMinutes()).padStart(2, "0");

    document.getElementById("time").value =
        `${hours}:${minutes}`;
}

setCurrentTime();