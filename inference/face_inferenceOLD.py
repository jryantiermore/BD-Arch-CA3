import joblib
import numpy as np
import os
from PIL import Image
from skimage.color import rgb2gray
from skimage.feature import hog

MODEL_PATH = os.getenv("MODEL_PATH", "models/face_classifier.pkl")

class FaceClassifier:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

    def extract_features(self, image_path):
        # Load and preprocess exactly like training
        img = Image.open(image_path).convert("RGB")
        img = img.resize((256, 256))

        img_gray = rgb2gray(np.array(img))

        features = hog(
            img_gray,
            pixels_per_cell=(8, 8),
            cells_per_block=(2, 2),
            orientations=9,
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
