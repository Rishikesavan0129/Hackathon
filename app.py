
import streamlit as st
import pandas as pd
import numpy as np
import cv2
from PIL import Image

# Load color dataset
@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv", names=["color", "color_name", "hex", "R", "G", "B"], header=None)

colors_df = load_colors()

# Function to get closest color name from RGB
def get_color_name(R, G, B):
    minimum = float('inf')
    cname = ""
    for i in range(len(colors_df)):
        d = abs(R - int(colors_df.loc[i, "R"])) + abs(G - int(colors_df.loc[i, "G"])) + abs(B - int(colors_df.loc[i, "B"]))
        if d < minimum:
            minimum = d
            cname = colors_df.loc[i, "color_name"]
    return cname

st.title("Color Detection from Image")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Click coordinates
    st.write("**Click on the image to detect color.**")
    clicked = st.experimental_data_editor(img_array, num_rows="dynamic", disabled=True, key="editor")

    # Using a dummy click event handler (Streamlit does not support pixel clicks directly on image)
    x = st.number_input("X-coordinate", min_value=0, max_value=img_array.shape[1]-1, value=0)
    y = st.number_input("Y-coordinate", min_value=0, max_value=img_array.shape[0]-1, value=0)

    if st.button("Detect Color"):
        b, g, r = img_array[y, x]
        color_name = get_color_name(r, g, b)
        st.write(f"**Color Name:** {color_name}")
        st.write(f"**RGB:** ({r}, {g}, {b})")
        st.markdown(f"<div style='width:100px;height:50px;background-color:rgb({r},{g},{b});'></div>", unsafe_allow_html=True)
