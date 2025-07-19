
import streamlit as st
import pickle
import pandas as pd

import gzip
with gzip.open("job_change_model.pkl.gz", "rb") as f:
    model = pickle.load(f)

st.title("Salary Prediction Web App")

experience = st.slider("Years of Experience", 0, 30, 2)

if st.button("Predict Salary"):
    df = pd.DataFrame([[experience]], columns=["experience"])
    prediction = model.predict(df)[0]
if prediction == 1:
    st.success("This person is likely to change jobs.")
else:
    st.warning("This person is not likely to change jobs.")
