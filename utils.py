import pandas as pd
import requests
import streamlit as st

URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.geojson"


# Makes streamlit remember the result, so API is only called once
@st.cache_data

# Function with no inputs: any page can call it
def load_earthquakes():
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    data = response.json()

    rows = []
    # Loops each earthquake, one at a time
    for quake in data["features"]:
        rows.append({
            "Place": quake["properties"]["place"],
            "Magnitude": quake["properties"]["mag"],
            "Time": quake["properties"]["time"],
            "Longitude": quake["geometry"]["coordinates"][0],
            "Latitude": quake["geometry"]["coordinates"][1],
            "Depth (km)": quake["geometry"]["coordinates"][2],
        })

    df = pd.DataFrame(rows)

    # Removes any rows missing info, which could cause errors
    df = df.dropna(subset=["Place", "Magnitude"])

    df["Time"] = pd.to_datetime(df["Time"], unit="ms")

    # Sorts each depth in to a bucket
    df["Depth type"] = pd.cut(
        df["Depth (km)"],
        bins=[-100, 70, 300, 1000],
        labels=["Shallow", "Intermediate", "Deep"],
    ).astype(str)
    return df