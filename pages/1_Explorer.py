import streamlit as st
from utils import load_earthquakes

st.title("Explorer")
st.write("Filter recent earthquakes to find the ones that match what you are studying.")

df = load_earthquakes()

# Sidebar: all the filter widgets
st.sidebar.header("Filters")

start = st.session_state.get("min_mag", 2.5)
min_mag = st.sidebar.slider("Minimum magnitude", 2.5, 8.0, float(start), step=0.1)

depth_types = st.sidebar.multiselect(
    "Depth type",
    ["Shallow", "Intermediate", "Deep"],
    default=["Shallow", "Intermediate", "Deep"],
)

search = st.sidebar.text_input("Search by place (for example: Japan, Alaska, Chile)")

sort_by = st.sidebar.selectbox("Sort by (highest first)", ["Magnitude", "Time", "Depth (km)"])

# Apply all the filters together
filtered = df[(df["Magnitude"] >= min_mag) & (df["Depth type"].isin(depth_types))]
if search:
    filtered = filtered[filtered["Place"].str.contains(search, case=False)]
filtered = filtered.sort_values(sort_by, ascending=False)

# Handle the case where nothing matches
if filtered.empty:
    st.warning("No earthquakes match your filters. Try lowering the minimum magnitude, choosing a depth type, or clearing the search.")
    st.stop()

# Summary numbers
col1, col2, col3 = st.columns(3)
col1.metric("Earthquake found", len(filtered))
col2.metric("Strongest", f"{filtered['Magnitude'].max():.1f}")
col3.metric("Average depth", f"{filtered['Depth (km)'].mean():.0f} km")

# Table and map in tabs
tab_table, tab_map = st.tabs(["Table", "Map"])

with tab_table:
    st.dataframe(
        filtered[["Time", "Place", "Magnitude", "Depth (km)", "Depth type"]],
        hide_index=True,
    )

with tab_map:
    st.map(filtered, latitude="Latitude", longitude="Longitude")
