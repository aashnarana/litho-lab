import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE SETUP ---
st.set_page_config(page_title="VLSI Mask Simulator", layout="wide")

# Custom CSS for UI consistency
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    h1 { font-size: 3rem !important; color: #4facfe; }
    h2 { font-size: 1.8rem !important; color: #00f2fe; }
    .metric-container { background-color: #1a1c24; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# # Virtual Lithography Lab: Mask Simulation 🎭
st.write("Aashna, you can now swap between different mask geometries to see how the light resolves.")
st.divider()

# --- SIDEBAR: PARAMETERS ---
with st.sidebar:
    st.write("## ⚙️ Process Settings")
    
    ### 🏗️ Mask & Resist
    mask_type = st.selectbox("Mask Pattern", ["Lines/Spaces", "Contact Holes", "Isolated Line", "Dense Array"])
    res_type = st.selectbox("Resist Type", ["Positive", "Negative"])
    thickness = st.slider("Resist Thickness (nm)", 100, 800, 400)
    
    st.divider()
    
    ### 💡 Exposure Settings
    wl = st.selectbox("Wavelength (nm)", [365, 248, 193, 13.5], index=2)
    na = st.slider("Numerical Aperture (NA)", 0.5, 1.35, 0.85)
    focus = st.slider("Focus Offset (nm)", -150, 150, 0)
    
    st.divider()
    run_sim = st.button("🚀 Run Simulation")

# --- SIMULATION ENGINE ---
if run_sim:
    # 1. Physics Calculations
    k1 = 0.4
    cd = (k1 * wl) / na
    dof = (0.5 * wl) / (na**2)
    
    # 2. Grid Creation (NumPy)
    grid_size = 200
    x = np.linspace(-500, 500, grid_size)
    y = np.linspace(-500, 500, grid_size)
    X, Y = np.meshgrid(x, y)
    
    # 3. Mask Geometry Logic
    intensity = np.zeros((grid_size, grid_size))
    
    if mask_type == "Lines/Spaces":
        intensity = np.abs(np.sinc(X * na / (wl/2)))**2
    elif mask_type == "Contact Holes":
        r = np.sqrt(X**2 + Y**2)
        intensity = np.abs(2 * np.sinc(r * na / (wl/2)))**2
    elif mask_type == "Isolated Line":
        intensity = np.where(np.abs(X) < cd/2, 1, 0)
        # Apply diffraction blur
        intensity = np.exp(-(X**2) / (2 * (cd/1.5)**2))
    elif mask_type == "Dense Array":
        intensity = (np.cos(2 * np.pi * X / (cd*2)) + 1) / 2
        
    # Apply Focus Blur (Convolution-like effect)
    blur = abs(focus) / 50
    if blur > 0:
        intensity = intensity * (1 - blur*0.2) # Simplification for visualization
        
    # 4. Visualization
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("### 🔝 Top View (Aerial Image)")
        fig1, ax1 = plt.subplots(facecolor='#0e1117')
        im = ax1.imshow(intensity, extent=[-500, 500, -500, 500], cmap='inferno')
        ax1.set_title(f"{mask_type} Pattern", color='white')
        ax1.axis('off')
        plt.colorbar(im, ax=ax1, label='Light Intensity')
        st.pyplot(fig1)

    with col2:
        st.write("### 📐 Side View (Cross-section)")
        fig2, ax2 = plt.subplots(facecolor='#0e1117')
        ax2.set_facecolor('#1a1c24')
        
        # Cross section taken at center (Y=0)
        center_line = intensity[grid_size//2, :]
        threshold = 0.5 if res_type == "Positive" else 0.3
        
        # Draw Substrate
        ax2.fill_between(x, -50, 0, color='#2c3e50', label='Silicon')
        
        # Draw Resist
        resist_profile = np.where(center_line < threshold, thickness, 0) if res_type == "Positive" \
                         else np.where(center_line > threshold, thickness, 0)
        
        ax2.fill_between(x, 0, resist_profile, color='orange', alpha=0.8, step="mid", label='Photoresist')
        
        ax2.set_ylim(-60, 1000)
        ax2.set_title(f"Z-Axis Profile", color='white')
        ax2.set_ylabel("Thickness (nm)", color='white')
        ax2.legend()
        st.pyplot(fig2)

    # --- METRICS ---
    st.divider()
    m1, m2, m3 = st.columns(3)
    with m1: st.metric("Resolution (CD)", f"{cd:.1f} nm")
    with m2: st.metric("Process Window (DOF)", f"{dof:.1f} nm")
    with m3:
        status = "✅ Stable" if abs(focus) < dof else "❌ Out of Focus"
        st.write(f"**Status:** {status}")

else:
    st.info("👈 Choose a mask type and click 'Run Simulation' to generate the views.")
