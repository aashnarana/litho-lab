import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 1. PAGE CONFIG & DARK UI ---
st.set_page_config(page_title="Full Cycle Lithography Lab", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #1e1e1e !important; border-right: 1px solid #333; }
    .stTabs [data-baseweb="tab-list"] { gap: 4px; }
    .stTabs [data-baseweb="tab"] { background-color: #1e1e1e; border: 1px solid #333; border-radius: 4px; color: #888; font-size: 12px; }
    .stTabs [aria-selected="true"] { background-color: #0056b3 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR: PROCESS PARAMETERS ---
with st.sidebar:
    st.write("### ⚙️ PARAMETERS")
    sub_mat = st.selectbox("Substrate", ["Silicon", "SOI"])
    target_mat = st.selectbox("Target Material (Layer)", ["SiO2", "Polysilicon", "Metal"])
    res_type = st.selectbox("Resist Type", ["Positive", "Negative"])
    
    st.divider()
    wl = st.selectbox("Wavelength", [365, 248, 193, 13], index=2)
    na = st.slider("NA", 0.3, 1.35, 0.85)
    
    st.divider()
    run_sim = st.button("🚀 RUN FULL PROCESS")

# --- 3. MAIN HEADER ---
st.write("# Lithography Process Simulation")
st.write("Visualizing the 9-step fabrication cycle.")

# --- 4. STEP-BY-STEP TABS (Matches Image_0c9989.jpg) ---
tabs = st.tabs([
    "1. Cleaning", "2. Prime/Coat", "3. Softbake", 
    "4. Exposure", "5. PEB/Dev", "6. Etching", "7. Stripping"
])

# --- 5. SIMULATION LOGIC ---
if run_sim:
    # Calculations
    k1 = 0.4
    cd = (k1 * wl) / na
    x = np.linspace(-500, 500, 1000)
    intensity = np.abs(np.sinc(x * na / (wl/2)))**2
    threshold = 0.5
    
    # helper for drawing layers
    def draw_base(ax):
        ax.set_facecolor('#121212')
        ax.add_patch(plt.Rectangle((-500, -50), 1000, 50, color='#8B0000', label="Substrate")) # Red Substrate
        ax.set_xlim(-500, 500)
        ax.set_ylim(-60, 300)
        ax.axis('off')

    # STEP 1: CLEANING & DEPOSITION
    with tabs[0]:
        fig1, ax1 = plt.subplots(figsize=(10, 2), facecolor='#121212')
        draw_base(ax1)
        ax1.add_patch(plt.Rectangle((-500, 0), 1000, 30, color='#008B8B', label="Target Material")) # Teal Layer
        st.pyplot(fig1)
        st.info("**Step 1-2:** Wafer is cleaned and the Target Material (e.g., Oxide) is deposited.")

    # STEP 2-3: COATING & SOFTBAKE
    with tabs[1]:
        fig2, ax2 = plt.subplots(figsize=(10, 2), facecolor='#121212')
        draw_base(ax2)
        ax2.add_patch(plt.Rectangle((-500, 0), 1000, 30, color='#008B8B')) 
        ax2.add_patch(plt.Rectangle((-500, 30), 1000, 40, color='#CCCC00', alpha=0.8, label="Resist")) # Yellow Resist
        st.pyplot(fig2)
        st.info("**Step 3-5:** Wafer priming and Photo-resist coating followed by Soft-baking.")

    # STEP 4: EXPOSURE
    with tabs[3]:
        fig3, ax3 = plt.subplots(figsize=(10, 2), facecolor='#121212')
        draw_base(ax3)
        ax3.add_patch(plt.Rectangle((-500, 0), 1000, 30, color='#008B8B'))
        ax3.add_patch(plt.Rectangle((-500, 30), 1000, 40, color='#CCCC00', alpha=0.4))
        # Light Beams
        for i in range(-450, 500, 200):
            ax3.annotate('', xy=(i, 30), xytext=(i, 150), arrowprops=dict(arrowstyle='->', color='red'))
        st.pyplot(fig3)
        st.warning("**Step 6:** Exposure through the mask. UV light creates a latent image in the resist.")

    # STEP 5: DEVELOPMENT
    with tabs[4]:
        fig4, ax4 = plt.subplots(figsize=(10, 2), facecolor='#121212')
        draw_base(ax4)
        ax4.add_patch(plt.Rectangle((-500, 0), 1000, 30, color='#008B8B'))
        # Resist Pattern
        res_profile = np.where(intensity < threshold, 40, 0) if res_type == "Positive" else np.where(intensity > threshold, 40, 0)
        ax4.fill_between(x, 30, 30 + res_profile, color='#808080', step="mid") # Grey developed resist
        st.pyplot(fig4)
        st.success("**Step 7 & 9:** Development removes soluble resist, leaving the pattern.")

    # STEP 6: ETCHING
    with tabs[5]:
        fig5, ax5 = plt.subplots(figsize=(10, 2), facecolor='#121212')
        draw_base(ax5)
        # Etched Target Material (Only stays under resist)
        etch_profile = np.where(res_profile > 0, 30, 0)
        ax5.fill_between(x, 0, etch_profile, color='#008B8B', step="mid")
        # Keep Resist on top
        ax5.fill_between(x, 30, 30 + res_profile, color='#808080', step="mid", alpha=0.5)
        st.pyplot(fig5)
        st.error("**Step 8:** Etching. The chemicals remove the target material NOT protected by resist.")

    # STEP 7: STRIPPING
    with tabs[6]:
        fig6, ax6 = plt.subplots(figsize=(10, 2), facecolor='#121212')
        draw_base(ax6)
        # Only the Target Pattern remains
        ax6.fill_between(x, 0, etch_profile, color='#008B8B', step="mid")
        st.pyplot(fig6)
        st.info("**Final Step:** Resist Strip. The photoresist is removed, leaving the final etched pattern.")

    # --- METRICS GRID ---
    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("Resolution (CD)", f"{cd:.1f} nm")
    m2.metric("Etch Selectivity", "High")
    m3.metric("Yield Estimate", "98%")

else:
    st.info("Click **Run Full Process** to begin the fabrication cycle.")
