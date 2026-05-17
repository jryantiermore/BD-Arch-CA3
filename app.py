import os
import uuid
from PIL import Image
from inference.face_inference import FaceClassifier
from flask import Flask, request, jsonify
from ingestion.upload_handler import handle_upload   # <-- FIXED IMPORT

app = Flask(__name__)

classifier = None #load model if available
try:
    classifier = FaceClassifier()
    print("Model loaded successfully.")
except FileNotFoundError:
    print("Model not found. /predict will not work until training is done, remember!!!.")


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files["file"]
    result, error = handle_upload(file)

    if error:
        return jsonify({"error": error}), 400

    return jsonify(result), 200


@app.route("/predict", methods=["POST"])
def predict():
    if classifier is None:
        return jsonify({"error": "Model not loaded. Train the model first."}), 400

    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Validate image
    try:
        img = Image.open(file.stream)
        img.verify()
        file.stream.seek(0)
    except Exception:
        return jsonify({"error": "Invalid image file"}), 400

    # Save temporarily
    temp_path = f"/tmp/{uuid.uuid4()}.jpg"
    file.save(temp_path)

    # Run inference
    result = classifier.predict(temp_path)

    # Clean up
    os.remove(temp_path)

    return jsonify(result), 200


# 🔥 THIS WAS MISSING — REQUIRED FOR python3 app.py TO WORK
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
