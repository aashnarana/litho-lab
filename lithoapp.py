import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 1. PAGE CONFIG & UI STYLING ---
st.set_page_config(page_title="VLSI 3D Litho Lab", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    h1 { font-size: 2.8rem !important; color: #0088cc; }
    h2 { font-size: 1.8rem !important; color: #00ccff; }
    .stButton>button { width: 100%; border-radius: 4px; }
    [data-testid="stSidebar"] { background-color: #1c1f26 !important; }
    </style>
    """, unsafe_allow_html=True)

# Main Heading
st.write("# Step-by-Step 3D Lithography Visualizer")
st.write(f"Hello Aashna! This simulation renders the physical volume of the material stack, from coating to development.")
st.divider()

# --- 2. SIDEBAR PARAMETERS ---
with st.sidebar:
    st.write("## ⚙️ Process Flow")
    
    # Sequential Stage Selector (Matches image_2.png flow)
    current_stage = st.select_slider("Select Fabrication Step", 
                                     options=["1. Start: Uniform Stack", "2. Develop: Positive PR", "3. Final Pattern"])
    
    st.divider()
    st.write("## ⚙️ Exposure Details")
    wl = st.selectbox("Wavelength", [365, 248, 193, 13], index=2, format_func=lambda x: f"{x} nm")
    na = st.slider("Numerical Aperture (NA)", 0.5, 1.35, 0.85)
    
    st.divider()
    run_sim = st.button("🚀 RENDER 3D VOLUME")

# --- 3. SIMULATION LOGIC ---
if run_sim:
    # A. Grid Creation (NumPy)
    # We define a volumetric grid of 'voxels' (Legos) to build the stack.
    x_dim, y_dim, z_dim = 20, 20, 10
    voxels = np.zeros((x_dim, y_dim, z_dim), dtype=bool)
    colors = np.empty(voxels.shape, dtype=object)

    # Color definitions (Technical drawing style)
    COLOR_SUBSTRATE = '#8B0000' # Deep Red (Like your first sketch)
    COLOR_RESIST = '#CCCC00'    # Dull Yellow (The "Resist" layer)
    COLOR_PATTERN = '#AAAAAA'   # Grey (The final developed resist)

    # B. Building the Stack: Stage 1 (Uniform Stack)
    # Substrate (Red)
    voxels[:, :, 0:3] = True
    colors[:, :, 0:3] = COLOR_SUBSTRATE

    # Resist (Yellow)
    voxels[:, :, 3:6] = True
    colors[:, :, 3:6] = COLOR_RESIST

    # C. Pattern Logic: Stage 2-3 (Development)
    if current_stage in ["2. Develop: Positive PR", "3. Final Pattern"]:
        # Logic for a "Cross" pattern matching your diagram
        # Positive Resist: Everything is removed EXCEPT the cross pattern
        voxels[:, :, 3:6] = False # Clear the uniform yellow layer
        
        # Draw the cross (3 voxels wide)
        voxels[8:12, 4:16, 3:6] = True # Vertical arm
        voxels[4:16, 8:12, 3:6] = True # Horizontal arm
        
        # During Development, we show the cross inGrey
        if current_stage == "2. Develop: Positive PR":
            colors[voxels] = COLOR_PATTERN
        else:
            # Final pattern: Keep the substrate red, pattern grey
            colors[0:20, 0:20, 0:3] = COLOR_SUBSTRATE
            colors[8:12, 4:16, 3:6] = COLOR_PATTERN
            colors[4:16, 8:12, 3:6] = COLOR_PATTERN

    # --- 4. RENDERER (Matplotlib 3D Voxel Engine) ---
    st.write(f"### 🔎 Viewing {current_stage}")
    
    col1, col2 = st.columns([2, 1])

    with col1:
        # Create the 3D plot
        fig = plt.figure(figsize=(10, 8), facecolor='#0e1117')
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#0e1117')

        # Voxel rendering
        ax.voxels(voxels, facecolors=colors, edgecolor='#121212', linewidth=0.3)

        # Matplotlib 3D View Angle (Matches your diagram perspective)
        ax.view_init(elev=35, azim=45) 
        ax.set_axis_off()
        st.pyplot(fig)

    with col2:
        # Side/Top View breakdown using tabs
        tab_side, tab_top = st.tabs(["📐 Side View (X-Z)", "🔝 Top View (X-Y)"])
        
        # Mathematical model for CD calculation
        k1 = 0.4
        cd = (k1 * wl) / na
        
        with tab_side:
            # Slice the 3D grid at the centerline (Y=10)
            mid_slice = voxels[:, 10, :]
            color_slice = colors[:, 10, :]
            
            fig_s, ax_s = plt.subplots(figsize=(6, 4), facecolor='#0e1117')
            ax_s.set_facecolor('#1e1e1e')
            ax_s.imshow(np.swapaxes(mid_slice,0,1), cmap='binary', extent=[-100, 100, -60, 100])
            ax_s.axis('off')
            ax_s.set_title("Cross-section", color='white')
            st.pyplot(fig_s)
            st.write(f"**CD** ≈ {cd:.0f} nm")

        with tab_top:
            # Top-down projection of the voxels
            fig_t, ax_t = plt.subplots(figsize=(6, 4), facecolor='#0e1117')
            ax_t.set_facecolor('#1e1e1e')
            projection = np.any(voxels, axis=2)
            ax_t.imshow(projection, cmap='Greys', extent=[-100, 100, -100, 100])
            ax_t.axis('off')
            st.pyplot(fig_t)

else:
    # Initial State: Clear visualizer with a tip
    st.info("Adjust the Wavelength in the sidebar and click **RENDER 3D VOLUME** to begin.")
    st.divider()
    
    # Conceptual help
    with st.expander("📚 Study Note: The Step-by-Step 3D Process"):
        st.write("""
        This 3D view is critical for understanding 'volumetric pattern formation'. Unlike a 2D drawing, the 
        light must activate the *entire depth* of the resist. In VLSI, any mismatch between the Top View and 
        the final developed Side View can cause transistor failure.
        """)
