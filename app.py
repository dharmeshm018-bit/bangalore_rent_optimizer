import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# --- STEP 1: LOAD REAL DATA ---
@st.cache_data
def load_data():
    # 1. Try to Load the Real CSV File
    try:
        df = pd.read_csv("House_Rent_Dataset.csv")
    except FileNotFoundError:
        # Fallback if user forgets the CSV
        st.error("⚠️ Error: 'House_Rent_Dataset.csv' not found. Please download it and put it in the folder.")
        return pd.DataFrame()

    # 2. Filter for just ONE city (Bangalore) to keep the map clean
    # The dataset has Mumbai/Delhi etc, but we want a specific map.
    df = df[df['City'] == 'Bangalore'].copy()
    
    # 3. DATA ENGINEERING: Create Coordinates
    # We map specific Area names to Lat/Long manually since the CSV doesn't have them.
    loc_map = {
        'Koramangala': [12.9345, 77.6186],
        'HSR Layout': [12.9121, 77.6446],
        'Whitefield': [12.9698, 77.7500],
        'Indiranagar': [12.9784, 77.6408],
        'Jayanagar': [12.9304, 77.5855],
        'Marathahalli': [12.9591, 77.6974],
        'Electronic City': [12.8399, 77.6770],
        'BTM Layout': [12.9166, 77.6101],
        'Hebbal': [13.0354, 77.5988],
        'Yelahanka': [13.1007, 77.5963],
        'Bellandur': [12.9260, 77.6762],
        'Sarjapur': [12.9237, 77.6546],
        'Basavanagudi': [12.9438, 77.5755],
        'Malleswaram': [13.0031, 77.5643]
    }
    
    # Function to find coordinates based on the text description
    def get_coords(area_text):
        for key in loc_map:
            if key.lower() in str(area_text).lower():
                # Add random "Jitter" so points don't stack on top of each other
                return loc_map[key][0] + np.random.uniform(-0.01, 0.01), \
                       loc_map[key][1] + np.random.uniform(-0.01, 0.01)
        return np.nan, np.nan # If we can't find the location

    # Apply the coordinate finder
    df['lat'], df['lon'] = zip(*df['Area Locality'].apply(get_coords))
    
    # Drop rows where we couldn't find the location (to prevent map errors)
    df = df.dropna(subset=['lat'])

    # 4. SIMULATE LIFESTYLE DATA
    # Since the Kaggle dataset doesn't have "Cafes" or "Safety", we engineer them 
    # based on the assumption that higher rent = more amenities.
    np.random.seed(42)
    df['Cafes'] = (df['Rent'] / 1500) + np.random.randint(5, 30, size=len(df))
    df['Safety_Score'] = np.random.uniform(6.5, 9.8, size=len(df))
    # Random distance to Metro (0.5km to 10km)
    df['Metro_Dist_KM'] = np.random.uniform(0.5, 10.0, size=len(df))

    return df

# Load the data
df = load_data()

# --- STEP 2: DASHBOARD SETUP ---
st.set_page_config(page_title="Bangalore Rent Optimizer", layout="wide")

st.title("🏡 Bangalore Rent Optimizer")
st.markdown("Use Data Science to find the best 'Value for Money' apartments in Bangalore.")

if df.empty:
    st.stop() # Stop the app if data didn't load

# Sidebar Inputs
st.sidebar.header("Filter Your Preferences")
budget = st.sidebar.slider("Max Budget (₹)", 5000, 100000, 35000)
min_safety = st.sidebar.slider("Minimum Safety Score (1-10)", 1.0, 10.0, 7.0)

st.sidebar.subheader("Priorities")
w_cafe = st.sidebar.slider("Importance of Cafes", 0.0, 1.0, 0.5)
w_metro = st.sidebar.slider("Importance of Metro Proximity", 0.0, 1.0, 0.8)

# --- STEP 3: THE ALGORITHM ---
# Filter first
filtered_df = df[(df['Rent'] <= budget) & (df['Safety_Score'] >= min_safety)].copy()

if not filtered_df.empty:
    # The 'Value Score' Formula
    filtered_df['Value_Score'] = (
        (filtered_df['Cafes'] * w_cafe) + 
        ((1 / filtered_df['Metro_Dist_KM']) * 100 * w_metro)
    ) / (filtered_df['Rent'] / 1000)
    
    # Sort by Best Value
    filtered_df = filtered_df.sort_values(by='Value_Score', ascending=False)
    
    # Display Top Metrics
    col1, col2, col3 = st.columns(3)
    best_match = filtered_df.iloc[0]
    
    col1.metric("Top Recommended Area", best_match['Area Locality'])
    col2.metric("Rent", f"₹{best_match['Rent']}")
    col3.metric("Value Score", f"{best_match['Value_Score']:.2f}")
    
    # --- STEP 4: VISUALIZATION ---
    chart_col, map_col = st.columns([1, 1])
    
    with chart_col:
        st.subheader("💰 Rent vs. Value Analysis")
        fig_scatter = px.scatter(
            filtered_df, 
            x="Rent", 
            y="Value_Score", 
            size="Safety_Score", 
            color="Area Locality",
            hover_data=['BHK', 'Size', 'Metro_Dist_KM'],
            title="Goal: Find High Value (Top) at Low Rent (Left)"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with map_col:
        st.subheader("📍 Interactive Map")
        fig_map = px.scatter_mapbox(
            filtered_df,
            lat="lat",
            lon="lon",
            color="Value_Score",
            size="Rent",
            color_continuous_scale=px.colors.sequential.Viridis,
            zoom=10,
            mapbox_style="open-street-map"
        )
        st.plotly_chart(fig_map, use_container_width=True)

    # Raw Data
    st.subheader("Detailed Listings")
    st.dataframe(filtered_df[['Posted On', 'BHK', 'Rent', 'Area Locality', 'City', 'Furnishing Status', 'Value_Score']])

else:
    st.error(f"No apartments found under ₹{budget} with Safety Score > {min_safety}. Try increasing your budget.")