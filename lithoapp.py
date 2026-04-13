import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 1. PAGE CONFIG & UI STYLING ---
st.set_page_config(page_title="VLSI Process Simulator", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #e0e0e0; }
    section[data-testid="stSidebar"] { background-color: #1e1e1e !important; border-right: 1px solid #333; width: 320px !important; }
    div[data-testid="stMetricValue"] { font-size: 24px !important; color: #ffffff !important; text-align: center; }
    div[data-testid="stMetricLabel"] { font-size: 11px !important; text-transform: uppercase; color: #888 !important; text-align: center; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #1e1e1e; border: 1px solid #333; border-radius: 4px; color: white; padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { background-color: #0056b3 !important; border-color: #0056b3 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR PARAMETERS ---
with st.sidebar:
    st.markdown("### 🛠️ SUBSTRATE & RESIST")
    sub_type = st.selectbox("Substrate", ["Silicon", "SOI", "GaAs"])
    res_type = st.selectbox("Resist Type", ["Positive", "Negative"])
    thickness = st.slider("Resist Thickness (nm)", 100, 800, 400)
    
    st.markdown("---")
    st.markdown("### 💡 EXPOSURE SETTINGS")
    mask_pattern = st.selectbox("Mask Pattern", ["Lines/Spaces", "Contact Hole", "Isolated Line"])
    wl = st.selectbox("Wavelength", [365, 248, 193, 13], format_func=lambda x: f"{x} nm")
    na = st.slider("Numerical Aperture", 0.30, 1.35, 0.85)
    dose = st.slider("Dose (mJ/cm²)", 5, 100, 30)
    
    st.markdown("---")
    run_sim = st.button("🚀 Run Simulation")

# --- 3. MAIN INTERFACE ---
st.title("Virtual lithography visualizer with process parameters")
st.write(f"Hello Aashna! This simulation follows the core photolithography steps: Coating, Exposure, and Development.")

# Sequential Tabs to show "After each step"
tab1, tab2, tab3 = st.tabs(["Step 1: Resist Coating", "Step 2: Exposure", "Step 3: Development"])

# --- 4. CALCULATIONS ---
k1 = 0.4
cd = (k1 * wl) / na
dof = (0.5 * wl) / (na**2)
x = np.linspace(-500, 500, 1000)

if run_sim:
    # --- STEP 1: COATING ---
    with tab1:
        st.write("### After Coating & Softbake")
        fig1, ax1 = plt.subplots(figsize=(10, 3), facecolor='#121212')
        ax1.set_facecolor('#121212')
        # Substrate
        ax1.add_patch(plt.Rectangle((-500, -50), 1000, 50, color='#2c3e50'))
        # Uniform Resist Layer
        ax1.add_patch(plt.Rectangle((-500, 0), 1000, thickness/2, color='orange', alpha=0.6))
        ax1.set_xlim(-500, 500)
        ax1.set_ylim(-60, 450)
        ax1.axis('off')
        st.pyplot(fig1)
        st.info("A uniform layer of photoresist has been applied via spin-coating and hardened with a Softbake.")

    # --- STEP 2: EXPOSURE ---
    with tab2:
        st.write("### During Exposure (Aerial Image)")
        fig2, ax2 = plt.subplots(figsize=(10, 3), facecolor='#121212')
        ax2.set_facecolor('#121212')
        
        # Modeling the intensity pattern
        intensity = np.abs(np.sinc(x * na / (wl/2)))**2 if mask_pattern != "Isolated Line" else np.exp(-x**2/(2*cd**2))
        ax2.plot(x, intensity * 300, color='cyan', lw=2, label="Light Intensity")
        ax2.fill_between(x, 0, intensity * 300, color='cyan', alpha=0.2)
        
        # Substrate/Resist indicators
        ax1.add_patch(plt.Rectangle((-500, -50), 1000, 50, color='#2c3e50'))
        ax2.set_xlim(-500, 500)
        ax2.set_ylim(-60, 450)
        ax2.axis('off')
        st.pyplot(fig2)
        st.warning(f"UV light at {wl}nm passes through the {mask_pattern} mask, creating a chemical change in the resist.")

    # --- STEP 3: DEVELOPMENT ---
    with tab3:
        st.write("### After Development (Final Pattern)")
        fig3, ax3 = plt.subplots(figsize=(10, 3), facecolor='#121212')
        ax3.set_facecolor('#121212')
        ax3.add_patch(plt.Rectangle((-500, -50), 1000, 50, color='#2c3e50'))
        
        # Logic for Positive/Negative resist removal
        threshold = 0.5
        profile = np.where(intensity < threshold, thickness/2, 0) if res_type == "Positive" else np.where(intensity > threshold, thickness/2, 0)
        ax3.fill_between(x, 0, profile, color='orange', step="mid")
        
        ax3.set_xlim(-500, 500)
        ax3.set_ylim(-60, 450)
        ax3.axis('off')
        st.pyplot(fig3)
        st.success(f"The developer solution has removed the {'exposed' if res_type=='Positive' else 'unexposed'} regions.")

    # --- METRICS SECTION ---
    st.divider()
    m1, m2, m3 = st.columns(3)
    with m1: st.metric("Critical Dimension", f"{cd:.0f} nm")
    with m2: st.metric("Depth of Focus", f"{dof:.0f} nm")
    with m3: st.metric("Process Status", "Pass" if dof > 100 else "Warning")

else:
    st.info("👈 Adjust the sidebar and click **Run Simulation** to see the process steps.")
