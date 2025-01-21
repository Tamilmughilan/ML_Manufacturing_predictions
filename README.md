# ML Manufacturing Predictions

This project is a RESTful API built using flask that predicts machine failure based on manufacturing data. It accepts a CSV file for training a machine learning model (Decision Tree Classifier or Logistic Regression) and provides predicts the likelihood of machine failure.

## Table of Contents

- [Tech stack](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
  - [Upload Dataset](#upload-dataset)
  - [Train the Model](#train-the-model)
  - [Make Predictions](#make-predictions)
- [API Endpoints](#api-endpoints)
  - [Upload Dataset](#upload-dataset)
  - [Train Model](#train-model)
  - [Make Prediction](#make-prediction)
- [Testing the API](#testing-the-api)

## Technologies Used

- Python 
- Flask
- scikit-learn
- Pandas
- cURL/Postman for testing

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/Tamilmughilan/ML_Manufacturing_predictions.git
   cd ML_Manufacturing_predictions
   ```

2. Set up a Python virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On windows:
     ```bash
     venv\Scripts\activate
     ```
   - On mac or Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the application locally, execute the following:

```bash
python app.py
```

This will start the Flask server, and the API will be available at `http://127.0.0.1:5000`.

### Upload Dataset

To upload the manufacturing dataset, use the following endpoint:

#### Endpoint: `POST /upload`
Upload your CSV file containing the data:

```bash
curl --location --request POST "http://127.0.0.1:5000/upload" \
--form "file=@/path/to/your/manufacturing_data.csv"
```

### Train the Model

Once the dataset is uploaded, you can train the machine learning model using :

#### Endpoint: `POST /train`
Train the model on the uploaded dataset:

```bash
curl --location --request POST "http://127.0.0.1:5000/train"
```

The response will include the accuracy and f score of the trained model in json format.

### Make Predictions

To make predictions, send a POST request with the necessary parameters (Air temperature, Process temperature, Rotational speed, Torque, Tool wear) in JSON format:

#### Endpoint: `POST /predict`
Example request:

```bash
curl --location --request POST "http://127.0.0.1:5000/predict" \
--header "Content-Type: application/json" \
--data-raw '{"Air temperature [K]": 298.2, "Process temperature [K]": 308.7, "Rotational speed [rpm]": 1408, "Torque [Nm]": 46.3, "Tool wear [min]": 3}'
```

The response will include the prediction and confidence score:

```json
{
  "Machine Failure": "No Failure",
  "Confidence": 0.95
}
```

## If you are using an alternative dataset change the columns of the code corresponding to yours:

```bash
X = df[['Air temperature [K]', 'Process temperature [K]', 'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']]
y = df['Machine failure'] 
```

```bash
required_fields = ['Air temperature [K]', 'Process temperature [K]', 'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required input fields"}), 400

      
        input_data = [[
            data['Air temperature [K]'],
            data['Process temperature [K]'],
            data['Rotational speed [rpm]'],
            data['Torque [Nm]'],
            data['Tool wear [min]']
        ]]
```

## API Endpoints

### Upload Dataset
- **URL**: `/upload`
- **Method**: `POST`
- **Body**: Form-data (file)
- **Description**: Upload a CSV file to be used for training the machine learning model.

### Train Model
- **URL**: `/train`
- **Method**: `POST`
- **Body**: None
- **Description**: Train the model on the uploaded dataset. Returns accuracy and F1-score.

### Make Prediction
- **URL**: `/predict`
- **Method**: `POST`
- **Body**: JSON
- **Request Example**:
  ```json
  {
    "Air temperature [K]": 298.2,
    "Process temperature [K]": 308.7,
    "Rotational speed [rpm]": 1408,
    "Torque [Nm]": 46.3,
    "Tool wear [min]": 3
  }
  
- **Response Example**:
  ```json
  {
    "Machine Failure": "No Failure",
    "Confidence": 0.95
  }
  ```

## Testing the API

You can test the API using `curl` or Postman by sending requests to the relevant endpoints.

### Using cURL
Refer to the examples above for how to use cURL to interact with the API endpoints.

### Using Postman
1. Open Postman.
2. Create a new request.
3. Set the method to `POST` and the URL to `http://127.0.0.1:5000/upload`, `http://127.0.0.1:5000/train`, or `http://127.0.0.1:5000/predict` depending on the action you want to test.
4. For `/upload`, select the `form-data` body type and attach the CSV file.
5. For `/train` and `/predict`, use `raw` JSON format for the body.


