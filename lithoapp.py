import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Compact 3D Lab", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        width: 100%; border-radius: 15px; border: 1px solid #4facfe;
        background-color: transparent; color: white; font-size: 12px;
    }
    .stButton>button:hover { background-color: #4facfe; color: black; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. NAVIGATION & STATE ---
if 'step' not in st.session_state:
    st.session_state.step = "Deposition"

st.write("## 🔬 Micro-Scale 3D Lithography Lab")

# Small navigation row
cols = st.columns(5)
steps = ["Deposition", "Coating", "Exposure", "Development", "Etching"]
for i, s in enumerate(steps):
    if cols[i].button(f"{i+1}. {s}"):
        st.session_state.step = s

st.divider()

# --- 3. COMPACT 3D LAYOUT ---
# Using columns to force the 3D plot into a smaller space
view_col, info_col = st.columns([1, 1])

with view_col:
    # Build Voxel Grid
    x, y, z = 20, 20, 12
    voxels = np.zeros((x, y, z), dtype=bool)
    colors = np.empty(voxels.shape, dtype=object)
    
    # Colors
    C_SUB, C_TGT, C_RES, C_EXP = '#8B0000', '#008B8B', '#FFD700', '#FF4500'

    # Always Substrate
    voxels[:, :, 0:3] = True
    colors[:, :, 0:3] = C_SUB

    curr = st.session_state.step
    if curr != "Deposition":
        # Target Layer
        if curr == "Etching":
            voxels[8:12, 4:16, 3:5] = True
            voxels[4:16, 8:12, 3:5] = True
            colors[8:12, 4:16, 3:5] = C_TGT
            colors[4:16, 8:12, 3:5] = C_TGT
        else:
            voxels[:, :, 3:5] = True
            colors[:, :, 3:5] = C_TGT

    if curr in ["Coating", "Exposure", "Development"]:
        if curr == "Development":
            voxels[8:12, 4:16, 5:9] = True
            voxels[4:16, 8:12, 5:9] = True
            colors[8:12, 4:16, 5:9] = C_RES
            colors[4:16, 8:12, 5:9] = C_RES
        else:
            voxels[:, :, 5:9] = True
            colors[:, :, 5:9] = C_RES
            if curr == "Exposure":
                colors[8:12, 4:16, 5:9] = C_EXP
                colors[4:16, 8:12, 5:9] = C_EXP

    # Render Smaller Figure
    fig = plt.figure(figsize=(5, 4)) # Reduced from (10, 7) to make it small
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#0e1117')
    ax.voxels(voxels, facecolors=colors, edgecolor='k', linewidth=0.1)
    ax.view_init(elev=30, azim=45)
    ax.set_axis_off()
    st.pyplot(fig)

with info_col:
    st.write(f"### Current Phase: **{curr}**")
    
    # Contextual info based on your process diagram
    if curr == "Deposition":
        st.write("• **Action**: Wafer Cleaning & Layer Deposition")
        st.write("• **Material**: Target material (Teal) is added to the substrate (Red)")
    elif curr == "Coating":
        st.write("• **Action**: Photo-resist Coating & Soft-Baking")
        st.write("• **Result**: A uniform light-sensitive layer (Yellow) is prepared")
    elif curr == "Exposure":
        st.write("• **Action**: UV Exposure through Mask")
        st.write("• **Visual**: The orange 'latent image' shows where the resist chemistry changed")
    elif curr == "Development":
        st.write("• **Action**: Developing the pattern")
        st.write("• **Result**: Soluble resist is washed away, leaving the physical 3D structure")
    elif curr == "Etching":
        st.write("• **Action**: Pattern Etching & Strip")
        st.write("• **Final**: The target material is now shaped, and the resist is removed")
