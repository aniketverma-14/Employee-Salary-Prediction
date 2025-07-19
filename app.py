
import streamlit as st
import pickle
import pandas as pd

import gzip
with gzip.open("job_change_model.pkl.gz", "rb") as f:
    model = pickle.load(f)

st.title("Salary Prediction Web App")

experience = st.slider("Years of Experience", 0, 30, 2)
current_salary = st.number_input("Current Salary (INR)", 100000, 5000000, step=10000)
relevent_experience = st.selectbox("Relevant Experience", ["Yes", "No"])
education_level = st.selectbox("Education Level", ["Graduate", "Masters", "Phd", "High School", "Other"])
company_size = st.selectbox("Company Size", ["<10", "10-49", "50-99", "100-500", "500-999", "1000-4999", "5000-9999", "10000+"])

# Dummy encoded values (you should use LabelEncoder mappings from training)
re_map = {"No": 0, "Yes": 1}
edu_map = {"High School": 0, "Graduate": 1, "Masters": 2, "Phd": 3, "Other": 4}
comp_map = {s: i for i, s in enumerate(["<10", "10-49", "50-99", "100-500", "500-999", "1000-4999", "5000-9999", "10000+"])} 

# Build input row
input_data = {
    'gender': 1,  # default dummy
    'relevent_experience': re_map[relevent_experience],
    'enrolled_university': 0,
    'education_level': edu_map[education_level],
    'major_discipline': 1,
    'company_size': comp_map[company_size],
    'company_type': 1,
    'last_new_job': 1,
    'city': 1,
    'experience_numeric': experience_numeric,
    'current_salary': current_salary
}

input_df = pd.DataFrame([input_data])

if st.button("Predict"):
    prediction = model.predict(input_df)[0]
if prediction == 1:
    st.success("This person is likely to change jobs.")
else:
    st.warning("This person is not likely to change jobs.")
