import React, { useState } from "react";
import "./Disease_pred.css";

function Heart() {
  const [formData, setFormData] = useState({
    Age: "",
    Sex: "",
    ChestPainType: "",
    BP: "",
    Cholesterol: "",
    FBSover120: "",
    EKGResults: "",
    MaxHR: "",
    ExerciseAngina: "",
    STDepression: "",
    SlopeST: "",
    NumVesselsFluro: "",
    Thallium: "",
  });

  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async () => {
    setError(null);
    setPrediction(null);
  
    // Ensure all fields are filled
    if (Object.values(formData).some(field => field === "")) {
      setError("Please fill in all fields.");
      return;
    }
  
    try {
      const response = await fetch("http://127.0.0.1:5000/predict_heart_disease", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ features: formData }),  // Changed to match backend
      });
  
      const data = await response.json();
      if (response.ok) {
        setPrediction(data.predicted_disease);
      } else {
        setError(data.error || "Something went wrong.");
      }
    } catch (err) {
      setError("Failed to connect to the server.");
    }
  };  

  return (
    <div className="disease">
      <h1>Heart Disease Prediction</h1>
      <form>
        <div className="input-group">
          <label>
            Age:
            <input
              type="number"
              name="Age"
              value={formData.Age}
              onChange={handleInputChange}
            />
          </label>
        </div>

        <div className="input-group">
          <label>
            Sex (0: Female, 1: Male):
            <input
              type="number"
              name="Sex"
              value={formData.Sex}
              onChange={handleInputChange}
            />
          </label>
        </div>

        <div className="input-group">
          <label>
            Chest Pain Type (1-4):
            <input
              type="number"
              name="ChestPainType"
              value={formData.ChestPainType}
              onChange={handleInputChange}
            />
          </label>
        </div>

        <div className="input-group">
          <label>
            Blood Pressure (BP):
            <input
              type="number"
              name="BP"
              value={formData.BP}
              onChange={handleInputChange}
            />
          </label>
        </div>

        <div className="input-group">
          <label>
            Cholesterol:
            <input
              type="number"
              name="Cholesterol"
              value={formData.Cholesterol}
              onChange={handleInputChange}
            />
          </label>
        </div>

        <div className="input-group">
          <label>
            FBS over 120 (0: No, 1: Yes):
            <input
              type="number"
              name="FBSover120"
              value={formData.FBSover120}
              onChange={handleInputChange}
            />
          </label>
        </div>

        <div className="input-group">
          <label>
            EKG Results (0-2):
            <input
              type="number"
              name="EKGResults"
              value={formData.EKGResults}
              onChange={handleInputChange}
            />
          </label>
        </div>

        <div className="input-group">
          <label>
            Max Heart Rate:
            <input
              type="number"
              name="MaxHR"
              value={formData.MaxHR}
              onChange={handleInputChange}
            />
          </label>
        </div>

        <div className="input-group">
          <label>
            Exercise Angina (0: No, 1: Yes):
            <input
              type="number"
              name="ExerciseAngina"
              value={formData.ExerciseAngina}
              onChange={handleInputChange}
            />
          </label>
        </div>

        <div className="input-group">
          <label>
            ST Depression:
            <input
              type="number"
              name="STDepression"
              value={formData.STDepression}
              onChange={handleInputChange}
            />
          </label>
        </div>

        <div className="input-group">
          <label>
            Slope of ST (1-3):
            <input
              type="number"
              name="SlopeST"
              value={formData.SlopeST}
              onChange={handleInputChange}
            />
          </label>
        </div>

        <div className="input-group">
          <label>
            Number of Vessels Fluro:
            <input
              type="number"
              name="NumVesselsFluro"
              value={formData.NumVesselsFluro}
              onChange={handleInputChange}
            />
          </label>
        </div>

        <div className="input-group">
          <label>
            Thallium (0-2):
            <input
              type="number"
              name="Thallium"
              value={formData.Thallium}
              onChange={handleInputChange}
            />
          </label>
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
        <div>
          <h3>Result: {prediction}</h3>
        </div>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default Heart;
