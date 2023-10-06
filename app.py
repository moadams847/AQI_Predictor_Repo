import streamlit as st
import joblib
import pandas as pd

# Load the saved model
model = joblib.load('linear_regression_model.pkl')

# Create a Streamlit app
st.title('AQI Predictor for sensor ENE02360')

# Input form for user to enter features
st.header('Input Features')

feature1 = st.number_input('PM2_5', value=4.0)
feature2 = st.number_input('PM10', value=4.0)


# Make predictions
if st.button('Predict'):
    input_data = pd.DataFrame({
        'PM2_5': [feature1],
        'PM10': [feature2]
    })
    prediction = model.predict(input_data)
    st.header('Prediction')
    st.write(f'The predicted AQI for sensor ENE02360 is : {prediction[0]:.2f}')
