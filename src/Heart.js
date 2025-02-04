import React, { useState } from "react"; 
import "./Heart.css";

function Heart() {
  const [formData, setFormData] = useState({
    Age: 25,
    Sex: 0, // 0 for Male, 1 for Female
    ChestPainType: 1,
    BP: 120,
    Cholesterol: 200,
    FBSover120: 0,
    EKGResults: 1,
    MaxHR: 150,
    ExerciseAngina: 0,
    STDepression: 1.2,
    SlopeST: 2,
    NumVesselsFluro: 0,
    Thallium: 1,
  });

  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (name, value) => {
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleIncrement = (name) => {
    setFormData((prev) => ({ ...prev, [name]: prev[name] + 1 }));
  };

  const handleDecrement = (name) => {
    setFormData((prev) => ({ ...prev, [name]: Math.max(0, prev[name] - 1) }));
  };

  const handleSubmit = async () => {
    setError(null);
    setPrediction(null);

    try {
      const response = await fetch("http://127.0.0.1:5000/predict_heart_disease", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ features: formData }),
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
      <div className="container">
        <div className="input-grid">
          {Object.keys(formData).map((key) => (
            <div className="input-group" key={key}>
              <label>{key.replace(/([A-Z])/g, " $1")}</label>
              <div className="input-box">
                {key === "Sex" ? (
                  <select
                    value={formData[key]}
                    onChange={(e) => handleChange(key, Number(e.target.value))}
                  >
                    <option value={0}>Male</option>
                    <option value={1}>Female</option>
                  </select>
                ) : (
                  <>
                    <button onClick={() => handleDecrement(key)}>-</button>
                    <input
                      type="number"
                      value={formData[key]}
                      onChange={(e) => handleChange(key, Number(e.target.value))}
                    />
                    <button onClick={() => handleIncrement(key)}>+</button>
                  </>
                )}
              </div>
            </div>
          ))}
        </div>

        <button type="button" onClick={handleSubmit} className="colorful-button">
          Submit
        </button>

        {prediction && <h3>Result: {prediction}</h3>}
        {error && <p style={{ color: "red" }}>{error}</p>}
      </div>
    </div>
  );
}

export default Heart;
