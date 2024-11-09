from streamlit_geolocation import streamlit_geolocation
from streamlit_folium import st_folium

import folium

import requests

import streamlit as st

#สร้างMap
m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
folium.Marker(
    [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)




options = st.multiselect(
    "Select the location of interest",
    ["hospital", "7-11", "department_store", ]
)
delimiter_comma  = ","


st.write(delimiter_comma.join(options))



location = streamlit_geolocation()
st.write(location)
st.write(location['latitude'])
st.write(location['longitude'])
lat = location['latitude']
long = location['longitude']

# Define the URL and parameters
url = f"https://api.longdo.com/POIService/json/search?tag={delimiter_comma.join(options)}&limit=5&span=3000m&lat={lat}&lon={long}&key=547e9ce8c3fd5f20d0e700487c062b06"


# Send the GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    for place in data['data']:
        st.write(place)
else:
    st.write("Error:", response.status_code, response.text)


