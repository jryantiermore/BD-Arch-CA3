# app.py
# ensures only JPG/PNG files allowed
# UUIDs prevent collisions and allow Kubernetes scale more easily...overkill here
# Data in data/raw/ for preprocessing
# JSON can be logged to CSV or elsewhere later

import os
import uuid
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
from ingest.metadata import log_metadata # added with set-up of metadata logging
from ingest.preprocess import preprocess_image #updated after creating preprocess.py

app = Flask(__name__)

# Directory for raw uploads
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/preprocessed"

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type"}), 400

    # Generate unique filename
    ext = file.filename.rsplit(".", 1)[1].lower()
    unique_name = f"{uuid.uuid4()}.{ext}"


    raw_path = os.path.join(RAW_DIR, secure_filename(unique_name))
    processed_path = os.path.join(PROCESSED_DIR, secure_filename(unique_name))

    # Validate image by attempting to open it
    try:
        img = Image.open(file.stream)
        img.verify()  # ensures it's a real image
    except Exception:
        return jsonify({"error": "Invalid image file"}), 400

    # Save raw file
    file.stream.seek(0)  # reset pointer after verify()
    file.save(raw_path)

    # file size
    file_size = os.path.getsize(raw_path) # also added for metadata

    # run preprocessing
    preprocess_info = preprocess_image(raw_path, processed_path)

    # log metadata (added)
    log_metadata(
	filename=unique_name,
	raw_path=raw_path,
	processed_path=processed_path,
	file_size=file_size,
	status="uploaded_and_preprocessed"
    )


    return jsonify({
        "filename": unique_name,
        "raw_path": raw_path,
        "processed_path": preprocess_info["processed_path"],
        "dimensions": {
            "width": preprocess_info["width"],
            "height": preprocess_info["height"]
        },
        "status": "uploaded_and_preprocessed"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

