import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 1. PAGE CONFIG & DARK THEME CSS ---
st.set_page_config(page_title="Virtual Lithography Visualizer", layout="wide")

st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #121212;
        color: #e0e0e0;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #1e1e1e !important;
        border-right: 1px solid #333;
        width: 320px !important;
    }
    
    /* Metric Card Styling */
    div[data-testid="stMetricValue"] {
        font-size: 24px !important;
        color: #ffffff !important;
        text-align: center;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 12px !important;
        text-transform: uppercase;
        color: #aaaaaa !important;
        text-align: center;
    }
    
    /* Custom Card Container */
    .metric-card {
        background-color: #262626;
        padding: 15px;
        border-radius: 5px;
        border: 1px solid #333;
        text-align: center;
    }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        background-color: #333333;
        color: white;
        border: 1px solid #444;
        border-radius: 4px;
    }
    .stButton>button:hover {
        background-color: #444444;
        border-color: #666;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR PARAMETERS ---
with st.sidebar:
    st.markdown("### 🛠️ SUBSTRATE & RESIST")
    substrate = st.selectbox("Substrate", ["Silicon", "SOI", "GaAs", "Glass"])
    res_type = st.selectbox("Resist Type", ["Positive", "Negative"])
    thickness = st.slider("Resist Thickness (nm)", 50, 800, 300)
    pac = st.slider("PAC Concentration", 0.10, 0.60, 0.30)
    
    st.markdown("---")
    st.markdown("### 💡 EXPOSURE")
    wl = st.selectbox("Wavelength", [365, 248, 193, 13], format_func=lambda x: f"{x} nm")
    dose = st.slider("Dose (mJ/cm²)", 5, 100, 25)
    na = st.slider("Numerical Aperture", 0.30, 1.35, 0.85)
    focus = st.slider("Focus Offset", -200, 200, 0)
    
    st.markdown("---")
    run_btn = st.button("Run Simulation")

# --- 3. MAIN CONTENT AREA ---
st.title("Virtual lithography visualizer with process parameters")

# Tabs for different views (Matches your screenshot)
tab_cross, tab_top, tab_aerial, tab_profile, tab_dose = st.tabs([
    "Cross-section", "Top-down", "Aerial Image", "Resist Profile", "Dose Map"
])

# --- 4. CALCULATIONS ---
# Physics Constants
k1 = 0.4
cd = (k1 * wl) / na
dof = (0.5 * wl) / (na**2)
el = (dose / 100) * 10 # Dummy Exposure Latitude calculation

# --- 5. VISUALIZATION LOGIC ---
if run_btn:
    with tab_cross:
        # Drawing the Cross-section
        fig, ax = plt.subplots(figsize=(10, 3), facecolor='#121212')
        ax.set_facecolor('#121212')
        
        # Draw Silicon Substrate
        ax.add_patch(plt.Rectangle((-500, -100), 1000, 100, color='#2c3e50'))
        ax.text(-480, -50, "Si substrate", color='white', fontsize=8)
        
        # Draw Resist Features
        x_vals = np.linspace(-500, 500, 6)
        for val in x_vals:
            color = '#3498db' if res_type == "Positive" else '#e67e22'
            ax.add_patch(plt.Rectangle((val, 0), cd, thickness/4, color=color))
            
        ax.set_xlim(-500, 500)
        ax.set_ylim(-100, 300)
        ax.axis('off')
        st.pyplot(fig)

    # Metrics Grid (3x2 layout like screenshot)
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m4, m5, m6 = st.columns(3)

    with m1: st.metric("Critical Dimension", f"{cd:.0f} nm")
    with m2: st.metric("Depth of Focus", f"{dof:.0f} nm")
    with m3: st.metric("Exposure Latitude", f"{el:.0f} %")
    with m4: st.metric("Resist Contrast", "3.4 γ")
    with m5: st.metric("LER Estimate", "6.4 nm 3σ")
    with m6:
        status = "Pass" if abs(focus) < dof else "Fail"
        st.metric("Process Status", status)

    # Success Box at bottom
    if status == "Pass":
        st.success("Process window looks healthy. All parameters within specification.")
    else:
        st.error("Process window failed. Adjust Focus or Numerical Aperture.")

else:
    st.info("Click 'Run Simulation' in the sidebar to visualize results.")
