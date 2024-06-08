from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
from plyer import notification
from threading import Thread
import time
from datetime import datetime
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
import joblib

app = Flask(__name__)

# Load and preprocess the dataset using the raw GitHub URL
df1 = pd.read_csv("https://raw.githubusercontent.com/saliniyan/saliniyan.github.io/main/data%20(5).csv")
le = LabelEncoder()
for i in df1.columns:
    df1[i] = le.fit_transform(df1[i])

# Load the trained ensemble classifier
ensemble_classifier = joblib.load('model_for_disease_prediction')

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

# Define dictionary for storing home remedy information
home_remedies = {
    'Fungal infection': [
        'Apply diluted tea tree oil to the affected area.',
        'Crush garlic and apply it to the affected area.',
        'Mix apple cider vinegar with water and apply.'
    ],
    'Allergy': [
        'Local honey can help with pollen allergies.',
        'Use a saline solution to clear nasal passages.',
        'Consume quercetin, found in onions, apples, and berries.'
    ],
    'GERD': [
        'Drink aloe vera juice before meals.',
        'Chew gum to increase saliva and reduce acid.',
        'A teaspoon of baking soda in water can neutralize acid.'
    ],
    'Chronic cholestasis': [
        'Milk thistle supports liver health.',
        'Drink dandelion root tea to help liver detox.',
        'Consume turmeric to reduce liver inflammation.'
    ],
    'Drug Reaction': [
        'Stop the medication and consult your doctor.',
        'Apply a cold compress to reduce itching and swelling.',
        'Apply aloe vera to soothe skin irritation.'
    ],
    'Peptic ulcer disease': [
        'Bananas act as natural antacids.',
        'Drink cabbage juice to help heal ulcers.',
        'Consume honey to soothe and heal the stomach lining.'
    ],
    'AIDS': [
        'Garlic boosts the immune system.',
        'Consume aloe vera to help with gastrointestinal issues.',
        'Drink ginger tea to reduce nausea.'
    ],
    'Diabetes': [
        'Drink bitter gourd juice to lower blood sugar levels.',
        'Consume fenugreek seeds to help manage diabetes.',
        'Use cinnamon to improve insulin sensitivity.'
    ],
    'Gastroenteritis': [
        'Drink ginger tea to reduce nausea.',
        'Consume mint to soothe the stomach.',
        'Follow the BRAT diet (bananas, rice, applesauce, toast).'
    ],
    'Bronchial Asthma': [
        'Consume ginger for its anti-inflammatory properties.',
        'Mix honey and cinnamon to soothe the throat.',
        'Use turmeric to reduce inflammation.'
    ],
    'Hypertension': [
        'Consume garlic to help lower blood pressure.',
        'Eat bananas, which are rich in potassium.',
        'Drink hibiscus tea to help lower blood pressure.'
    ],
    'Migraine': [
        'Apply peppermint oil to temples.',
        'Drink ginger tea to reduce inflammation.',
        'Consider taking butterbur herbal supplements.'
    ],
    'Cervical spondylosis': [
        'Use hot and cold compresses to reduce pain.',
        'Drink turmeric milk for its anti-inflammatory properties.',
        'Consume garlic to reduce inflammation.'
    ],
    'Paralysis (brain hemorrhage)': [
        'Undergo physiotherapy for recovery.',
        'Consume turmeric for its anti-inflammatory properties.',
        'Use ginger to support brain health.'
    ],
    'Jaundice': [
        'Drink sugarcane juice to improve liver function.',
        'Consume lemon to detoxify the liver.',
        'Drink tomato juice for its antioxidants.'
    ],
    'Malaria': [
        'Consume ginger to help reduce symptoms.',
        'Use cinnamon for its anti-inflammatory properties.',
        'Eat grapefruit, which contains quinine.'
    ],
    'Chicken pox': [
        'Take an oatmeal bath to soothe itching.',
        'Apply baking soda to relieve itching.',
        'Use honey to help with skin healing.'
    ],
    'Dengue': [
        'Drink papaya leaf juice to increase platelet count.',
        'Consume neem leaves to boost immunity.',
        'Stay hydrated for recovery.'
    ],
    'Typhoid': [
        'Stay hydrated by drinking plenty of fluids.',
        'Use apple cider vinegar to reduce fever.',
        'Consume garlic to boost immunity.'
    ],
    'Tuberculosis': [
        'Use garlic for its antibacterial properties.',
        'Consume mint to soothe the lungs.',
        'Eat bananas to boost the immune system.'
    ],
    'Common Cold': [
        'Mix honey and lemon to soothe the throat.',
        'Drink ginger tea to reduce symptoms.',
        'Consume chicken soup to boost the immune system.'
    ],
    'Dimorphic hemorrhoids (piles)': [
        'Apply witch hazel to reduce inflammation.',
        'Use aloe vera to soothe the area.',
        'Take warm sitz baths to reduce pain and swelling.'
    ],
    'Hypothyroidism': [
        'Consume coconut oil to improve thyroid function.',
        'Eat seaweed, which is rich in iodine.',
        'Use ginger to support thyroid health.'
    ],
    'Hyperthyroidism': [
        'Take bugleweed herbal supplements.',
        'Consume lemon balm to reduce thyroid activity.',
        'Eat broccoli to help regulate the thyroid.'
    ],
    'Hypoglycemia': [
        'Consume honey for a quick source of glucose.',
        'Drink orange juice to raise blood sugar levels.',
        'Use glucose tablets for immediate relief.'
    ],
    'Osteoarthritis': [
        'Use turmeric for its anti-inflammatory properties.',
        'Consume ginger to reduce pain.',
        'Take Epsom salt baths to reduce joint pain.'
    ],
    '(Vertigo) Paroxysmal Positional Vertigo': [
        'Perform the Epley maneuver to reposition inner ear crystals.',
        'Drink ginger tea to reduce dizziness.',
        'Stay hydrated to help with symptoms.'
    ]
}


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
