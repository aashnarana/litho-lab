import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="3D VLSI Litho Lab", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #1a1c24 !important; }
    h1 { color: #4facfe; font-size: 2.5rem !important; }
    </style>
    """, unsafe_allow_html=True)

# # 🧊 3D Lithography Visualizer
st.write(f"Hi Aashna! This simulation renders a **3D volumetric model** of the wafer.")
st.divider()

# --- SIDEBAR ---
with st.sidebar:
    st.write("### ⚙️ Fabrication Settings")
    step = st.select_slider("Current Process Step", 
                            options=["1. Deposition", "2. Coating", "3. Exposure", "4. Development", "5. Etching"])
    res_type = st.selectbox("Resist Type", ["Positive", "Negative"])
    na = st.slider("Numerical Aperture (NA)", 0.3, 0.9, 0.6)
    
    st.divider()
    st.info("💡 **Tip:** Use the 'Exposure' step to see the light latent image inside the resist block.")

# --- 3D VOXEL ENGINE ---
# Define a 15x15x10 grid for the 3D space
x_dim, y_dim, z_dim = 20, 20, 12
voxels = np.zeros((x_dim, y_dim, z_dim), dtype=bool)
colors = np.empty(voxels.shape, dtype=object)

# Material Color Palette
COLOR_SUBSTRATE = '#8B0000' # Deep Red
COLOR_TARGET = '#008B8B'    # Teal
COLOR_RESIST = '#FFD700'    # Gold/Yellow
COLOR_EXPOSED = '#FF4500'   # Orange-Red (Latent Image)

# --- STEP-BY-STEP LOGIC ---

# 1. Base Substrate (Always there)
voxels[:, :, 0:3] = True
colors[:, :, 0:3] = COLOR_SUBSTRATE

# 2. Target Layer (SiO2/Metal)
if step != "1. Deposition":
    # If we are at the Etching stage, the target material is only kept in the center
    if step == "5. Etching":
        voxels[8:12, :, 3:5] = True
        colors[8:12, :, 3:5] = COLOR_TARGET
    else:
        voxels[:, :, 3:5] = True
        colors[:, :, 3:5] = COLOR_TARGET

# 3. Resist Layer
if step in ["2. Coating", "3. Exposure", "4. Development"]:
    if step == "4. Development":
        # Remove resist based on "Positive" or "Negative" logic
        if res_type == "Positive":
            voxels[0:8, :, 5:9] = True
            voxels[12:20, :, 5:9] = True
        else:
            voxels[8:12, :, 5:9] = True
        colors[:, :, 5:9] = COLOR_RESIST
    else:
        voxels[:, :, 5:9] = True
        colors[:, :, 5:9] = COLOR_RESIST
        
    # Show Latent Image during Exposure
    if step == "3. Exposure":
        colors[8:12, :, 5:9] = COLOR_EXPOSED

# --- RENDERER ---
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#0e1117')

# Plotting the 3D Cubes
ax.voxels(voxels, facecolors=colors, edgecolor='k', linewidth=0.1)

# Styling the 3D Box
ax.set_axis_off()
ax.view_init(elev=25, azim=45) # Set the 3D angle like the reference image

st.pyplot(fig)

# --- EXPLANATION SECTION ---
st.divider()
st.write(f"### 🔍 Analysis of {step}")

if step == "1. Deposition":
    st.write("We start with the **Substrate** (Red) and deposit the **Target Layer** (Teal).")
elif step == "3. Exposure":
    st.write("The **Latent Image** (Orange) is formed inside the resist block where UV light hit the molecules.")
elif step == "5. Etching":
    st.write("The resist is gone (stripped), and the **Target Layer** is now permanently patterned.")
