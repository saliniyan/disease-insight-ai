import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load dataset
df = pd.read_csv("backend/disease/lung_cancer.csv")  # Update with your actual file path

# Encode categorical variables
le = LabelEncoder()
df["GENDER"] = le.fit_transform(df["GENDER"])  # Convert 'M'/'F' into numerical values
df["LUNG_CANCER"] = df["LUNG_CANCER"].map({"YES": 1, "NO": 0})  # Convert labels

# Define input features and target
X = df.drop(columns=["LUNG_CANCER"])
y = df["LUNG_CANCER"]

# Normalize features (Scaling)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model and scaler
joblib.dump(model, "lung_cancer_model.joblib")
joblib.dump(scaler, "scaler_lung_cancer.joblib")

print("Model trained and saved successfully!")
