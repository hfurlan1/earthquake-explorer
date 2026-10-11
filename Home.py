import streamlit as st

# Sets browser tab title and icon
st.set_page_config(page_title="Earthquake Explorer", page_icon="🌍")

st.title("Earthquake Explorer")
st.write("Explore the world's recent earthquakes, from the USGS live feed.")

# Problem statement section
st.header("Problem statement")
st.write("**Who is this for?** Students and curious learners studying geography and earth science.")
st.write("**What problem do they face?** Earthquake data is published as raw feeds. It is hard to see where recent quakes happened, how strong they were, and how deep.")
st.write("**Why does it matter?** Spotting patters in real earthquakes builds intuition about plate boundaries and natural hazards.")

# Why these pages? section
st.header("Why these pages?")
st.write("**Explorer:** answers 'which earthquakes match what I am studying' with filters.")
st.write("**Compare:** answers 'how do quakes of different strenghts compare?' with a chart.")

# List of choices in the selectbox
st.header("Start here")
options = [2.5, 3.0, 4.0, 5.0]
saved = st.session_state.get("min_mag", 2.5)
choice = st.selectbox(
    "What is the weakest earthquake you want to see (magnitude)?",
    options,
    index=options.index(saved),
)
st.session_state["min_mag"] = choice

# Shows confirmation box
st.success(f"Saved. The other pages will start at magnitude {choice} and above.")
st.caption("Data: USGS Earthquake Hazards Program, earthquakes of magnitude 2.5 and above from the past 30 days.")
