import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

import requests
import time
from datetime import datetime, timedelta
import json

st.title('Nacasky Air Quality Dashboard')

def authenticate_and_request(APITocken, APPType, request_body):
    # API endpoint URL (replace with the actual API endpoint)
    api_url = 'https://echt.seelive.io/API/DataAI/API_GetSensorData'

    # Construct headers with authentication tokens
    headers = {
        'Authorization': f'Bearer {APITocken}',
        'APITocken': APITocken,
        'APPType': APPType
    }

    try:
        # Send POST request to the API with request body
        response = requests.post(api_url, headers=headers, json=request_body)

        # Check for successful response (status code 200)
        if response.status_code == 200:
            data = response.json()  # Assuming the API returns JSON data
            print('API Response:')
            return (data)
#             return data_dictionary.update(data)
        else:
            print(f'Error: HTTP Status Code {response.status_code}')
            print(response.text)  # Print the response content for debugging

    except Exception as e:
        print(f'Error: {e}')


#--------------------------------------------------------------------------------------------
APITocken='Rth-0987u-wert-3456'
APPType='AIUSER'

# # Define the start and end date strings------------------------------------------------------
# start_date = datetime(2023, 7, 1, 0, 0)
# end_date = datetime(2023, 8, 31, 23, 59)

# Create a container for horizontal layout
col1, col2 = st.columns(2)

# Date input widgets in the first column
with col1:
    start_date = st.date_input("Select Start Date", value=datetime(2023, 7, 1))
    end_date = st.date_input("Select End Date", value=datetime(2023, 7, 31))

# Time input widgets in the second column
with col2:
    start_time = st.time_input("Select Start Time", value=datetime(2023, 7, 1, 0, 0))
    end_time = st.time_input("Select End Time", value=datetime(2023, 7, 31, 23, 59))

# Combine the selected date and time into datetime objects using np.array
start_datetime = np.array(datetime.combine(start_date, start_time))
end_datetime = np.array(datetime.combine(end_date, end_time))

# Define a custom datetime format-----------------------------------------------------------
custom_format = "%d-%b-%Y %I:%M %p"

# @st.cache_data
def fetch_data_for_month():
    print(1)
    # Format the datetime objects using the custom format
    start_date_str = start_date.strftime(custom_format)
    end_date_str = end_date.strftime(custom_format)
    
    print(start_date_str)
    print(end_date_str)

    request_body =  {
    "SensorID":"ENE02368",
     "FromDate":start_date_str,
     "ToDate":end_date_str,
     "DataInteval":1,
     "DataType":"R"
    }
    
    July_data = authenticate_and_request(APITocken, APPType, request_body)
    Sensor_Data_July = July_data['SearchDetail']
    print(Sensor_Data_July[0])
    df_july_one = pd.DataFrame(Sensor_Data_July)
    df_july_one['DataDate'] = pd.to_datetime(df_july_one['DataDate'])
    df_july_two = df_july_one.loc[:, (df_july_one != 0).any(axis=0)]
    print(df_july_two.head())
    return df_july_two

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading graph...')

# Load 10,000 rows of data into the dataframe.
data = fetch_data_for_month()

# Create a download button to download the displayed data as CSV
# st.subheader('Raw data')
# st.write(data)

# Notify the reader that the data was successfully loaded.
# data_load_state.text("Done!")

# csv_data = data.to_csv(index=False).encode()
# st.download_button(
#     label="Download Data as CSV",
#     data=csv_data,
#     file_name="data_july_ENE02368.csv",
#     mime="text/csv"
# )


# Streamlit app title
# st.subheader('Time Series Plot with PM2.5')

# with st.spinner('Wait for it...'):
#     time.sleep(1)

# Create a time series plot using Plotly Express
fig = px.line(data, x='DataDate', y='PM2_5', title='PM2.5 Time Series')
fig.update_xaxes(title_text='Date and Time')
fig.update_yaxes(title_text='PM2.5 Value')

# Display the time series plot in Streamlit
st.plotly_chart(fig)


