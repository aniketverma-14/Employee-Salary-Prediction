
import streamlit as st
import pickle
import pandas as pd

import gzip
with gzip.open("job_change_model.pkl.gz", "rb") as f:
    model = pickle.load(f)

st.set_page_config(page_title="Salary Predictor")
st.title("Salary Prediction Web App")

experience = st.slider("Years of Experience", 0, 30, 2)

if st.button("Predict Salary"):
    df = pd.DataFrame([[experience]], columns=["experience"])
    prediction = model.predict(df)[0]
    st.success(f"Estimated Salary: ₹{int(prediction[0]):,}")
