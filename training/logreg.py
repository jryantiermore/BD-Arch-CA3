import os
import json
import joblib
import numpy as np
import csv
import argparse
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.feature import hog
from sklearn.linear_model import LogisticRegression

# Paths
METADATA_FILE = "data/metadata.csv"   # created during ingestion

def load_dataset(orientations):
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
                orientations=orientations,
                block_norm="L2-Hys"
            )

            X.append(features)
            y.append(label)

    return np.array(X), np.array(y)

def train_model(output_path, orientations):
    X, y = load_dataset(orientations)

    model = LogisticRegression(max_iter=100)
    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, output_path)

    print(f"Model trained and saved to: {output_path}")
    print(f"HOG orientations used: {orientations}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a face classifier model.")
    parser.add_argument("--output", type=str, required=True,
                        help="Output path for the trained model, e.g. models/blue.pkl")
    parser.add_argument("--orientations", type=int, default=9,
                        help="Number of HOG orientations (default: 9)")

    args = parser.parse_args()
    train_model(args.output, args.orientations)
