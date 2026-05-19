import time
import requests
import json
from datetime import datetime

BLUE_URL = "http://localhost:5000/predict-blue"
GREEN_URL = "http://localhost:5000/predict-green"

TEST_IMAGES = [
    "man1.jpg",
    "potatoe.jpg",
    "woman2.jpg"
]

OUTPUT_FILE = "comparison_results.txt"

def call_model(url, image_path):
    with open(image_path, "rb") as f:
        files = {"file": f}
        start = time.time()
        response = requests.post(url, files=files)
        latency = time.time() - start

    try:
        data = response.json()
    except json.JSONDecodeError:
        data = {"error": "Invalid JSON response"}

    return data, latency


def log_result(text):
    with open(OUTPUT_FILE, "a") as f:
        f.write(text + "\n")


def compare_models(image_path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"\n=== Comparison for {image_path} at {timestamp} ===\n"
    print(header)
    log_result(header)

    blue_result, blue_latency = call_model(BLUE_URL, image_path)
    green_result, green_latency = call_model(GREEN_URL, image_path)

    blue_text = f"BLUE -> {blue_result} | latency: {blue_latency:.4f}s"
    green_text = f"GREEN -> {green_result} | latency: {green_latency:.4f}s"

    print(blue_text)
    print(green_text)

    log_result(blue_text)
    log_result(green_text)

    summary = f"Latency difference: {blue_latency - green_latency:.4f}s"
    print(summary)
    log_result(summary)


if __name__ == "__main__":
    for img in TEST_IMAGES:
        compare_models(img)
