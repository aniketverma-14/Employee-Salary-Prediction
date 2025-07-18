import streamlit as st
import pandas as pd
import pickle
import gzip
import json

# Load model
with gzip.open("job_change_model.pkl.gz", "rb") as f:
    model = pickle.load(f)

# Load feature list
with open("feature_list.json", "r") as f:
    expected_features = json.load(f)

# App UI
st.title("Job Change Prediction Web App")

# Inputs
education = st.selectbox("Education Level", ['High School', 'Graduate', 'Masters', 'Phd'])
re = st.selectbox("Relevant Experience", ['No', 'Yes'])
company_size = st.selectbox("Company Size", ['<10', '10-49', '50-99', '100-500', '500-999', '1000-4999', '5000-9999', '10000+'])
exp = st.slider("Years of Experience", 0, 30, 2)
salary = st.number_input("Current Salary (INR)", 100000, 5000000, step=10000)

# Encoding
edu_map = {'High School': 0, 'Graduate': 1, 'Masters': 2, 'Phd': 3}
re_map = {'No': 0, 'Yes': 1}
comp_map = {'<10': 0, '10-49': 1, '50-99': 2, '100-500': 3, '500-999': 4, '1000-4999': 5, '5000-9999': 6, '10000+': 7}

input_data = {
    'education_level': edu_map[education],
    'relevent_experience': re_map[re],
    'company_size': comp_map[company_size],
    'experience_numeric': exp,
    'current_salary': salary
}

# Ensure column order matches model's training
input_df = pd.DataFrame([input_data])
input_df = input_df.reindex(columns=expected_features)  # 🔥 Critical line

# Predict
if st.button("Predict"):
    prediction = model.predict(input_df)[0]
    if prediction == 1:
        st.success("Likely to change job")
    else:
        st.warning("Unlikely to change job")
