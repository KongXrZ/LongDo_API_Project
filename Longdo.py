import folium
import requests
import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from streamlit_folium import st_folium

class LocationMap:
    def __init__(self, api_key):
        self.api_key = api_key
        self.lat = None
        self.long = None
        self.location = None
        self.map = None

    def get_location(self):
        """Retrieve user location from the device."""
        self.location = streamlit_geolocation()
        if self.location and self.location.get('latitude') is not None and self.location.get('longitude') is not None:
            self.lat = self.location['latitude']
            self.long = self.location['longitude']
            st.write(f"Latitude: {self.lat}, Longitude: {self.long}")
            return True
        else:
            st.write("Unable to retrieve location data from the device. Please ensure location access is enabled.")
            return False

    def create_map(self):
        """Create a Folium map centered on the user's location."""
        if self.lat is not None and self.long is not None:
            self.map = folium.Map(location=[self.lat, self.long], zoom_start=16)
            # Set user's marker color to red using Icon
            folium.Marker([self.lat, self.long], 
                          popup="Your Location", 
                          tooltip="Your Location", 
                          icon=folium.Icon(color='red')).add_to(self.map)
        else:
            st.write("Map could not be created due to missing location data.")

    def add_location_markers(self, options):
        """Add markers to the map based on selected location types."""
        if options and self.lat is not None and self.long is not None:
            # Construct the URL for the Longdo POI Service API
            url = f"https://api.longdo.com/POIService/json/search?tag={','.join(options)}&limit=5&span=3000m&lat={self.lat}&lon={self.long}&key={self.api_key}"

            # Send the GET request to Longdo API
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()

                # Debugging: Show raw API response if needed
                st.write("API Response:", data)

                # Add markers for each place on the map
                for place in data['data']:
                    folium.Marker(
                        [place['lat'], place['lon']], 
                        popup=place['name'],
                        tooltip=place['name']
                    ).add_to(self.map)

            else:
                st.write("Error:", response.status_code, response.text)
        else:
            st.write("No location types selected or invalid location data.")

    def display_map(self):
        """Render the Folium map in Streamlit."""
        if self.map:
            st_folium(self.map, width=725)
        else:
            st.write("Map is not available. Please check location or markers.")

# Set up your Longdo API key
LONGDO_API_KEY = "547e9ce8c3fd5f20d0e700487c062b06"

# Instantiate the LocationMap class
location_map = LocationMap(LONGDO_API_KEY)

# Get location and create map
if location_map.get_location():
    location_map.create_map()

    # Multi-select options for location types
    options = st.multiselect(
        "Select the location of interest",
        ["hospital", "7-11", "department_store", "temple"]
    )

    st.write("Selected categories:", ",".join(options))

    # Add markers if options are selected
    if options:
        location_map.add_location_markers(options)

    # Display the map
    location_map.display_map()
else:
    st.write("Unable to proceed without location data.")
