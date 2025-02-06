from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle
import logging

# Initialize Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load the trained model
with open(r"E:\website\web environment\models\model.pkl", 'rb') as model_file:
    model = pickle.load(model_file)

# Check the type of the model
print(f"Loaded model type: {type(model)}")

# Define mappings for categorical features
mappings = {
    'trim' : {
        "Limited": 600,
        "Sport": 500,
        "SE": 400,
        "Base": 300
    },
    'transmission': {
        "Automatic": 1,
        "Manual": 0
    },
    'engine': {
        "V6 Cylinder Engine": 1200,
        "V4 Cylinder Engine": 800,
        "3.5L Four Cylinder Engine": 600,
        "2.5L Four Cylinder Engine": 500,
        "2L Four Cylinder Engine": 400
    },
    'drivetrain': {
        "All-Wheel Drive": 2100,
        "Front-Wheel Drive": 4800,
        "Rear-Wheel Drive": 1800
    },
    'condition': {
        "Used": 8000,
        "Certified Pre Owned": 200,
        "New": 150
    },
    'bodyStyle': {
        "Sedan": 3358,
        "SUV": 3236,
        "Coupe": 596,
        "Pickup_Truck": 552,
        "Pickup": 453,
        "Convertible": 422,
        "Hatchback": 340,
        "Wagon": 138,
        "MiniVan": 118,
        "Van": 103
    },
    'location': {
        "SF": 3412,
        "LA": 3072,
        "Austin": 2832
    },
    'interiorColor': {
        "Gray": 800,
        "Black": 700,
        "Tan": 600,
        "Brown": 600,
        "Red": 800,
        "Ceramic": 500,
        "Silver": 650,
        "Yellow": 300,
        "Beige": 800,
        "Cognac": 900
    },
    'exteriorColor': {
        "Gray": 800,
        "Black": 2000,
        "White": 1400,
        "Brown": 700,
        "Red": 600,
        "Clearcoat": 632,
        "Silver": 700,
        "Yellow": 180,
        "Green": 200,
        "Pink": 205
    }
}

# Home route to render the HTML page
@app.route('/')
def home():
    return render_template('New.html')

# Prediction route to handle POST requests
@app.route('/prediction', methods=['POST'])
def predict():
    try:
        # Get JSON data from the request
        data = request.get_json()
        # Log the incoming data
        logging.debug(f"Received data: {data}")  # Log the data

        if not data:
            logging.error("No data received in the request.")  # Log an error if no data is received
            return jsonify({'error': 'No data received'}), 400

        # Extract and validate all required fields
        required_fields = [
                'trim', 'transmission', 'engine', 'drivetrain', 'condition',
            'bodyStyle', 'location', 'interiorColor', 'exteriorColor', 'mileage'
        ]
        
        for field in required_fields:
            if field not in data:
                logging.error(f"Missing field: {field}")  # Log missing fields
                return jsonify({'error': f'Missing field: {field}'}), 400

        # Validate mileage (must be between 2000 and 8000)
        mileage = data.get('mileage')
        if not (2000 <= mileage <= 8000):
            logging.error(f"Invalid mileage: {mileage}")  # Log invalid mileage
            return jsonify({'error': 'Mileage must be between 2000 and 8000'}), 400

        # Validate all categorical fields before using them
        for field in ['trim','transmission', 'engine', 'drivetrain', 'condition', 'bodyStyle', 'location', 'interiorColor', 'exteriorColor']:
            if data[field] not in mappings[field]:
                logging.error(f"Invalid value for {field}: {data[field]}")  # Log invalid categorical values
                return jsonify({'error': f"Invalid value for {field}: {data[field]}"}), 400

        # Create features array using the mappings
        features = np.array([[mappings['trim'][data['trim']],
                            mappings['transmission'][data['transmission']],
                            mappings['engine'][data['engine']],
                            mappings['drivetrain'][data['drivetrain']],
                            mappings['condition'][data['condition']],
                            mappings['bodyStyle'][data['bodyStyle']],
                            mappings['location'][data['location']],
                            mappings['interiorColor'][data['interiorColor']],
                            mappings['exteriorColor'][data['exteriorColor']],
                            mileage]])

        # Make prediction using the loaded model
        prediction = model.predict(features)
        
        # Log the prediction
        logging.debug(f"Prediction result: {prediction}")

        # Check if the prediction is valid (numeric)
        if isinstance(prediction[0], (int, float)):
            prediction_result = float(prediction[0])*-100 # multiplying with -100

         # Format the result with commas and two decimal places
            formatted_prediction = f"{prediction_result:,.2f}"  # Format with 2 decimal places and commas
        else:
            logging.error(f"Invalid prediction output: {prediction}")
            return jsonify({'error': 'Invalid prediction output'}), 500

        # Return the prediction as JSON
        return jsonify({
            'prediction': formatted_prediction,  # Use formatted_prediction here
            'status': 'success'
        })

    except KeyError as e:
        # Handle missing or invalid keys in the data
        logging.error(f"KeyError: {str(e)}")
        return jsonify({'error': f'Invalid value for field: {str(e)}'}), 400
    except Exception as e:
        # Handle any other exceptions
        logging.error(f"Exception: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
