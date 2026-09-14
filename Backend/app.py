from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "Frontend")

app = Flask(__name__)
CORS(app)

# --------------------------------------------------
# Load trained model
# --------------------------------------------------

model_path = os.path.join(
    os.path.dirname(__file__),
    "accident_model.pkl"
)

model = joblib.load(model_path)

print("Accident model loaded successfully!")


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.route("/")
def home():
    return open(os.path.join(FRONTEND_DIR, "index.html"), encoding="utf-8").read()


# --------------------------------------------------
# Prediction
# --------------------------------------------------

@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    input_data = pd.DataFrame([data])

    # Model probabilities
    probabilities = model.predict_proba(input_data)[0]

    classes = model.classes_

    probability_dict = dict(
        zip(classes, probabilities)
    )

    class_1_probability = probability_dict.get(1, 0)
    class_2_probability = probability_dict.get(2, 0)
    class_3_probability = probability_dict.get(3, 0)

    # --------------------------------------------------
    # ML Risk Score
    # --------------------------------------------------

    risk_score = (
        class_1_probability * 100
        + class_2_probability * 60
        + class_3_probability * 20
    )

    # --------------------------------------------------
    # Additional condition score
    # --------------------------------------------------

    condition_score = 0

    # Traffic
    vehicles = int(data.get("Number_of_Vehicles", 1))

    if vehicles >= 5:
        condition_score += 25
    elif vehicles >= 3:
        condition_score += 10

    # Casualties
    casualties = int(data.get("Number_of_Casualties", 0))

    if casualties >= 4:
        condition_score += 20
    elif casualties >= 2:
        condition_score += 10

    # Speed
    speed = int(data.get("Speed_limit", 30))

    if speed >= 70:
        condition_score += 15
    elif speed >= 50:
        condition_score += 5

    # Weather
    weather = data.get("Weather_Conditions", "")

    if "Raining with high winds" in weather:
        condition_score += 20
    elif "Raining" in weather:
        condition_score += 10
    elif "Fog" in weather:
        condition_score += 10

    # Road condition
    road = data.get("Road_Surface_Conditions", "")

    if road == "Wet or damp":
        condition_score += 10

    # --------------------------------------------------
    # Final Risk Score
    # --------------------------------------------------

    final_risk_score = (
        risk_score * 0.5
        + condition_score * 0.5
    )

    final_risk_score = min(
        final_risk_score,
        100
    )

    # --------------------------------------------------
    # Determine Risk Level
    # --------------------------------------------------

    if final_risk_score >= 55:

        prediction = 1
        risk = "High Risk"
        description = "Severe Accident Risk"

    elif final_risk_score >= 35:

        prediction = 2
        risk = "Medium Risk"
        description = "Moderate Accident Risk"

    else:

        prediction = 3
        risk = "Low Risk"
        description = "Slight Accident Risk"

    # --------------------------------------------------
    # Print result
    # --------------------------------------------------

    print("\nPrediction Result:")

    print(
        "Class 1 Probability:",
        round(class_1_probability * 100, 2),
        "%"
    )

    print(
        "Class 2 Probability:",
        round(class_2_probability * 100, 2),
        "%"
    )

    print(
        "Class 3 Probability:",
        round(class_3_probability * 100, 2),
        "%"
    )

    print(
        "ML Risk Score:",
        round(risk_score, 2)
    )

    print(
        "Condition Score:",
        round(condition_score, 2)
    )

    print(
        "Final Risk Score:",
        round(final_risk_score, 2)
    )

    print(
        "Risk Level:",
        risk
    )

    # --------------------------------------------------
    # Send result to frontend
    # --------------------------------------------------

    return jsonify({

        "prediction": prediction,

        "risk": risk,

        "description": description,

        "risk_score": round(
            final_risk_score,
            2
        ),

        "class_1_probability": round(
            class_1_probability * 100,
            2
        ),

        "class_2_probability": round(
            class_2_probability * 100,
            2
        ),

        "class_3_probability": round(
            class_3_probability * 100,
            2
        )
    })


# --------------------------------------------------
# Run Flask
# --------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)