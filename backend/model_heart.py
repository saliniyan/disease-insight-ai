import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load the dataset
df1 = pd.read_csv("backend/disease/Heart_Disease_Prediction.csv")

# Encode categorical variables only
categorical_columns = ['Sex', 'Chest pain type', 'FBS over 120', 'EKG results', 
                       'Exercise angina', 'Slope of ST', 'Number of vessels fluro', 'Thallium', 'Heart Disease']

le = LabelEncoder()
for col in categorical_columns:
    df1[col] = le.fit_transform(df1[col])

# Remove rows where the target class is 'Presence' or 'Absence' (this step may not be needed depending on data)
df1 = df1[df1['Heart Disease'].isin([0, 1])]  # Assuming '0' for 'Absence' and '1' for 'Presence'

# Split features and labels
X = df1.iloc[:, :-1]  # All columns except the last one
y = df1.iloc[:, -1]   # The last column is the target (Heart Disease)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Apply feature scaling (important for algorithms like KNN and SVM)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create an ensemble classifier
ensemble_classifier = VotingClassifier(estimators=[
    ('knn', KNeighborsClassifier(n_neighbors=3)),
    ('rf', RandomForestClassifier()),
    ('nb', GaussianNB()),
    ('svm', SVC(probability=True))
], voting='soft')

# Fit the model and predict
ensemble_classifier.fit(X_train, y_train)
y_pred = ensemble_classifier.predict(X_test)

# Print accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Print classification report
print("Classification Report:\n")
print(classification_report(y_test, y_pred))

# Save the model
joblib.dump(ensemble_classifier, 'model_heart.joblib')
print("Model saved as 'model_heart.joblib'")

# Optionally, you can also save the scaler for future use
joblib.dump(scaler, 'scaler_heart.joblib')
print("Scaler saved as 'scaler_heart.joblib'")
