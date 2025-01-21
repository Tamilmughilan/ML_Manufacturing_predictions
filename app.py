import os
import pandas as pd
import pickle
from flask import Flask, request, jsonify
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score

app = Flask(__name__)

DATA_FILE = "manufacturing_data.csv"
MODEL_FILE = "model.pkl"

# Endpoint to upload CSV file
@app.route('/upload', methods=['POST'])
def upload_file():
    print(f"Request Path: {request.path}")
    file = request.files['file']
    if file.filename.endswith('.csv'):
        file.save(DATA_FILE)
        return jsonify({"message": "File uploaded successfully"}), 200
    else:
        return jsonify({"error": "Invalid file format"}), 400

# Endpoint to train the model
@app.route('/train', methods=['POST'])
def train_model():
    try:
        df = pd.read_csv(DATA_FILE)

        # Selecting relevant features and target variable
        X = df[['Air temperature [K]', 'Process temperature [K]', 'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']]
        y = df['Machine failure']  # Predicting machine failure (0 or 1)

        # Splitting data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model = DecisionTreeClassifier()
        model.fit(X_train, y_train)

        # Save the trained model
        with open(MODEL_FILE, 'wb') as f:
            pickle.dump(model, f)

        # Evaluate the model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        return jsonify({
            "message": "Model trained successfully",
            "accuracy": round(accuracy, 2),
            "f1_score": round(f1, 2)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to make predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        required_fields = ['Air temperature [K]', 'Process temperature [K]', 'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required input fields"}), 400

        # Prepare input data for prediction
        input_data = [[
            data['Air temperature [K]'],
            data['Process temperature [K]'],
            data['Rotational speed [rpm]'],
            data['Torque [Nm]'],
            data['Tool wear [min]']
        ]]

        # Load the trained model
        with open(MODEL_FILE, 'rb') as f:
            model = pickle.load(f)

        prediction = model.predict(input_data)
        result = "Failure" if prediction[0] == 1 else "No Failure"
        confidence = max(model.predict_proba(input_data)[0])

        return jsonify({
            "Machine Failure": result,
            "Confidence": round(confidence, 2)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
