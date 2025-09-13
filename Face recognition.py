import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# Load Haar Cascade Classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# App Title
st.title("👤 Face Detection with Viola-Jones (Haar Cascade)")

# Instructions
st.markdown("""
### 📌 Instructions:
1. Upload an image using the uploader below.  
2. Adjust **scaleFactor** and **minNeighbors** sliders to fine-tune face detection.  
3. Pick a rectangle **color** for marking detected faces.  
4. Save the processed image to your device.  
""")

# Upload image
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

# Sidebar controls
st.sidebar.header("⚙️ Detection Settings")
scaleFactor = st.sidebar.slider("Scale Factor", 1.05, 2.0, 1.1, 0.05)
minNeighbors = st.sidebar.slider("Min Neighbors", 1, 10, 5, 1)
rect_color = st.sidebar.color_picker("Pick Rectangle Color", "#00FF00")  # Default green
bgr_color = tuple(int(rect_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))  # Convert HEX to BGR

if uploaded_file is not None:
    # Convert uploaded image to OpenCV format
    image = Image.open(uploaded_file)
    image_np = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors)

    # Draw rectangles around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image_np, (x, y), (x + w, y + h), bgr_color, 2)

    # Show result
    st.image(image_np, caption=f"Detected {len(faces)} face(s)", use_column_width=True)

    # Save option
    save_btn = st.button("💾 Save Image")
    if save_btn:
        save_path = os.path.join("detected_faces.png")
        cv2.imwrite(save_path, cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))
        st.success(f"Image saved as {save_path}")
        with open(save_path, "rb") as file:
            st.download_button("⬇️ Download Image", file, file_name="detected_faces.png")

