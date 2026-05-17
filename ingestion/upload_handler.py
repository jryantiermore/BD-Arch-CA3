# ingestion/upload_handler.py
# details the upload logic

import os
import uuid
from werkzeug.utils import secure_filename
from PIL import Image

from ingestion.preprocess import preprocess_image
from ingestion.metadata import log_metadata

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_image(file):
    """Ensure the uploaded file is a real image."""
    try:
        img = Image.open(file.stream)
        img.verify()
        file.stream.seek(0)
        return True
    except Exception:
        return False


def save_raw_file(file, unique_name):
    """Save the raw uploaded file to disk."""
    raw_path = os.path.join(RAW_DIR, secure_filename(unique_name))
    file.save(raw_path)
    return raw_path


def generate_unique_filename(original_name):
    ext = original_name.rsplit(".", 1)[1].lower()
    return f"{uuid.uuid4()}.{ext}"


def handle_upload(file):
    """Main entry point for ingestion logic."""
    if file.filename == "":
        return None, "No file selected"

    if not allowed_file(file.filename):
        return None, "Unsupported file type"

    if not validate_image(file):
        return None, "Invalid image file"

    # Generate unique name and save raw file
    unique_name = generate_unique_filename(file.filename)
    raw_path = save_raw_file(file, unique_name)

    # Preprocess the image
    processed_path = os.path.join(PROCESSED_DIR, unique_name)
    preprocess_info = preprocess_image(raw_path, processed_path)

    # Metadata logging
    file_size = os.path.getsize(raw_path)
    log_metadata(
        filename=unique_name,
        raw_path=raw_path,
        processed_path=processed_path,
        file_size=file_size,
        faces_found=preprocess_info["faces_found"],
	width=preprocess_info["width"],
	height=preprocess_info["height"]
    )

    # Return structured response
    return {
        "filename": unique_name,
        "raw_path": raw_path,
        "processed_path": processed_path,
	"faces_found": preprocess_info["faces_found"],
        "dimensions": {
            "width": preprocess_info["width"],
            "height": preprocess_info["height"]
        }
    }, None
