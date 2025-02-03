import React, { useState } from "react";
import axios from "axios";

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

  // Handle input change
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value === "M" || value === "F" ? value : Number(value), // Convert non-gender inputs to numbers
    });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setPrediction(null);

    // Validate AGE input
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
    <div className="max-w-lg mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-semibold text-center mb-4">Lung Cancer Prediction</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Gender Input */}
        <div>
          <label className="block font-medium">Gender:</label>
          <select
            name="GENDER"
            value={formData.GENDER}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          >
            <option value="M">Male</option>
            <option value="F">Female</option>
          </select>
        </div>

        {/* Age Input */}
        <div>
          <label className="block font-medium">Age:</label>
          <input
            type="number"
            name="AGE"
            value={formData.AGE}
            onChange={handleChange}
            className="w-full p-2 border rounded"
            required
          />
        </div>

        {/* Other Symptoms Checkboxes */}
        {["SMOKING", "YELLOW_FINGERS", "ANXIETY", "PEER_PRESSURE", "CHRONICDISEASE", 
          "FATIGUE", "ALLERGY", "WHEEZING", "ALCOHOLCONSUMING", "COUGHING", 
          "SHORTNESSOFBREATH", "SWALLOWINGDIFFICULTY", "CHESTPAIN"].map((symptom) => (
        <div key={symptom} className="flex items-center">
        <input
            type="checkbox"
            name={symptom}
            checked={formData[symptom] === 2} // Check if value is 2
            onChange={() => setFormData({
            ...formData,
            [symptom]: formData[symptom] === 2 ? 1 : 2 // Toggle between 1 and 2
            })}
            className="mr-2"
        />
        <label className="capitalize">{symptom.replace("_", " ").toLowerCase()}</label>
        </div>
        ))}

        {/* Submit Button */}
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600"
          disabled={loading}
        >
          {loading ? "Predicting..." : "Predict Lung Cancer"}
        </button>
      </form>

      {/* Display Prediction Result */}
      {prediction && (
        <div className="mt-4 p-4 bg-gray-100 rounded text-center font-semibold">
          {prediction}
        </div>
      )}
    </div>
  );
};

export default Lung;
