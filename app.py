from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
# from plyer import notification
from threading import Thread
import time
from datetime import datetime
import sqlite3
import joblib
from home_remedies import home_remedies

app = Flask(__name__)

# Load and preprocess the dataset using the raw GitHub URL
df1 = pd.read_csv("https://raw.githubusercontent.com/saliniyan/saliniyan.github.io/main/data%20(5).csv")
le = LabelEncoder()
for i in df1.columns:
    df1[i] = le.fit_transform(df1[i])

# Load the trained ensemble classifier
ensemble_classifier = joblib.load('model_for_disease_prediction.joblib')

all_symptoms = [
    "itching", "weight_loss", "dark_urine", "excessive_hunger", "sweating", "loss_of_appetite", "skin_rash",
    "headache", "stomach_pain", "ulcers_on_tongue", "dehydration", "family_history", "mucoid_sputum",
    "extra_marital_contacts", "unsteadiness", "mood_swings", "malaise", "back_pain", "swelling_joints",
    "knee_pain", "indigestion", "pain_during_bowel_movements", "toxic_look_(typhos)", "throat_irritation",
    "shivering", "fatigue", "Unnamed: 26", "chills", "dizziness", "increased_appetite", "enlarged_thyroid",
    "yellowing_of_eyes", "puffy_face_and_eyes", "diarrhoea", "constipation", "internal_itching", "hip_joint_pain",
    "burning_micturition", "breathlessness", "redness_of_eyes", "mild_fever", "drying_and_tingling_lips",
    "irregular_sugar_level", "cold_hands_and_feets", "continuous_sneezing", "neck_pain", "passage_of_gases",
    "nausea", "sinus_pressure", "belly_pain", "weakness_of_one_body_side", "painful_walking", "spotting_ urination",
    "joint_pain", "muscle_weakness", "polyuria", "watering_from_eyes", "restlessness", "slurred_speech",
    "irritation_in_anus", "yellowish_skin", "bloody_stool", "pain_behind_the_eyes", "dischromic _patches",
    "swollen_extremeties", "abdominal_pain", "pain_in_anal_region", "loss_of_smell", "phlegm", "vomiting",
    "sunken_eyes", "blurred_and_distorted_vision", "acidity", "weakness_in_limbs", "anxiety", "muscle_pain",
    "red_spots_over_body", "congestion", "lethargy", "muscle_wasting", "obesity", "visual_disturbances",
    "brittle_nails", "spinning_movements", "high_fever", "lack_of_concentration", "chest_pain", "cough",
    "altered_sensorium", "irritability", "abnormal_menstruation", "depression", "patches_in_throat", "stiff_neck",
    "loss_of_balance", "swelled_lymph_nodes", "palpitations", "fast_heart_rate", "weight_gain", "runny_nose",
    "nodal_skin_eruptions", "blood_in_sputum"
]

def get_db_connection():
    conn = sqlite3.connect('solution.db')
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

# Route for handling login requests
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM solution WHERE username = ? AND password = ?', (username, password))
        user_data = cursor.fetchone()  # Fetch one row

        cursor.close()
        conn.close()

        if user_data:
            # Redirect to the index page after successful login
            return redirect(url_for('index'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match.')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO solution (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        conn.commit()
        conn.close()

        return redirect(url_for('signup_success'))

    return render_template('signup.html')

@app.route('/signup_success')
def signup_success():
    return render_template('signup_success.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    # Get the selected symptoms from the form
    symptoms = request.json.get('symptoms')

    # Create an array to store the symptoms data
    symptoms_array = np.array([[1 if sym in symptoms else 0 for sym in all_symptoms]])

    # Make predictions using the ensemble classifier
    predicted_label = ensemble_classifier.predict(symptoms_array)
    predicted_disease = le.inverse_transform(predicted_label)

    remedy_info = home_remedies.get(predicted_disease[0], [])
    

    return jsonify({'predicted_disease': predicted_disease[0], 'remedy_info': remedy_info})

def send_notification(title, message, description):
    notification.notify(
        title=title,
        message=f"{message}\n\nDescription: {description}",
        timeout=1 
    )
    print(f"Notification sent - Title: {title}, Message: {message}, Description: {description}")

def schedule_notification(title, message, description, scheduled_time):
    current_time = datetime.now().strftime("%H:%M")
    if current_time == scheduled_time:
        send_notification(title, message, description)
    else:
        delay = (datetime.strptime(scheduled_time, "%H:%M") - datetime.strptime(current_time, "%H:%M")).total_seconds()
        if delay > 0:
            # Schedule the notification in a separate thread
            def send_after_delay():
                time.sleep(delay)
                send_notification(title, message, description)
            
            thread = Thread(target=send_after_delay)
            thread.start()

@app.route('/notification.html', methods=['GET', 'POST'])
def show_notification():
    if request.method == 'POST':
        user_time = request.form.get('notification-time')
        description = request.form.get('notification-description')
        if user_time:
            notification_title = "Health care monitor"
            notification_message ="!"
            schedule_notification(notification_title, notification_message, description, user_time)
            return render_template('notification.html', user_time=user_time, description=description)
        else:
            return render_template('notification.html', error="Please enter a valid notification time.")
    return render_template('notification.html')

if __name__ == '__main__':
    app.run(debug=True)
