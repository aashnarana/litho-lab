import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(page_title="Virtual Litho Lab", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    /* Top Bar Styling */
    .top-bar { background: #161b22; padding: 15px; border-radius: 10px; border-bottom: 2px solid #00f2ff; margin-bottom: 20px; }
    /* Panel Styling */
    .lab-panel { background: #1c2128; padding: 20px; border-radius: 12px; border: 1px solid #30363d; height: 85vh; overflow-y: auto; }
    h1, h2, h3 { color: #00f2ff; font-family: 'Courier New', monospace; }
    .metric-box { background: #0d1117; padding: 10px; border-radius: 8px; border-left: 4px solid #7000ff; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. TOP BAR (Experiment Control) ---
st.markdown('<div class="top-bar"><h1>🧪 Photolithography Process Simulation</h1></div>', unsafe_allow_html=True)

tcol1, tcol2, tcol3 = st.columns([2, 3, 2])
with tcol1:
    run = st.button("▶ RUN SIMULATION")
with tcol2:
    st.write("**Step Indicator:**")
    st.caption("Coating → Pre-Bake → Exposure → Development")
with tcol3:
    preset = st.selectbox("📁 Load Preset", ["Ideal", "Overexposed", "Underexposed"])

st.divider()

# --- 3. MAIN LAB INTERFACE (SPLIT-SCREEN) ---
left_col, center_col, right_col = st.columns([1, 2, 1])

# 🔷 LEFT PANEL: INPUTS
with left_col:
    st.markdown('<div class="lab-panel">', unsafe_allow_html=True)
    st.subheader("📥 Process Inputs")
    
    with st.expander("📌 A. Photoresist Parameters", expanded=True):
        res_type = st.radio("Resist Type", ["Positive", "Negative"])
        thick = st.slider("Thickness (µm)", 0.5, 5.0, 1.2)
        spin = st.slider("Spin Speed (RPM)", 1000, 6000, 3000)
    
    with st.expander("📌 B. Pre-Exposure (Soft Bake)"):
        sb_temp = st.slider("Temperature (°C)", 60, 120, 90)
        sb_time = st.slider("Time (sec)", 30, 120, 60)
        
    with st.expander("📌 C. Exposure Settings"):
        wl = st.number_input("UV Wavelength (nm)", value=193)
        dose = st.slider("Dose (mJ/cm²)", 10, 200, 50)
        mask = st.selectbox("Mask Pattern", ["Lines", "Dots", "Custom"])

    with st.expander("📌 D. Development"):
        dev_time = st.slider("Dev Time (sec)", 10, 90, 45)
    st.markdown('</div>', unsafe_allow_html=True)

# 🔷 CENTER PANEL: VISUALIZER
with center_col:
    st.subheader("🧱 Multi-Layer Visualization")
    view_mode = st.tabs(["3D Volumetric", "Cross-Sectional", "Top-Down"])
    
    # 3D Rendering Logic
    x, y, z = 20, 20, 10
    voxels = np.zeros((x, y, z), dtype=bool)
    colors = np.empty(voxels.shape, dtype=object)
    
    # Material Colors (Neon Theme)
    C_SUB = '#1a1a1a' # Dark Wafer
    C_TGT = '#00f2ff' # Cyan Target
    C_RES = '#7000ff' # Purple Resist
    
    # Build the stack
    voxels[:, :, 0:2] = True; colors[:, :, 0:2] = C_SUB
    voxels[:, :, 2:4] = True; colors[:, :, 2:4] = C_TGT
    
    # Simulation Logic for development
    if run:
        # Pattern logic based on "Dose" and "Resist Type"
        is_pos = (res_type == "Positive")
        if dose > 150: # Overexposed
            p_width = 8 if is_pos else 2
        elif dose < 30: # Underexposed
            p_width = 2 if is_pos else 8
        else:
            p_width = 4
            
        # Draw Pattern
        if is_pos:
            voxels[10-p_width:10+p_width, :, 4:8] = False # Exposed area removed
            voxels[0:10-p_width, :, 4:8] = True; colors[0:10-p_width, :, 4:8] = C_RES
            voxels[10+p_width:20, :, 4:8] = True; colors[10+p_width:20, :, 4:8] = C_RES
        else:
            voxels[10-p_width:10+p_width, :, 4:8] = True; colors[10-p_width:10+p_width, :, 4:8] = C_RES
            
    with view_mode[0]:
        fig = plt.figure(figsize=(8, 6), facecolor='#0b0e14')
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#0b0e14')
        ax.voxels(voxels, facecolors=colors, edgecolor='#000000', linewidth=0.1)
        ax.view_init(elev=20, azim=45)
        ax.axis('off')
        st.pyplot(fig)

# 🔷 RIGHT PANEL: OUTPUTS
with right_col:
    st.markdown('<div class="lab-panel">', unsafe_allow_html=True)
    st.subheader("📊 Output Metrics")
    
    cd_val = (wl * 0.4) / 0.85 # Simplified CD formula
    
    st.markdown(f'<div class="metric-box"><small>CD (Critical Dimension)</small><h3>{cd_val:.1f} nm</h3></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-box"><small>Resolution</small><h3>{cd_val*1.2:.1f} nm</h3></div>', unsafe_allow_html=True)
    
    st.subheader("⚠️ Warnings")
    if dose > 150:
        st.error("Overexposure detected: Pattern widening.")
    elif dose < 30:
        st.warning("Underexposure: Incomplete development.")
    else:
        st.success("Process within ideal window.")
        
    st.button("🧾 Export Lab Report")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. BOTTOM PANEL (Theory) ---
st.divider()
bcol1, bcol2 = st.columns([1, 1])
with bcol1:
    st.subheader("📈 Exposure Profile")
    st.line_chart(np.sin(np.linspace(0, 10, 100))**2)
with bcol2:
    st.subheader("📘 Step Explanation")
    st.info("**Soft Bake:** Removes solvent and improves adhesion. Too high temperature causes resist hardening (dark decay).")
