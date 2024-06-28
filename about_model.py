from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import pandas as pd

# Load the dataset
df1 = pd.read_csv("https://raw.githubusercontent.com/saliniyan/saliniyan.github.io/main/data%20(5).csv")

# Encode categorical variables
le = LabelEncoder()
for i in df1.columns:
    df1[i] = le.fit_transform(df1[i])

# Assume the last column is the target variable
X = df1.iloc[:, :-1]
y = df1.iloc[:, -1]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Load the trained model
ensemble_classifier = joblib.load('model_for_disease_prediction')

# Evaluate the model
accuracy = ensemble_classifier.score(X_test, y_test)
print(f"Model Accuracy: {accuracy}")

# Display the algorithms used in the ensemble model
if hasattr(ensemble_classifier, 'estimators_'):
    print("Algorithms used in the model:")
    for estimator in ensemble_classifier.estimators_:
        print(type(estimator).__name__)
else:
    print(f"The model does not have multiple estimators. It is a {type(ensemble_classifier).__name__}.")