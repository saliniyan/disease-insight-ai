import React, { useState } from "react";
import Home from "./Home";
import Blog from "./Blog";
import Disease_pred from "./Disease_pred";
import "./App.css";

const App = () => {
  const [activeTab, setActiveTab] = useState("Home");

  return (
    <div className="app-container">
      {/* Sidebar Navigation */}
      <div className="sidebar">
        <button
          className={activeTab === "Home" ? "tab active" : "tab"}
          onClick={() => setActiveTab("Home")}
        >
          🏠 Home
        </button>
        <button
          className={activeTab === "Blog" ? "tab active" : "tab"}
          onClick={() => setActiveTab("Blog")}
        >
          📖 Blog
        </button>
        <button
          className={activeTab === "Disease_pred" ? "tab active" : "tab"}
          onClick={() => setActiveTab("Disease_pred")}
        >
          ⚕️ Disease Prediction
        </button>
      </div>

      {/* Content Area */}
      <div className="content">
        {activeTab === "Home" && <Home />}
        {activeTab === "Blog" && <Blog />}
        {activeTab === "Disease_pred" && <Disease_pred />}
      </div>
    </div>
  );
};

export default App;
