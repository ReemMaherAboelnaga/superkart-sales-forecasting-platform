
import pandas as pd
import joblib
from flask import Flask, request, jsonify

# Initialize Flask API
superkart_api = Flask("SuperKart ForecastHub")

# Load serialized model
MODEL_PATH = "SuperKart__model_v1_0.joblib"
model = joblib.load(MODEL_PATH)

# Home endpoint
@superkart_api.get("/")
def home():
    return "Welcome to the SuperKart ForecastHub Sales Forecasting API!"

# --------------------------------------------------
# Single Prediction Endpoint
# --------------------------------------------------

@superkart_api.post("/v1/predict")
def predict_sales():

    try:

        sales_data = request.get_json()

        input_data = pd.DataFrame([{
            "Product_Weight": sales_data["Product_Weight"],
            "Product_Sugar_Content": sales_data["Product_Sugar_Content"],
            "Product_Allocated_Area": sales_data["Product_Allocated_Area"],
            "Product_Type": sales_data["Product_Type"],
            "Product_MRP": sales_data["Product_MRP"],
            "Store_Id": sales_data["Store_Id"],
            "Store_Size": sales_data["Store_Size"],
            "Store_Location_City_Type": sales_data["Store_Location_City_Type"],
            "Store_Type": sales_data["Store_Type"],
            "Store_Age": sales_data["Store_Age"]
        }])

        prediction = round(
            float(model.predict(input_data)[0]),
            2
        )

        return jsonify({
            "Predicted Sales Revenue": prediction
        })

    except Exception as e:

        return jsonify({
            "Error": str(e)
        })

# --------------------------------------------------
# Batch Prediction Endpoint
# --------------------------------------------------

@superkart_api.post("/v1/predictbatch")
def predict_sales_batch():

    try:

        file = request.files["file"]

        input_data = pd.read_csv(file)

        predictions = [
            round(float(x), 2)
            for x in model.predict(input_data)
        ]

        output_dict = dict(
            zip(
                range(1, len(predictions) + 1),
                predictions
            )
        )

        return jsonify(output_dict)

    except Exception as e:

        return jsonify({
            "Error": str(e)
        })

# --------------------------------------------------
# Run API
# --------------------------------------------------

if __name__ == "__main__":

    superkart_api.run(
        host="0.0.0.0",
        port=7860,
        debug=True
    )
