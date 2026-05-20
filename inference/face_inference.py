import joblib
import numpy as np
import os
from PIL import Image
from skimage.color import rgb2gray
from skimage.feature import hog

MODEL_PATH = os.getenv("MODEL_PATH", "models/face_classifier.pkl")
HOG_ORIENTATIONS = int(os.getenv("HOG_ORIENTATIONS", 9))
PIXELS_PER_CELL = int(os.getenv("PIXELS_PER_CELL", 8))
CELLS_PER_BLOCK = int(os.getenv("CELLS_PER_BLOCK", 2))

class FaceClassifier:
    def __init__(self, model_path):
        self.model = joblib.load(model_path)

    def extract_features(self, image_path):
        # Load and preprocess exactly like training
        img = Image.open(image_path).convert("RGB")
        img = img.resize((256, 256))

        img_gray = rgb2gray(np.array(img))

        features = hog(
            img_gray,
            pixels_per_cell=(PIXELS_PER_CELL, PIXELS_PER_CELL),
            cells_per_block=(CELLS_PER_BLOCK, CELLS_PER_BLOCK),
            orientations=HOG_ORIENTATIONS,
            block_norm="L2-Hys"
        )

        return features

    def predict(self, image_path):
        features = self.extract_features(image_path)
        features = features.reshape(1, -1)

        pred = self.model.predict(features)[0]
        prob = self.model.predict_proba(features)[0][pred]

        return {
            "prediction": "face" if pred == 1 else "no_face",
            "confidence": float(prob)
        }
