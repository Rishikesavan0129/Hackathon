
import streamlit as st
import pandas as pd
import cv2
from PIL import Image
import numpy as np

# Load color dataset
@st.cache_data
def load_colors():
    df = pd.read_csv("colors.csv", names=["color", "color_name", "hex", "R", "G", "B"], header=None)
    return df

def get_color_name(R, G, B, df):
    minimum = float('inf')
    cname = "Unknown"
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B - int(df.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = df.loc[i, "color_name"]
    return cname

st.title("Color Detection App")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
df = load_colors()

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img = np.array(image)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    x = st.number_input("Enter X coordinate", min_value=0, max_value=img.shape[1]-1, value=0)
    y = st.number_input("Enter Y coordinate", min_value=0, max_value=img.shape[0]-1, value=0)

    if st.button("Detect Color"):
        b, g, r = img[int(y), int(x)]
        color_name = get_color_name(r, g, b, df)
        st.markdown(f"**Color Name:** {color_name}")
        st.markdown(f"**RGB:** ({r}, {g}, {b})")
        st.markdown("**Detected Color:**")
        st.markdown(
            f"<div style='width:100px;height:50px;background-color:rgb({r},{g},{b});'></div>",
            unsafe_allow_html=True
        )
