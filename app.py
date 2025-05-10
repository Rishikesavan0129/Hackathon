
import streamlit as st
import pandas as pd
import cv2
import numpy as np
from PIL import Image

st.title("Color Detection App")

@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv")

colors_df = load_colors()

def get_color_name(R, G, B):
    min_dist = float('inf')
    cname = "Unknown"
    for _, row in colors_df.iterrows():
        d = abs(R - row['R']) + abs(G - row['G']) + abs(B - row['B'])
        if d < min_dist:
            min_dist = d
            cname = row['color_name']
    return cname

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    img = Image.open(uploaded_file)
    img_np = np.array(img)
    st.image(img, use_column_width=True)

    click = st.image(img, use_column_width=True)

    st.write("Click on the image to detect color (Use desktop Streamlit)")

    if 'coords' not in st.session_state:
        st.session_state.coords = None

    def get_click_coordinates():
        st.write("Note: Click feature not available directly in basic Streamlit.")
        st.write("Instead, enter X and Y coordinates below:")

        x = st.number_input("X", min_value=0, max_value=img_np.shape[1]-1, step=1)
        y = st.number_input("Y", min_value=0, max_value=img_np.shape[0]-1, step=1)

        if st.button("Detect Color"):
            pixel = img_np[int(y), int(x)]
            R, G, B = int(pixel[0]), int(pixel[1]), int(pixel[2])
            color_name = get_color_name(R, G, B)

            st.success(f"Color: {color_name}")
            st.info(f"RGB: ({R}, {G}, {B})")
            st.markdown(f"<div style='width:100px;height:50px;background-color:rgb({R},{G},{B});'></div>", unsafe_allow_html=True)

    get_click_coordinates()
