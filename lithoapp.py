import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 1. PAGE CONFIG & UI STYLING ---
st.set_page_config(page_title="VLSI 3D Lab", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    h1 { font-size: 2.5rem !important; color: #4facfe; }
    .stButton>button { 
        width: 100%; border-radius: 20px; border: 1px solid #4facfe;
        background-color: transparent; color: white; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #4facfe; color: black; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE FOR NAVIGATION ---
if 'step' not in st.session_state:
    st.session_state.step = "Deposition"

# --- 3. TOP NAVIGATION BUTTONS ---
st.write("# 3.0 Interactive Lithography Lab")
cols = st.columns(5)
with cols[0]:
    if st.button("1. Deposition"): st.session_state.step = "Deposition"
with cols[1]:
    if st.button("2. Coating"): st.session_state.step = "Coating"
with cols[2]:
    if st.button("3. Exposure"): st.session_state.step = "Exposure"
with cols[3]:
    if st.button("4. Development"): st.session_state.step = "Development"
with cols[4]:
    if st.button("5. Etching"): st.session_state.step = "Etching"

st.divider()

# --- 4. 3D VOXEL ENGINE ---
x_dim, y_dim, z_dim = 20, 20, 12
voxels = np.zeros((x_dim, y_dim, z_dim), dtype=bool)
colors = np.empty(voxels.shape, dtype=object)

# Color Palette
COLOR_SUB = '#8B0000'   # Red Substrate
COLOR_TGT = '#008B8B'   # Teal Target
COLOR_RES = '#FFD700'   # Yellow Resist
COLOR_EXP = '#FF4500'   # Orange Latent Image

# Layer Logic
# Always show Substrate
voxels[:, :, 0:3] = True
colors[:, :, 0:3] = COLOR_SUB

# Step-specific logic
step = st.session_state.step

if step == "Deposition":
    voxels[:, :, 3:5] = True
    colors[:, :, 3:5] = COLOR_TGT
    msg = "Step 1: Silicon Substrate with a fresh Target Layer (SiO2) deposited on top."

elif step == "Coating":
    voxels[:, :, 3:5] = True
    colors[:, :, 3:5] = COLOR_TGT
    voxels[:, :, 5:9] = True
    colors[:, :, 5:9] = COLOR_RES
    msg = "Step 2: Photoresist is spin-coated and soft-baked into a uniform block."

elif step == "Exposure":
    voxels[:, :, 3:5] = True
    colors[:, :, 3:5] = COLOR_TGT
    voxels[:, :, 5:9] = True
    colors[:, :, 5:9] = COLOR_RES
    # Show latent image "cross" in orange
    colors[8:12, 4:16, 5:9] = COLOR_EXP
    colors[4:16, 8:12, 5:9] = COLOR_EXP
    msg = "Step 3: UV light creates a latent chemical image (orange) inside the resist."

elif step == "Development":
    voxels[:, :, 3:5] = True
    colors[:, :, 3:5] = COLOR_TGT
    # Keep only the cross pattern (Positive Resist logic)
    voxels[8:12, 4:16, 5:9] = True
    voxels[4:16, 8:12, 5:9] = True
    colors[8:12, 4:16, 5:9] = COLOR_RES
    colors[4:16, 8:12, 5:9] = COLOR_RES
    msg = "Step 4: Developer washes away the exposed resist, leaving a 3D relief pattern."

elif step == "Etching":
    # Target layer only exists under where the resist was
    voxels[8:12, 4:16, 3:5] = True
    voxels[4:16, 8:12, 3:5] = True
    colors[8:12, 4:16, 3:5] = COLOR_TGT
    colors[4:16, 8:12, 3:5] = COLOR_TGT
    msg = "Step 5: The pattern is etched into the target layer and the resist is stripped."

# --- 5. RENDERING ---
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#0e1117')
ax.voxels(voxels, facecolors=colors, edgecolor='k', linewidth=0.2)
ax.view_init(elev=30, azim=45)
ax.set_axis_off()

st.pyplot(fig)
st.info(msg)
