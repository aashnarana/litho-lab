import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE SETUP ---
st.set_page_config(page_title="VLSI Lithography Lab", layout="wide")

# Custom CSS for distinct heading sizes
st.markdown("""
    <style>
    h1 { font-size: 3.5rem !important; color: #002b5c; }
    h2 { font-size: 2.2rem !important; color: #0056b3; margin-top: 20px; }
    h3 { font-size: 1.4rem !important; font-weight: bold; color: #333; }
    .stButton>button { width: 100%; font-weight: bold; height: 3em; background-color: #0056b3; color: white; }
    </style>
    """, unsafe_allow_html=True)

# # Virtual Lithography Lab 🔬
st.write("Welcome back, Aashna! Adjust your parameters in the sidebar and click **Run Simulation** to compute the results.")
st.divider()

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.write("## ⚙️ Process Parameters")
    
    ### 🏗️ Substrate & Resist
    res_type = st.selectbox("Resist Type", ["Positive", "Negative"])
    thickness = st.slider("Resist Thickness (nm)", 50, 800, 300)
    
    st.divider()
    
    ### 💡 Optical Settings
    wl = st.selectbox("Wavelength (λ) in nm", [365, 248, 193, 13.5], index=2)
    na = st.slider("Numerical Aperture (NA)", 0.3, 1.35, 0.85)
    dose = st.slider("Dose (mJ/cm²)", 5, 100, 25)
    focus = st.slider("Focus Offset (nm)", -200, 200, 0)
    
    st.divider()
    
    # THE RUN BUTTON
    run_sim = st.button("🚀 Run Simulation")

# --- SIMULATION ENGINE ---
# We use st.session_state to "remember" the results so they don't disappear 
if run_sim:
    # 1. Physics Calculations
    k1, k2 = 0.4, 0.5
    cd = (k1 * wl) / na
    dof = (k2 * wl) / (na**2)
    
    # 2. NumPy Modeling
    x = np.linspace(-500, 500, 1000)
    # Modeling the Aerial Image Intensity
    intensity = np.sinc(x * na / (wl/2))**2 
    
    # Apply Focus Blur
    blur_factor = abs(focus) / 200
    if blur_factor > 0:
        kernel_size = int(100 * blur_factor) + 1
        intensity = np.convolve(intensity, np.ones(kernel_size)/kernel_size, mode='same')

    # 3. Visualization Layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("## 📊 Process Metrics")
        st.metric("Critical Dimension (CD)", f"{cd:.2f} nm")
        st.metric("Depth of Focus (DOF)", f"{dof:.2f} nm")
        
        if abs(focus) > dof:
            st.error("### ❌ FAIL: Out of Focus")
            st.write("The focus offset exceeds the Depth of Focus. The resist won't resolve correctly.")
        else:
            st.success("### ✅ PASS: Stable Process")

    with col2:
        st.write("## 🖼️ Visualization")
        
        # Plotting the Intensity Curve
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(x, intensity, color='#0056b3', lw=2, label='Light Intensity')
        ax.fill_between(x, intensity, alpha=0.1, color='#0056b3')
        
        # Plotting the Resist Cross-section
        threshold = 0.4 if res_type == "Positive" else 0.2
        resist_profile = np.where(intensity < threshold, thickness, 0) if res_type == "Positive" \
                         else np.where(intensity > threshold, thickness, 0)
        
        ax.fill_between(x, -resist_profile/100, 0, color="orange", alpha=0.8, step="mid", label="Resist Profile")
        
        ax.set_title(f"Lithography Simulation: λ={wl}nm, NA={na}")
        ax.set_xlabel("Position (nm)")
        ax.set_ylabel("Normalized Intensity / Profile")
        ax.legend()
        st.pyplot(fig)
        
    st.divider()
    st.write("### 📝 Lab Summary")
    st.info(f"Using **{wl}nm** light with an **NA of {na}** provides a theoretical resolution limit of **{cd:.2f}nm**.")

else:
    st.info("👈 Adjust the parameters in the sidebar and click the **Run Simulation** button to see the results!")
