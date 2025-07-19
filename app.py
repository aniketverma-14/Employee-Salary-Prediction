
import streamlit as st
import pickle
import pandas as pd

model = pickle.load(open("model.pkl", "rb"))

st.set_page_config(page_title="Salary Predictor")
st.title("Salary Prediction Web App")

experience = st.slider("Years of Experience", 0, 30, 2)

if st.button("Predict Salary"):
    df = pd.DataFrame([[experience]], columns=["experience"])
    prediction = model.predict(df)
    st.success(f"Estimated Salary: ₹{int(prediction[0]):,}")
