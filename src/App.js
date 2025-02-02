import React, { useState } from "react";
import "./App.css";
import { diseaseInfo, home_remedies } from "./disease";

function App() {
  const [symptoms, setSymptoms] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const [showHomeRemedies, setShowHomeRemedies] = useState(false); // New state for toggling content

  const all_symptoms = [
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
  ];

  const handleCheckboxChange = (event) => {
    const value = event.target.value;
    setSymptoms((prevSymptoms) => {
      if (prevSymptoms.includes(value)) {
        return prevSymptoms.filter((symptom) => symptom !== value);
      } else {
        return [...prevSymptoms, value];
      }
    });
  };

  const handleSubmit = async () => {
    setError(null);
    setPrediction(null);

    if (symptoms.length === 0) {
      setError("Please select at least one symptom.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/process_form", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symptoms: symptoms }),
      });

      const data = await response.json();
      if (response.ok) {
        setPrediction(data.disease);
      } else {
        setError(data.error || "Something went wrong.");
      }
    } catch (err) {
      setError("Failed to connect to the server.");
    }
  };

  // Toggle function for showing home remedies
  const toggleContent = () => {
    setShowHomeRemedies((prev) => !prev);
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Disease Prediction</h1>
      <form>
        <div className="checkbox-group">
          {all_symptoms.map((symptom) => (
            <label key={symptom} className="checkbox-label">
              <input
                type="checkbox"
                value={symptom}
                onChange={handleCheckboxChange}
              />
              {symptom.replace("_", " ").toUpperCase()}
            </label>
          ))}
        </div>
        <button
          type="button"
          onClick={handleSubmit}
          className="colorful-button"
          style={{
            padding: "10px 20px",
            cursor: "pointer",
            marginTop: "20px",
          }}
        >
          Submit
        </button>
      </form>

      {prediction && (
        <>
          <h3>Predicted Disease: {prediction}</h3>

          {/* Button Group */}
          <div style={{ display: "flex", justifyContent: "center", marginTop: "20px" }}>
            <button
              onClick={toggleContent}
              style={{
                marginRight: "10px",
                padding: "10px 20px",
                cursor: "pointer",
                backgroundColor: "#4CAF50",
                color: "white",
                border: "none",
              }}
            >
              Description
            </button>
            <button
              onClick={toggleContent}
              style={{
                padding: "10px 20px",
                cursor: "pointer",
                backgroundColor: "#008CBA",
                color: "white",
                border: "none",
              }}
            >
              Home Remedies
            </button>
          </div>

          {/* Message Box */}
          <div
            style={{
              marginTop: "20px",
              padding: "20px",
              border: "1px solid #ccc",
              borderRadius: "5px",
              maxWidth: "600px",
              marginLeft: "auto",
              marginRight: "auto",
              textAlign: "left",
              backgroundColor: "#f9f9f9",
            }}
          >
            {showHomeRemedies ? (
              home_remedies[prediction] ? (
                <>
                  <h4>Home Remedies:</h4>
                  <ul>
                    {home_remedies[prediction].map((remedy, index) => (
                      <li key={index}>{remedy}</li>
                    ))}
                  </ul>
                </>
              ) : (
                <p>No home remedies available for this disease.</p>
              )
            ) : (
              <p>
                <strong>Description:</strong> {diseaseInfo[prediction] || "No information available."}
              </p>
            )}
          </div>
        </>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default App;
