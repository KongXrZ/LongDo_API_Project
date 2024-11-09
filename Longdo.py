from streamlit_geolocation import streamlit_geolocation
from streamlit_folium import st_folium
import folium
import requests
import streamlit as st

# Set up your Longdo API key
LONGDO_API_KEY = "547e9ce8c3fd5f20d0e700487c062b06"

# Get user location from the device
location = streamlit_geolocation()

# Ensure that location data exists
if location and location.get('latitude') is not None and location.get('longitude') is not None:
    lat = location['latitude']
    long = location['longitude']
    st.write(f"Latitude: {lat}, Longitude: {long}")

    # Create a Folium map centered on the user's location
    m = folium.Map(location=[lat, long], zoom_start=16)
    folium.Marker(
        [lat, long], popup="Your Location", tooltip="Your Location"
    ).add_to(m)

    # Multi-select options for location types
    options = st.multiselect(
        "Select the location of interest",
        ["hospital", "7-11", "department_store"]
    )
    delimiter_comma = ","
    st.write("Selected categories:", delimiter_comma.join(options))

    # If options are selected, query Longdo API with the user’s location
    if options:
        # Construct the URL for the Longdo POI Service API
        url = f"https://api.longdo.com/POIService/json/search?tag={delimiter_comma.join(options)}&limit=5&span=3000m&lat={lat}&lon={long}&key={LONGDO_API_KEY}"
        
        # Send the GET request to Longdo API
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            
            # Debugging: Show raw API response if needed
            st.write("API Response:", data)     #เช็คไฟล์์JSON
            
            # Add markers for each place on the map
            for place in data['data']:
                folium.Marker(
                    [place['lat'], place['lon']], 
                    popup=place['name'],
                    tooltip=place['name']
                ).add_to(m)
            # Update the map with new markers
            st_data = st_folium(m, width=725)
        else:
            st.write("Error:", response.status_code, response.text)
    else:
        # Render initial map if no options selected
        st_data = st_folium(m, width=725)
        st.write("Please select at least one location type to display nearby places.")
else:
    st.write("Unable to retrieve location data from the device. Please ensure location access is enabled.")