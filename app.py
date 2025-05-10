import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image

# Load the color dataset (CSV file)
color_df = pd.read_csv('colors.csv')

# Function to get the closest color name based on RGB values
def get_closest_color(rgb):
    min_dist = float('inf')
    closest_color = None
    for index, row in color_df.iterrows():
        color_rgb = np.array([row['R'], row['G'], row['B']])
        dist = np.linalg.norm(rgb - color_rgb)
        if dist < min_dist:
            min_dist = dist
            closest_color = row['Color']
    return closest_color

# Streamlit app title
st.title("Color Detection Tool")

# Upload an image
uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_image:
    # Open the uploaded image using PIL
    image = Image.open(uploaded_image)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Convert image to OpenCV format (numpy array)
    img_array = np.array(image)

    # Function to detect color at clicked position
    def get_color(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Get the RGB values of the clicked pixel
            rgb = img_array[y, x]
            closest_color_name = get_closest_color(rgb)
            st.write(f"RGB: {rgb}")
            st.write(f"Closest Color: {closest_color_name}")
            # Display the color in a box
            st.markdown(f"<div style='width:100px; height:100px; background-color:rgb({rgb[0]},{rgb[1]},{rgb[2]});'></div>", unsafe_allow_html=True)

    # Create an OpenCV window to display the image
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', get_color)

    # Display image using OpenCV (this will allow mouse clicks)
    while True:
        cv2.imshow('Image', img_array)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit the window
            break
    
    cv2.destroyAllWindows()
