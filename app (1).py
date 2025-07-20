
import streamlit as st
import pickle
import pandas as pd
import gzip
import json

# Load the compressed models
with gzip.open("job_change_model.pkl.gz", "rb") as f:
    job_model = pickle.load(f)

with gzip.open("salary_growth_model.pkl.gz", "rb") as f:
    salary_model = pickle.load(f)

# Load feature names
with open("feature_list.json", "r") as f:
    feature_list = json.load(f)

st.set_page_config(page_title="Job Change and Salary Predictor")
st.title("Job Change and Salary Prediction Web App")

# Input form
experience = st.slider("Experience (years)", 0.0, 30.0, 2.0, 0.5)
salary = st.number_input("Current Salary (INR)", 100000, 5000000, step=10000)
education_level = st.selectbox("Education Level", ["Graduate", "Masters", "Phd", "High School", "Other"])
company_size = st.selectbox("Company Size", ["<10", "10-49", "50-99", "100-500", "500-999", "1000-4999", "5000-9999", "10000+"])
relevent_experience = st.selectbox("Relevant Experience", ["Yes", "No"])

# Encoding values (These should match the encoding used in the notebook)
edu_map = {"High School": 0, "Graduate": 1, "Masters": 2, "Phd": 3, "Other": 4}
comp_map = {size: i for i, size in enumerate(["<10", "10-49", "50-99", "100-500", "500-999", "1000-4999", "5000-9999", "10000+"])}
rel_exp_map = {"No": 0, "Yes": 1}

if st.button("Predict"):
    # Create input DataFrame with all features, using dummy values for those not in the form
    input_data = {
        'city': 1, # Dummy value
        'city_development_index': 0.8, # Dummy value
        'gender': 1,  # Dummy value
        'relevent_experience': rel_exp_map[relevent_experience],
        'enrolled_university': 0, # Dummy value
        'education_level': edu_map[education_level],
        'major_discipline': 1, # Dummy value
        'company_size': comp_map[company_size],
        'company_type': 1, # Dummy value
        'last_new_job': 1, # Dummy value
        'experience_numeric': experience,
        'current_salary': salary
    }

    input_df = pd.DataFrame([input_data])

    # Ensure the column order matches the training data
    input_df = input_df[feature_list]

    job_change = job_model.predict(input_df)[0]

    if job_change == 1:
        growth = salary_model.predict(input_df)[0]
        new_salary = salary * (1 + growth / 100)
        st.success("This person is likely to change jobs.")
        st.write(f"Estimated Salary Growth: **{growth:.2f}%**")
        st.write(f"New Estimated Salary: ₹{new_salary:,.0f}")
    else:
        st.warning("Unlikely to change jobs.")
