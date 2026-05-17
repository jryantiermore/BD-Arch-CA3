# ingestion/metadata.py
# keeping this to bare min to allow for training
# generates the metadata CSV file in the data folder
# appends a new row for each upload

import csv
import os
from datetime import datetime

METADATA_FILE = "data/metadata.csv"

# Ensure metadata file exists with headers
def init_metadata_file():
    if not os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "filename",
                "raw_path",
                "processed_path",
                "file_size_bytes",
		"faces_found",
		"width",
		"height",
                "timestamp"
            ])

def log_metadata(filename, raw_path, processed_path, file_size, faces_found, width, height):
    init_metadata_file()
    with open(METADATA_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            filename,
            raw_path,
            processed_path,
            file_size,
	    faces_found,
	    width,
	    height,
            datetime.utcnow().isoformat()
        ])
