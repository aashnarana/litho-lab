import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="VLSI Full Process Lab", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    h1 { font-size: 3rem !important; color: #4facfe; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #1a1c24; border: 1px solid #30363d; border-radius: 8px; color: #888; padding: 10px 15px;
    }
    .stTabs [aria-selected="true"] { background-color: #0056b3 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# # 🔬 9-Step Process Visualizer
st.write("Aashna, use the tabs below to see the **Top View** and **Side View** for every step of the fabrication cycle.")
st.divider()

# --- 2. SIDEBAR PARAMETERS ---
with st.sidebar:
    st.write("### ⚙️ SETTINGS")
    res_type = st.selectbox("Resist Type", ["Positive", "Negative"])
    wl = st.selectbox("Wavelength", [365, 248, 193, 13.5], index=2)
    na = st.slider("NA", 0.3, 1.35, 0.85)
    st.divider()
    run_sim = st.button("🚀 RUN SIMULATION")

# --- 3. SIMULATION LOGIC ---
if run_sim:
    # Calculations
    k1 = 0.4
    cd = (k1 * wl) / na
    grid_size = 200
    x = np.linspace(-500, 500, grid_size)
    y = np.linspace(-500, 500, grid_size)
    X, Y = np.meshgrid(x, y)
    
    # Mathematical model for Aerial Image
    intensity = np.abs(np.sinc(X * na / (wl/2)))**2
    threshold = 0.5
    res_profile = np.where(intensity[grid_size//2, :] < threshold, 40, 0) if res_type == "Positive" else np.where(intensity[grid_size//2, :] > threshold, 40, 0)

    # Helper function for dual-view plotting
    def plot_dual_view(step_name, top_data, side_logic_fn):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"#### {step_name}: Top View")
            fig_t, ax_t = plt.subplots(facecolor='#0e1117')
            ax_t.imshow(top_data, extent=[-500, 500, -500, 500], cmap='magma')
            ax_t.axis('off')
            st.pyplot(fig_t)
        with col2:
            st.write(f"#### {step_name}: Side View")
            fig_s, ax_s = plt.subplots(facecolor='#0e1117')
            ax_s.set_facecolor('#1a1c24')
            side_logic_fn(ax_s)
            ax_s.set_xlim(-500, 500)
            ax_s.set_ylim(-60, 150)
            ax_s.axis('off')
            st.pyplot(fig_s)

    # --- 4. TABS FOR EACH STEP ---
    t1, t2, t3, t4, t5 = st.tabs(["1-2. Deposit", "3-5. Coat/Bake", "6. Exposure", "7. Develop", "8-9. Etch/Strip"])

    with t1:
        st.info("Step 1-2: Cleaning and Deposition of Target Material.")
        def side_1(ax):
            ax.add_patch(plt.Rectangle((-500, -50), 1000, 50, color='#8B0000')) # Substrate
            ax.add_patch(plt.Rectangle((-500, 0), 1000, 20, color='#008B8B')) # Target
        plot_dual_view("Deposition", np.ones((grid_size, grid_size))*0.5, side_1)

    with t2:
        st.info("Step 3-5: Wafer Priming, Resist Coating, and Soft-Baking.")
        def side_2(ax):
            ax.add_patch(plt.Rectangle((-500, -50), 1000, 50, color='#8B0000'))
            ax.add_patch(plt.Rectangle((-500, 0), 1000, 20, color='#008B8B'))
            ax.add_patch(plt.Rectangle((-500, 20), 1000, 40, color='#CCCC00', alpha=0.8)) # Resist
        plot_dual_view("Coating", np.ones((grid_size, grid_size))*0.8, side_2)

    with t3:
        st.warning("Step 6: Exposure through mask. Red arrows represent UV light.")
        def side_3(ax):
            ax.add_patch(plt.Rectangle((-500, -50), 1000, 50, color='#8B0000'))
            ax.add_patch(plt.Rectangle((-500, 0), 1000, 20, color='#008B8B'))
            ax.add_patch(plt.Rectangle((-500, 20), 1000, 40, color='#CCCC00', alpha=0.4))
            for i in range(-400, 500, 200):
                ax.annotate('', xy=(i, 20), xytext=(i, 100), arrowprops=dict(arrowstyle='->', color='red'))
        plot_dual_view("Exposure", intensity, side_3)

    with t4:
        st.success("Step 7: Development removes soluble resist.")
        def side_4(ax):
            ax.add_patch(plt.Rectangle((-500, -50), 1000, 50, color='#8B0000'))
            ax.add_patch(plt.Rectangle((-500, 0), 1000, 20, color='#008B8B'))
            ax.fill_between(x, 20, 20 + res_profile, color='#808080', step="mid") # Developed Resist
        # Top view shows the pattern formed in the resist
        top_res = np.where(intensity < threshold, 1, 0) if res_type == "Positive" else np.where(intensity > threshold, 1, 0)
        plot_dual_view("Development", top_res, side_4)

    with t5:
        st.error("Step 8-9: Etching the target material and Stripping the resist.")
        def side_5(ax):
            ax.add_patch(plt.Rectangle((-500, -50), 1000, 50, color='#8B0000'))
            # Etched profile (Target material remains only where resist was)
            etch_p = np.where(res_profile > 0, 20, 0)
            ax.fill_between(x, 0, etch_p, color='#008B8B', step="mid")
        plot_dual_view("Final Etch", top_res, side_5)

else:
    st.info("Click 'Run Simulation' to visualize the dual-view process flow.")
