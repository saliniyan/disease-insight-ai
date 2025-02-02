import React from "react";
import "./Home.css";

const Home = () => {
  return (
    <div className="home-container">
      <h1>Welcome to Health Assistant</h1>
      <p>Your one-stop solution for health monitoring and disease prediction.</p>
      <div className="home-cards">
        <div className="card">
          <h2>Disease Prediction</h2>
          <p>Enter your symptoms and predict possible diseases.</p>
        </div>
        <div className="card">
          <h2>Health Blog</h2>
          <p>Read the latest articles on health and wellness.</p>
        </div>
      </div>
    </div>
  );
};

export default Home;
