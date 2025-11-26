# bangalore_rent_optimizer
🏡 A Data Science dashboard that helps freshers optimize housing choices by calculating a custom "Livability Score" based on rent, safety, and commute data.
# 🏡 Smart Rent Optimizer (Bangalore Edition)

### 📊 Project Overview
Finding an apartment in a major tech city like Bangalore is a struggle between **Budget** vs. **Quality of Life**. Most platforms only sort by price. 
This project introduces a **"Value Score" algorithm** that weighs amenities (Cafes, Safety) against Rent and Commute distance to identify "Hidden Gem" neighborhoods for young professionals.

**🔴 Live Demo:** [Insert your Streamlit Link Here]

---

### 💡 The Business Problem
* **The Issue:** Low rent often means poor safety or 2+ hours of travel time.
* **The Solution:** An interactive dashboard that allows users to define their own priorities (e.g., "I care more about Safety than Metro proximity") and visualizes the best trade-offs on a map.

### 🛠️ Tech Stack
* **Python 3.9**
* **Streamlit:** For the interactive web interface.
* **Pandas:** For data cleaning and vectorized score calculation.
* **Plotly:** For geospatial mapping and scatter plot analysis.
* **NumPy:** For statistical operations.

### 🧠 The "Value Score" Logic
I engineered a custom metric to rank neighborhoods:

$$\text{Score} = \frac{(\text{Cafe Count} \times W_1) + (\text{Metro Proximity} \times W_2)}{\text{Rent}}$$

*Where $W$ represents user-defined weights customized via the sidebar sliders.*

---

### 🚀 How to Run Locally
1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/bangalore-rent-optimizer.git](https://github.com/YOUR_USERNAME/bangalore-rent-optimizer.git)
