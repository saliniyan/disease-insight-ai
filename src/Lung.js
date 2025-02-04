import React, { useState } from "react";
import axios from "axios";
import "./Lung.css";

const Lung = () => {
  const [formData, setFormData] = useState({
    GENDER: "M",
    AGE: "",
    SMOKING: 0,
    YELLOW_FINGERS: 0,
    ANXIETY: 0,
    PEER_PRESSURE: 0,
    CHRONICDISEASE: 0,
    FATIGUE: 0,
    ALLERGY: 0,
    WHEEZING: 0,
    ALCOHOLCONSUMING: 0,
    COUGHING: 0,
    SHORTNESSOFBREATH: 0,
    SWALLOWINGDIFFICULTY: 0,
    CHESTPAIN: 0,
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value === "M" || value === "F" ? value : Number(value),
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setPrediction(null);

    if (!formData.AGE || isNaN(formData.AGE)) {
      setPrediction("Please enter a valid age.");
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:5000/predict_lung_cancer", {
        features: formData,
      });
      setPrediction(response.data.prediction);
    } catch (error) {
      setPrediction("Error predicting lung cancer. Try again.");
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h2 className="title">Lung Cancer Prediction</h2>

      <form onSubmit={handleSubmit} className="form-container">
        <div>
          <label>Gender:</label>
          <select name="GENDER" value={formData.GENDER} onChange={handleChange} className="input-field">
            <option value="M">Male</option>
            <option value="F">Female</option>
          </select>
        </div>
        <div>
          <label>Age:</label>
          <input type="number" name="AGE" value={formData.AGE} onChange={handleChange} className="input-field" required />
        </div>

        <div className="checkbox-group">
          {["SMOKING", "YELLOW_FINGERS", "ANXIETY", "PEER_PRESSURE", "CHRONICDISEASE", 
            "FATIGUE", "ALLERGY", "WHEEZING", "ALCOHOLCONSUMING", "COUGHING", 
            "SHORTNESSOFBREATH", "SWALLOWINGDIFFICULTY", "CHESTPAIN"].map((symptom) => (
            <div key={symptom} className="checkbox-container">
              <input
                type="checkbox"
                name={symptom}
                checked={formData[symptom] === 2}
                onChange={() => setFormData({
                  ...formData,
                  [symptom]: formData[symptom] === 2 ? 1 : 2
                })}
                className="checkbox-input"
              />
              <label className="checkbox-label">{symptom.replace("_", " ").toLowerCase()}</label>
            </div>
          ))}
        </div>

        <button type="submit" className="colorful-button" disabled={loading}>
          {loading ? "Predicting..." : "Predict Lung Cancer"}
        </button>
      </form>

      {prediction && <div className="result-box">{prediction}</div>}
    </div>
  );
};

export default Lung;
