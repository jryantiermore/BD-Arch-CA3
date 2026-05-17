# ingestion/preprocess.py
import os
from PIL import Image
import cv2

# Load Haar Cascade once at import time
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def preprocess_image(input_path, output_path, size=(256, 256)):
    """
    Preprocessing:
    - Convert to RGB
    - Resize
    - Detect faces using Haar Cascade
    - Save processed image
    - Return metadata including faces_found
    """

    # Load image with PIL
    img = Image.open(input_path).convert("RGB")
    img = img.resize(size)

    # Save processed image
    img.save(output_path)

    # Convert to OpenCV format for detection
    cv_img = cv2.cvtColor(cv2.imread(output_path), cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        cv_img,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(40, 40)
    )

    faces_found = len(faces)

    return {
        "processed_path": output_path,
        "width": size[0],
        "height": size[1],
        "faces_found": faces_found
    }
