import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 1. SETTINGS & NEON THEME ---
st.set_page_config(page_title="VLSI Nano-Lab", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .step-container { display: flex; justify-content: space-between; margin-bottom: 20px; gap: 5px; }
    .stButton>button { 
        border-radius: 5px; height: 3em; font-weight: bold; font-size: 12px;
        transition: 0.3s; border: 1px solid #30363d;
    }
    /* Active Step Glow */
    .active-btn { border: 2px solid #00f2ff !important; box-shadow: 0 0 10px #00f2ff; }
    .panel { background: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #30363d; }
    h3 { color: #00f2ff; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE (The Brain) ---
if 'current_step' not in st.session_state:
    st.session_state.current_step = "Wafer"

# --- 3. TOP BAR: STEP NAVIGATION BUTTONS ---
st.write("### 🔷 1. Process Step Control")
step_cols = st.columns(9)
steps = ["Wafer", "Coat", "Soft Bake", "Align", "Exposure", "PEB", "Develop", "Etch", "Strip"]

for i, s in enumerate(steps):
    if step_cols[i].button(s, key=f"btn_{s}"):
        st.session_state.current_step = s

st.divider()

# --- 4. MAIN INTERFACE LAYOUT ---
left_input, center_viz, right_ctrl = st.columns([1, 2, 1])

# 🔷 LEFT PANEL: PARAMETERS
with left_input:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("📥 Inputs")
    
    pr_type = st.radio("Photoresist Type", ["Positive PR", "Negative PR"], horizontal=True)
    mask_shape = st.selectbox("Mask Pattern", ["Lines", "Dots", "Contact Holes", "Grid"])
    
    st.markdown("---")
    dose = st.slider("Exposure Dose (mJ/cm²)", 10, 200, 50)
    thick = st.slider("Thickness (µm)", 0.5, 3.0, 1.2)
    
    apply = st.button("🔥 APPLY CHANGES", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# 🔷 CENTER PANEL: 3D VISUALIZER
with center_viz:
    # 3D Voxel Setup
    x, y, z = 20, 20, 12
    voxels = np.zeros((x, y, z), dtype=bool)
    colors = np.empty(voxels.shape, dtype=object)
    
    # Material Colors
    C_SUB = '#2c3e50'   # Dark Gray Substrate
    C_TGT = '#00f2ff'   # Cyan Target Layer
    C_RES = '#7000ff'   # Purple Photoresist
    C_EXP = '#ff00ff'   # Neon Pink (Exposed Region)

    curr = st.session_state.step = st.session_state.current_step

    # 🧱 Layer Construction Logic
    # 1. Always Substrate
    voxels[:, :, 0:2] = True; colors[:, :, 0:2] = C_SUB
    
    # 2. Target Layer (Silicon Dioxide)
    if curr != "Wafer":
        if curr in ["Etch", "Strip"]:
            voxels[8:12, 4:16, 2:4] = True; colors[8:12, 4:16, 2:4] = C_TGT
            voxels[4:16, 8:12, 2:4] = True; colors[4:16, 8:12, 2:4] = C_TGT
        else:
            voxels[:, :, 2:4] = True; colors[:, :, 2:4] = C_TGT

    # 3. Photoresist Layer
    if curr in ["Coat", "Soft Bake", "Align", "Exposure", "PEB", "Develop"]:
        if curr == "Develop":
            # POSITIVE: Exposed is removed. NEGATIVE: Unexposed is removed.
            if pr_type == "Positive PR":
                voxels[0:8, :, 4:9] = True; voxels[12:20, :, 4:9] = True
                colors[:, :, 4:9] = C_RES
            else:
                voxels[8:12, 4:16, 4:9] = True; voxels[4:16, 8:12, 4:16] = True
                colors[:, :, 4:9] = C_RES
        else:
            voxels[:, :, 4:9] = True; colors[:, :, 4:9] = C_RES
            # Highlight Exposure Pattern
            if curr in ["Exposure", "PEB"]:
                colors[8:12, 4:16, 4:9] = C_EXP
                colors[4:16, 8:12, 4:9] = C_EXP

    # Render 3D
    fig = plt.figure(figsize=(7, 6), facecolor='#0b0e14')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#0b0e14')
    ax.voxels(voxels, facecolors=colors, edgecolor='k', linewidth=0.1)
    ax.view_init(elev=25, azim=45)
    ax.axis('off')
    st.pyplot(fig)
    
    st.write(f"### Current View: **{curr}**")

# 🔷 RIGHT PANEL: SMART PREVIEW & OUTPUTS
with right_ctrl:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("🔍 Smart Preview")
    
    if st.button("🖼️ Pre-Exposure"): st.session_state.current_step = "Coat"
    if st.button("🖼️ Post-Exposure"): st.session_state.current_step = "Exposure"
    if st.button("🖼️ After Development"): st.session_state.current_step = "Develop"
    if st.button("🖼️ Final Output"): st.session_state.current_step = "Strip"
    
    st.markdown("---")
    st.subheader("📊 Metrics")
    st.metric("CD (Line Width)", f"{40 + (dose/10):.1f} nm")
    st.metric("Uniformity", "98.2 %")
    
    if dose > 160:
        st.error("⚠️ Overexposure Warning")
    st.markdown('</div>', unsafe_allow_html=True)
