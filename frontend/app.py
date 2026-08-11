
import streamlit as st
import pandas as pd
import requests

# Backend Flask API URL
BACKEND_URL = "http://backend:7860"

# App Title
st.title("🛒 SuperKart ForecastHub")
st.write("Sales Revenue Forecasting using the Tuned XGBoost Model")

# =====================================================
# Online Prediction
# =====================================================

st.subheader("Online Prediction")

product_weight = st.number_input("Product Weight", min_value=4.0, max_value=22.0, value=12.66, step=0.01)

product_sugar_content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

product_allocated_area = st.number_input(
    "Product Allocated Area",
    min_value=0.004,
    max_value=0.298,
    value=0.056,
    step=0.001,
    format="%.3f"
)

product_type = st.selectbox(
    "Product Type",
    ["Fruits and Vegetables", "Snack Foods", "Frozen Foods", "Dairy",
     "Household", "Baking Goods", "Canned", "Health and Hygiene",
     "Meat", "Soft Drinks", "Breads", "Hard Drinks", "Others",
     "Starchy Foods", "Breakfast", "Seafood"]
)

product_mrp = st.number_input(
    "Product MRP",
    min_value=31.0,
    max_value=266.0,
    value=146.74,
    step=0.01
)

store_id = st.selectbox(
    "Store ID",
    ["OUT001", "OUT002", "OUT003", "OUT004"]
)

store_size = st.selectbox(
    "Store Size",
    ["Small", "Medium", "High"]
)

store_location_city_type = st.selectbox(
    "Store Location City Type",
    ["Tier 1", "Tier 2", "Tier 3"]
)

store_type = st.selectbox(
    "Store Type",
    ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"]
)

store_establishment_year = st.number_input(
    "Store Establishment Year",
    min_value=1987,
    max_value=2009,
    value=2009,
    step=1
)

store_age = 2026 - store_establishment_year

input_data = pd.DataFrame([{
    "Product_Weight": product_weight,
    "Product_Sugar_Content": product_sugar_content,
    "Product_Allocated_Area": product_allocated_area,
    "Product_Type": product_type,
    "Product_MRP": product_mrp,
    "Store_Id": store_id,
    "Store_Size": store_size,
    "Store_Location_City_Type": store_location_city_type,
    "Store_Type": store_type,
    "Store_Age": store_age
}])

if st.button("Predict Sales Revenue", type="primary"):

    response = requests.post(
        f"{BACKEND_URL}/v1/predict",
        json=input_data.to_dict(orient="records")[0]
    )

    if response.status_code == 200:
        prediction = response.json()["Predicted Sales Revenue"]
        st.success(f"Predicted Sales Revenue: {prediction:,.2f}")
    else:
        st.error("Unable to connect to the prediction API.")

# =====================================================
# Batch Prediction
# =====================================================

st.subheader("Batch Prediction")

uploaded_file = st.file_uploader(
    "Upload CSV file for batch prediction",
    type=["csv"]
)

if uploaded_file is not None:

    if st.button("Predict Batch", type="primary"):

        response = requests.post(
            f"{BACKEND_URL}/v1/predictbatch",
            files={"file": uploaded_file}
        )

        if response.status_code == 200:

            predictions = response.json()

            st.success("Batch Prediction Completed Successfully!")

            st.dataframe(
                pd.DataFrame(
                    list(predictions.items()),
                    columns=["Record ID", "Predicted Sales Revenue"]
                )
            )

        else:
            st.error("Unable to connect to the prediction API.")
