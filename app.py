from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Load model
with open('best_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('label_encoders.pkl', 'rb') as f:
    label_encoders = pickle.load(f)

FEATURE_COLUMNS = [
    'age', 'gender', 'family_history_of_addiction', 'mental_health_issues',
    'past_drug_use', 'peer_pressure', 'stress_or_trauma', 'social_isolation',
    'how_often_they_use_drugs', 'work_or_school_problems', 'health_problems',
    'access_to_drugs', 'why_they_use_drugs', 'trying_to_quit'
]

FIELD_OPTIONS = {
    'gender': ['Male', 'Female'],
    'family_history_of_addiction': ['Yes', 'No'],
    'mental_health_issues': ['Yes', 'No'],
    'past_drug_use': ['Yes', 'No'],
    'peer_pressure': ['Yes', 'No'],
    'stress_or_trauma': ['Yes', 'No'],
    'social_isolation': ['Yes', 'No'],
    'how_often_they_use_drugs': ['Daily', 'Occasionally', 'Rarely', 'Regularly'],
    'work_or_school_problems': ['Poor', 'Average', 'Excellent'],
    'health_problems': ['Yes', 'No'],
    'access_to_drugs': ['Easy', 'Hard', 'No Access'],
    'why_they_use_drugs': ['Curiosity', 'Fit In', 'No Motivation', 'Other', 'Stress Relief'],
    'trying_to_quit': ['Yes', 'No']
}

def encode_input(data):
    encoded = {}

    for col in FEATURE_COLUMNS:
        value = data.get(col, '')

        if col == 'age':
            encoded[col] = float(value) if value else 0
        else:
            try:
                encoded[col] = label_encoders[col].transform([value])[0]
            except:
                encoded[col] = 0

    return encoded


@app.route('/')
def home():
    return render_template('index.html', field_options=FIELD_OPTIONS)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        form_data = {col: request.form.get(col, '') for col in FEATURE_COLUMNS}

        if not form_data['age'].isdigit():
            return jsonify({'error': 'Invalid age'}), 400

        encoded = encode_input(form_data)

        df = pd.DataFrame([encoded])[FEATURE_COLUMNS]

        pred = model.predict(df)[0]

        proba = None
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(df)[0].max()

        return jsonify({
            'prediction': int(pred),
            'confidence': float(proba) if proba else None
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)