from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the saved model
model = joblib.load('linear_regression_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from the request
        data = request.get_json(force=True)

        # Prepare input data as a DataFrame
        input_data = pd.DataFrame(data)

        # Make predictions
        predictions = model.predict(input_data)

        # Return predictions as JSON response
        return jsonify(predictions.tolist())
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
