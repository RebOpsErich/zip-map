{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import pandas as pd\
import geopandas as gpd\
import folium\
from streamlit_folium import st_folium\
\
# Title\
st.title("Interactive ZIP Code Coverage Map")\
\
# Load ZIP code list from uploaded file\
uploaded_file = st.file_uploader("Upload your ZIP code CSV", type=["csv"])\
\
if uploaded_file:\
    df = pd.read_csv(uploaded_file)\
    zip_codes = df["ZIP"].astype(str).str.zfill(5).tolist()\
\
    # Load US ZIP code shapefile or GeoJSON (simplified for web)\
    st.markdown("Loading ZIP code boundaries...")\
    zip_geo_url = "https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/il_illinois_zip_codes_geo.min.json"\
    zip_geo = gpd.read_file(zip_geo_url)\
\
    # Filter GeoDataFrame to include only ZIPs in the list\
    filtered_geo = zip_geo[zip_geo['ZCTA5CE10'].isin(zip_codes)]\
\
    # Convert to folium-readable GeoJSON\
    m = folium.Map(location=[41.85, -87.65], zoom_start=9)\
\
    folium.GeoJson(\
        filtered_geo,\
        name="ZIP Code Regions",\
        style_function=lambda feature: \{\
            'fillColor': '#3186cc',\
            'color': 'black',\
            'weight': 1,\
            'fillOpacity': 0.5,\
        \},\
        tooltip=folium.GeoJsonTooltip(fields=["ZCTA5CE10"], aliases=["ZIP Code"])\
    ).add_to(m)\
\
    st_folium(m, width=800, height=600)\
\
    st.success(f"Displayed \{len(filtered_geo)\} ZIP codes from your file.")\
else:\
    st.info("Upload a CSV with a single column named 'ZIP'")}