
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import requests

st.set_page_config(page_title="ZIP Code Map", layout="wide")
st.title("Interactive ZIP Code Coverage Map")

uploaded_file = st.file_uploader("Upload your cleaned ZIP code CSV (with column 'ZIP')", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    zip_codes = df['ZIP'].astype(str).str.zfill(5).tolist()

    # Load simplified US ZIP code GeoJSON (IL example)
    url = "https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/il_illinois_zip_codes_geo.min.json"
    geojson_data = requests.get(url).json()

    # Filter GeoJSON to include only ZIPs in uploaded list
    filtered_features = [f for f in geojson_data['features'] if f['properties']['ZCTA5CE10'] in zip_codes]
    filtered_geojson = {"type": "FeatureCollection", "features": filtered_features}

    # Build map
    m = folium.Map(location=[41.85, -87.65], zoom_start=9)
    folium.GeoJson(
        filtered_geojson,
        name="Filtered ZIPs",
        style_function=lambda feature: {
            'fillColor': '#ff7800',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6,
        },
        tooltip=folium.GeoJsonTooltip(fields=["ZCTA5CE10"], aliases=["ZIP Code"])
    ).add_to(m)

    st_folium(m, width=1000, height=600)
    st.success(f"Plotted {len(filtered_features)} ZIP code areas.")
else:
    st.info("Upload a CSV with a column named 'ZIP' to begin.")
