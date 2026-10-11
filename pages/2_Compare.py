import pandas as pd
import streamlit as st
from utils import load_earthquakes

st.title("Compare")
st.write("See how earthquakes of different strengths compare.")

df = load_earthquakes()

# Use the magnitude chosen on the Home page
min_mag = st.session_state.get("min_mag", 2.5)
st.info(f"Showing earthquake of magnitude {min_mag} and above (chosen on the Home page).")

filtered = df[df["Magnitude"] >= min_mag]

# Handle the case where nothing matches
if filtered.empty:
    st.warning("No earthquakes at this strength. Go back to the Home page and choose a lower magnitude.")
    st.stop()

# Sort each earthquake into a strength band
bands = pd.cut(
    filtered["Magnitude"],
    bins=[2.5, 3, 4, 5, 6, 11],
    labels=["2.5-2.9", "3.0-3.9", "4.0-4.9", "5.0-5.9", "6.0+"],
    right=False,
)

# Group by band: count and average depth
counts = filtered.groupby(bands, observed=True).size()
avg_depth = filtered.groupby(bands, observed=True)["Depth (km)"].mean().round(0)

# Two charts side by side
col1, col2 = st.columns(2)

with col1:
    st.subheader("How many?")
    st.bar_chart(counts)
    st.caption("Number of earthquakes in each magnitude band.")

with col2:
    st.subheader("How deep, on average?")
    st.bar_chart(avg_depth)
    st.caption("Average depth in km for each magnitude band.")

    