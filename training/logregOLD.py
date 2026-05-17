import os
import json
import joblib
import numpy as np
import csv
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.feature import hog
from sklearn.linear_model import LogisticRegression

# Paths
METADATA_FILE = "data/metadata.csv"   # created during ingestion
MODEL_PATH = "models/face_classifier.pkl"

def load_dataset():
    X = []
    y = []

    with open(METADATA_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            img_path = row["processed_path"]
            label = int(row["faces_found"])

            img = imread(img_path)
            img_gray = rgb2gray(img)

            features = hog(
            	img_gray,
            	pixels_per_cell=(8, 8),
            	cells_per_block=(2, 2),
            	orientations=9,
            	block_norm="L2-Hys"
            )

            X.append(features)
            y.append(label)

    return np.array(X), np.array(y)

def train_model():
    X, y = load_dataset()

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("Model trained and saved to:", MODEL_PATH)

if __name__ == "__main__":
    train_model()
