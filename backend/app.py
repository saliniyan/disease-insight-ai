from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from flask_cors import CORS
from sklearn.preprocessing import LabelEncoder, StandardScaler

app = Flask(__name__)
CORS(app)

# Load dataset and encode labels
df1 = pd.read_csv("https://raw.githubusercontent.com/saliniyan/saliniyan.github.io/main/data%20(5).csv")
le = LabelEncoder()

# Encode symptoms (Ensure consistency with model training)
for col in df1.columns:
    df1[col] = le.fit_transform(df1[col])

# Load trained models and scalers with error handling
try:
    heart_model = joblib.load("backend/model_heart.joblib")
    scaler_heart = joblib.load("backend/scaler_heart.joblib")
    lung_model = joblib.load("backend/lung_cancer_model.joblib")
    scaler_lung = joblib.load("backend/scaler_lung_cancer.joblib")
    ensemble_classifier = joblib.load("/home/saliniyan/Documents/git_project/health-care-monitor/model_for_disease_prediction.joblib")  # Use relative path
except Exception as e:
    heart_model, scaler_heart, lung_model, scaler_lung = None, None, None, None
    print(f"⚠️ Error loading model or scaler: {e}")

# Symptom list for disease prediction
all_symptoms = [
    "itching", "weight_loss", "dark_urine", "excessive_hunger", "sweating", "loss_of_appetite", "skin_rash",
    "headache", "stomach_pain", "ulcers_on_tongue", "dehydration", "family_history", "mucoid_sputum",
    "extra_marital_contacts", "unsteadiness", "mood_swings", "malaise", "back_pain", "swelling_joints",
    "knee_pain", "indigestion", "pain_during_bowel_movements", "toxic_look_(typhos)", "throat_irritation",
    "shivering", "fatigue", "Unnamed: 26", "chills", "dizziness", "increased_appetite", "enlarged_thyroid",
    "yellowing_of_eyes", "puffy_face_and_eyes", "diarrhoea", "constipation", "internal_itching", "hip_joint_pain",
    "burning_micturition", "breathlessness", "redness_of_eyes", "mild_fever", "drying_and_tingling_lips",
    "irregular_sugar_level", "cold_hands_and_feets", "continuous_sneezing", "neck_pain", "passage_of_gases",
    "nausea", "sinus_pressure", "belly_pain", "weakness_of_one_body_side", "painful_walking", "spotting_ urination",
    "joint_pain", "muscle_weakness", "polyuria", "watering_from_eyes", "restlessness", "slurred_speech",
    "irritation_in_anus", "yellowish_skin", "bloody_stool", "pain_behind_the_eyes", "dischromic _patches",
    "swollen_extremeties", "abdominal_pain", "pain_in_anal_region", "loss_of_smell", "phlegm", "vomiting",
    "sunken_eyes", "blurred_and_distorted_vision", "acidity", "weakness_in_limbs", "anxiety", "muscle_pain",
    "red_spots_over_body", "congestion", "lethargy", "muscle_wasting", "obesity", "visual_disturbances",
    "brittle_nails", "spinning_movements", "high_fever", "lack_of_concentration", "chest_pain", "cough",
    "altered_sensorium", "irritability", "abnormal_menstruation", "depression", "patches_in_throat", "stiff_neck",
    "loss_of_balance", "swelled_lymph_nodes", "palpitations", "fast_heart_rate", "weight_gain", "runny_nose",
    "nodal_skin_eruptions", "blood_in_sputum"
]

@app.route('/process_form', methods=['POST'])
def process_form():
    if not ensemble_classifier:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        data = request.json
        symptoms = data.get('symptoms', [])

        if not symptoms:
            return jsonify({"error": "No symptoms selected"}), 400

        # Ensure the symptoms are encoded correctly
        encoded_symptoms = [1 if symptom in symptoms else 0 for symptom in all_symptoms]

        # Convert to NumPy array and reshape for prediction
        symptoms_array = np.array(encoded_symptoms).reshape(1, -1)

        # Make prediction using the ensemble classifier
        prediction = ensemble_classifier.predict(symptoms_array)
        
        # Decode the predicted disease label back to the disease name
        predicted_disease = le.inverse_transform(prediction)

        response = {"disease": predicted_disease[0]}
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 400
@app.route('/predict_heart_disease', methods=['POST'])
def predict_heart_disease():
    if not heart_model or not scaler_heart:
        return jsonify({"error": "Model or Scaler not loaded"}), 500

    try:
        data = request.json
        features = data.get('features', {})

        if not features:
            return jsonify({"error": "No features provided"}), 400

        heart_features = ["Age", "Sex", "ChestPainType", "BP", "Cholesterol", "FBSover120",
                          "EKGResults", "MaxHR", "ExerciseAngina", "STDepression", "SlopeST",
                          "NumVesselsFluro", "Thallium"]

        input_features = [features.get(f, 0) for f in heart_features]
        scaled_features = scaler_heart.transform([input_features])

        prediction = heart_model.predict(scaled_features)
        disease_mapping = {0: "Negative", 1: "Positive"}

        return jsonify({"predicted_disease": disease_mapping.get(int(prediction[0]), "Unknown")})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/predict_lung_cancer', methods=['POST'])
def predict_lung_cancer():
    if not lung_model or not scaler_lung:
        return jsonify({"error": "Model or Scaler not loaded"}), 500

    try:
        data = request.json
        features = data.get('features', {})

        if not features:
            return jsonify({"error": "No features provided"}), 400

        lung_features = ["GENDER", "AGE", "SMOKING", "YELLOW_FINGERS", "ANXIETY", "PEER_PRESSURE",
                         "CHRONICDISEASE", "FATIGUE", "ALLERGY", "WHEEZING", "ALCOHOLCONSUMING",
                         "COUGHING", "SHORTNESSOFBREATH", "SWALLOWINGDIFFICULTY", "CHESTPAIN"]

        features["GENDER"] = 1 if features["GENDER"] == "M" else 0
        input_features = [features.get(feat, 0) for feat in lung_features]
        input_scaled = scaler_lung.transform([input_features])
        prediction = lung_model.predict(input_scaled)
        result = "Lung Cancer Detected" if int(prediction[0]) == 1 else "No Lung Cancer"

        return jsonify({"prediction": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
