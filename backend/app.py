
# =====================================================
# Import Required Libraries
# =====================================================

import numpy as np
import pandas as pd
import joblib

from flask import (Flask, request, jsonify)

# =====================================================
# Initialize Flask REST API
# =====================================================

superkart_api = Flask("SuperKart ForecastHub")

# =====================================================
# Load Serialized Model
# =====================================================

model = joblib.load("SuperKart__model_v1_0.joblib")

# =====================================================
# Home Endpoint
# =====================================================

@superkart_api.get("/")
def home():
    """
    Handle GET requests to the root endpoint.
    Returns a welcome message confirming that
    the API is running successfully.
    """
    return (
        "Welcome to the SuperKart ForecastHub "
        "Sales Forecasting API!"
    )

# =====================================================
# Single Prediction Endpoint
# =====================================================

@superkart_api.post("/v1/predict")
def predict_sales():
    """
    Handles POST requests for a single sales prediction.
    Expects a JSON payload containing the required
    product and store information.
    Returns:
        Predicted Sales Revenue
    """

    try:

        # -----------------------------------------
        # Read JSON Payload
        # -----------------------------------------

        sales_data = request.get_json()

        # -----------------------------------------
        # Extract Features
        # -----------------------------------------

        sample = {

            "Product_Weight":
            sales_data["Product_Weight"],

            "Product_Sugar_Content":
            sales_data["Product_Sugar_Content"],

            "Product_Allocated_Area":
            sales_data["Product_Allocated_Area"],

            "Product_Type":
            sales_data["Product_Type"],

            "Product_MRP":
            sales_data["Product_MRP"],

            "Store_Id":
            sales_data["Store_Id"],

            "Store_Size":
            sales_data["Store_Size"],

            "Store_Location_City_Type":
            sales_data["Store_Location_City_Type"],

            "Store_Type":
            sales_data["Store_Type"],

            "Store_Age":
            sales_data["Store_Age"]

        }

        # -----------------------------------------
        # Convert to DataFrame
        # -----------------------------------------

        input_data = pd.DataFrame([sample])

        # -----------------------------------------
        # Generate Prediction
        # -----------------------------------------

        predicted_sales = model.predict(input_data)[0]

        # Convert NumPy value to Python float
        predicted_sales = round(float(predicted_sales), 2)

        # -----------------------------------------
        # Return Prediction
        # -----------------------------------------

        return jsonify({"Predicted Sales Revenue": predicted_sales})

    except Exception as e:

        return jsonify({

            "Error":
            str(e)

        })

# =====================================================
# Batch Prediction Endpoint
# =====================================================

@superkart_api.post("/v1/predictbatch")
def predict_sales_batch():
    """
    Handles POST requests for batch prediction.
    Expects:
        CSV File
    Returns:
        Dictionary of predictions
    """

    try:

        # -----------------------------------------
        # Read Uploaded CSV
        # -----------------------------------------

        file = request.files["file"]

        input_data = pd.read_csv(file)

        # -----------------------------------------
        # Generate Predictions
        # -----------------------------------------

        predictions = model.predict(input_data)

        predictions = [round(float(x), 2) for x in predictions]

        # -----------------------------------------
        # Create Prediction Dictionary
        # -----------------------------------------

        prediction_ids = list(range(1, len(predictions) + 1))

        output_dict = dict(zip(prediction_ids, predictions))

        # -----------------------------------------
        # Return Predictions
        # -----------------------------------------

        return jsonify(output_dict)

    except Exception as e:

        return jsonify({

            "Error":
            str(e)

        })

# =====================================================
# Run Flask API
# =====================================================

if __name__ == "__main__":

    superkart_api.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
