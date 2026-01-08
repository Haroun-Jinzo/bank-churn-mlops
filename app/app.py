import streamlit as st
import requests
import json

# ------------------------------------------------------------------------------
# Configure the page
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Bank Churn Prediction",
    page_icon="🏦",
    layout="wide"
)

# ------------------------------------------------------------------------------
# ⚠️ UPDATE THIS URL TO YOUR AZURE API ⚠️
# Example: "https://bank-churn-api.azurewebsites.net"
# ------------------------------------------------------------------------------
API_URL = "https://bank-churn.redpond-3c4969cd.spaincentral.azurecontainerapps.io" 

# Check if the user forgot to update the URL
if "YOUR-APP-NAME" in API_URL:
    st.error("🚨 Please update the API_URL in streamlit_app.py to your actual Azure address!")
    st.stop()

st.title("🏦 Bank Churn Prediction Dashboard")
st.markdown(f"Connected to API: `{API_URL}`")

# ------------------------------------------------------------------------------
# Sidebar: Input Form
# ------------------------------------------------------------------------------
st.sidebar.header("Customer Profile")

def user_input_features():
    credit_score = st.sidebar.slider("Credit Score", 300, 850, 650)
    age = st.sidebar.slider("Age", 18, 100, 35)
    tenure = st.sidebar.slider("Tenure (Years)", 0, 10, 5)
    balance = st.sidebar.number_input("Balance ($)", min_value=0.0, value=50000.0)
    num_of_products = st.sidebar.selectbox("Number of Products", [1, 2, 3, 4], index=1)
    has_cr_card = st.sidebar.selectbox("Has Credit Card?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    is_active_member = st.sidebar.selectbox("Is Active Member?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    estimated_salary = st.sidebar.number_input("Estimated Salary ($)", min_value=0.0, value=75000.0)
    
    geography = st.sidebar.selectbox("Location", ["France", "Germany", "Spain"])
    
    # Convert geography to model features
    geo_germany = 1 if geography == "Germany" else 0
    geo_spain = 1 if geography == "Spain" else 0
    
    data = {
        "CreditScore": credit_score,
        "Age": age,
        "Tenure": tenure,
        "Balance": balance,
        "NumOfProducts": num_of_products,
        "HasCrCard": has_cr_card,
        "IsActiveMember": is_active_member,
        "EstimatedSalary": estimated_salary,
        "Geography_Germany": geo_germany,
        "Geography_Spain": geo_spain
    }
    return data

input_data = user_input_features()

# ------------------------------------------------------------------------------
# Main Page: Prediction
# ------------------------------------------------------------------------------

# Show input data summary
st.subheader("Customer Data")
col1, col2, col3 = st.columns(3)
col1.metric("Credit Score", input_data["CreditScore"])
col2.metric("Age", input_data["Age"])
col3.metric("Balance", f"${input_data['Balance']:,.2f}")

# Predict Button
if st.button("🚀 Predict Churn Risk", type="primary"):
    try:
        # Send data to Azure API
        response = requests.post(f"{API_URL}/predict", json=input_data)
        
        if response.status_code == 200:
            result = response.json()
            
            # Display Results
            risk_level = result["risk_level"]
            probability = result["churn_probability"]
            
            st.divider()
            
            if risk_level == "High":
                st.error(f"⚠️ High Risk of Churn ({probability:.1%})")
            elif risk_level == "Medium":
                st.warning(f"⚖️ Medium Risk of Churn ({probability:.1%})")
            else:
                st.success(f"✅ Low Risk of Churn ({probability:.1%})")
                
            st.progress(probability, text="Churn Probability")
            
        else:
            st.error(f"Error {response.status_code}: {response.text}")
            
    except Exception as e:
        st.error(f"Connection Error: {e}")