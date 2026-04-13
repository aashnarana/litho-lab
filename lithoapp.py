import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="Pro Litho Lab", layout="wide")

# --- CUSTOM CSS FOR HIERARCHY ---
st.markdown("""
    <style>
    h1 { font-size: 3rem !important; border-bottom: 2px solid #0056b3; }
    h2 { font-size: 2rem !important; color: #0056b3; }
    h3 { font-size: 1.2rem !important; font-weight: bold; color: #444; }
    </style>
    """, unsafe_allow_html=True)

# # Main Heading
st.write("# 🔬 Virtual Lithography Lab")
st.write("Welcome Aashna! This lab uses NumPy to simulate optical intensity profiles.")
st.divider()

# --- SIDEBAR: PARAMETERS ---
with st.sidebar:
    st.write("### 🏗️ Substrate & Resist")
    res_type = st.selectbox("Resist Type", ["Positive", "Negative"])
    thickness = st.slider("Resist Thickness (nm)", 50, 800, 300)
    
    st.divider()
    
    st.write("### 💡 Exposure Settings")
    wl = st.selectbox("Wavelength (nm)", [365, 248, 193, 13.5], index=2)
    na = st.slider("Numerical Aperture (NA)", 0.3, 1.35, 0.85)
    dose = st.slider("Dose (mJ/cm²)", 5, 100, 25)
    focus = st.slider("Focus Offset (nm)", -200, 200, 0)

# --- CALCULATIONS (NUMPY) ---
# Rayleigh Criteria for Resolution (CD) and Depth of Focus (DOF)
k1 = 0.4
k2 = 0.5
cd = (k1 * wl) / na
dof = (k2 * wl) / (na**2)

# --- SIMULATION LOGIC ---
x = np.linspace(-500, 500, 1000)
# Simple Aerial Image Model: Sinc squared function to simulate diffraction
intensity = np.sinc(x * na / wl)**2 

# Apply focus penalty (blurring effect)
blur = abs(focus) / 200
if blur > 0:
    intensity = np.convolve(intensity, np.ones(int(100*blur)+1)/(100*blur+1), mode='same')

# --- DASHBOARD LAYOUT ---
col1, col2 = st.columns([1, 2])

with col1:
    st.write("## 📊 Metrics")
    st.metric("Critical Dimension (CD)", f"{cd:.2f} nm")
    st.metric("Depth of Focus (DOF)", f"{dof:.2f} nm")
    
    # Process Status Logic
    if abs(focus) > dof:
        st.error("❌ FAIL: Out of Focus")
    elif abs(focus) > dof * 0.7:
        st.warning("⚠️ WARNING: Near Focus Limit")
    else:
        st.success("✅ PASS: Optimal Process")

with col2:
    st.write("## 🖼️ Visualization")
    tab1, tab2 = st.tabs(["Aerial Image", "Resist Profile"])
    
    with tab1:
        fig, ax = plt.subplots()
        ax.plot(x, intensity, color='#0056b3', lw=2)
        ax.fill_between(x, intensity, alpha=0.2, color='#0056b3')
        ax.set_title(f"Aerial Image Intensity (λ={wl}nm)")
        ax.set_xlabel("Position (nm)")
        ax.set_ylabel("Relative Intensity")
        st.pyplot(fig)
        
    with tab2:
        # Simple simulation of resist development based on intensity threshold
        threshold = 0.5 if res_type == "Positive" else 0.3
        resist_remaining = np.where(intensity < threshold, thickness, 0) if res_type == "Positive" \
                           else np.where(intensity > threshold, thickness, 0)
        
        fig2, ax2 = plt.subplots()
        ax2.fill_between(x, resist_remaining, color="orange", step="mid", label="Photoresist")
        ax2.set_ylim(0, 1000)
        ax2.set_title("Cross-section Profile")
        ax2.set_ylabel("Height (nm)")
        ax2.legend()
        st.pyplot(fig2)

st.divider()
st.info("💡 **Tip:** Adjust the Numerical Aperture to see the Critical Dimension (CD) shrink!")