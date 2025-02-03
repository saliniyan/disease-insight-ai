import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load the dataset
df1 = pd.read_csv("https://raw.githubusercontent.com/saliniyan/saliniyan.github.io/main/data%20(5).csv")

# Encode categorical variables
le = LabelEncoder()
for i in df1.columns:
    df1[i] = le.fit_transform(df1[i])

# Remove rows where the target class is 20
df1 = df1[df1.iloc[:, -1] != 20]

# Split features and labels
X = df1.iloc[:, :-1]
y = df1.iloc[:, -1]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create an ensemble classifier
'''ensemble_classifier = VotingClassifier(estimators=[
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

joblib.dump(ensemble_classifier, 'model_for_disease_prediction.joblib')
print("Model saved as 'model_for_disease_prediction.joblib'") '''

ensemble_classifier = joblib.load('model_for_disease_prediction.joblib')

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
