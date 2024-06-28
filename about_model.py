import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib

df1 = pd.read_csv("https://raw.githubusercontent.com/saliniyan/saliniyan.github.io/main/data%20(5).csv")

le = LabelEncoder()
for i in df1.columns:
    df1[i] = le.fit_transform(df1[i])

X = df1.iloc[:, :-1]
y = df1.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

ensemble_classifier = joblib.load('model_for_disease_prediction')

accuracy = ensemble_classifier.score(X_test, y_test)
print(f"Model Accuracy: {accuracy}")

# Display the algorithms used

print("Algorithms used in the model:")
for estimator in ensemble_classifier.estimators_:
    print(type(estimator).__name__)

print("\nModel Details:")
print(ensemble_classifier)

for idx, estimator in enumerate(ensemble_classifier.estimators_):
    print(f"\nEstimator {idx+1}:")
    print(estimator)
