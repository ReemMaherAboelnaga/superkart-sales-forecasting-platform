
# =====================================================
# Import Required Libraries
# =====================================================

import streamlit as st
import pandas as pd
import requests

# =====================================================
# Backend Flask API URL
# =====================================================

BACKEND_URL = "http://backend:7860"

# =====================================================
# Application Title
# =====================================================

st.title("🛒 SuperKart ForecastHub")

st.markdown(
    """
    This application uses the final Tuned XGBoost model
    to forecast Product Store Sales Revenue.

    The solution supports:
    - Online Prediction
    - Batch Prediction
    """
)

# =====================================================
# Online Prediction Section
# =====================================================

st.subheader("Online Prediction")

# Product Information

product_weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    value=12.5
)

product_sugar_content = st.selectbox(
    "Product Sugar Content",
    [
        "Low Sugar",
        "Regular",
        "No Sugar"
    ]
)

product_allocated_area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    max_value=1.0,
    value=0.06
)

product_type = st.selectbox(
    "Product Type",
    [
        "Baking Goods",
        "Breads",
        "Breakfast",
        "Canned",
        "Dairy",
        "Frozen Foods",
        "Fruits and Vegetables",
        "Hard Drinks",
        "Health and Hygiene",
        "Household",
        "Meat",
        "Others",
        "Seafood",
        "Snack Foods",
        "Soft Drinks",
        "Starchy Foods"
    ]
)

product_mrp = st.number_input(
    "Product MRP",
    min_value=0.0,
    value=150.0
)

# Store Information

store_id = st.selectbox(
    "Store ID",
    [
        "OUT001",
        "OUT002",
        "OUT003",
        "OUT004"
    ]
)

store_size = st.selectbox(
    "Store Size",
    [
        "Small",
        "Medium",
        "High"
    ]
)

store_location_city_type = st.selectbox(
    "Store Location City Type",
    [
        "Tier 1",
        "Tier 2",
        "Tier 3"
    ]
)

store_type = st.selectbox(
    "Store Type",
    [
        "Departmental Store",
        "Food Mart",
        "Supermarket Type1",
        "Supermarket Type2"
    ]
)

store_age = st.number_input(
    "Store Age",
    min_value=1,
    value=17
)

# Create Input DataFrame

input_data = pd.DataFrame([{

    "Product_Weight":
    product_weight,

    "Product_Sugar_Content":
    product_sugar_content,

    "Product_Allocated_Area":
    product_allocated_area,

    "Product_Type":
    product_type,

    "Product_MRP":
    product_mrp,

    "Store_Id":
    store_id,

    "Store_Size":
    store_size,

    "Store_Location_City_Type":
    store_location_city_type,

    "Store_Type":
    store_type,

    "Store_Age":
    store_age

}])

# =====================================================
# Single Prediction Button
# =====================================================

if st.button(
    "Predict Sales Revenue",
    type="primary"
):

    try:

        response = requests.post(
            f"{BACKEND_URL}/v1/predict",
            json=input_data.to_dict(
                orient="records"
            )[0]
        )

        if response.status_code == 200:

            prediction = response.json()[
                "Predicted Sales Revenue"
            ]

            st.success(
                f"Predicted Sales Revenue: {prediction:,.2f}"
            )

        else:

            st.error(
                "Unable to connect to the prediction API."
            )

    except Exception as e:

        st.error(str(e))

# =====================================================
# Batch Prediction Section
# =====================================================

st.subheader("Batch Prediction")

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# =====================================================
# Batch Prediction Button
# =====================================================

if uploaded_file is not None:

    if st.button(
        "Predict Batch",
        type="primary"
    ):

        try:

            response = requests.post(
                f"{BACKEND_URL}/v1/predictbatch",
                files={
                    "file":
                    uploaded_file
                }
            )

            if response.status_code == 200:

                predictions = response.json()

                st.success(
                    "Batch Prediction Completed Successfully!"
                )

                batch_results = pd.DataFrame(
                    list(predictions.items()),
                    columns=[
                        "Record ID",
                        "Predicted Sales Revenue"
                    ]
                )

                st.dataframe(
                    batch_results
                )

            else:

                st.error(
                    "Unable to connect to the prediction API."
                )

        except Exception as e:

            st.error(str(e))
