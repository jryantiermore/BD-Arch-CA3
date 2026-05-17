import time
import requests
import json

BLUE_URL = "http://localhost:5001/predict"
GREEN_URL = "http://localhost:5002/predict"

TEST_IMAGES = [
    "man1.jpg",
    "potatoe.jpg",
    "woman2.jpg"
]

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


def compare_models(image_path):
    print(f"\n=== Comparing Blue vs Green for {image_path} ===\n")

    blue_result, blue_latency = call_model(BLUE_URL, image_path)
    green_result, green_latency = call_model(GREEN_URL, image_path)

    print("🔵 BLUE MODEL")
    print(f"Prediction: {blue_result}")
    print(f"Latency: {blue_latency:.4f} sec\n")

    print("🟢 GREEN MODEL")
    print(f"Prediction: {green_result}")
    print(f"Latency: {green_latency:.4f} sec\n")

    print("=== Summary ===")
    print(f"Blue latency:  {blue_latency:.4f} sec")
    print(f"Green latency: {green_latency:.4f} sec")
    print("\nDone.\n")


if __name__ == "__main__":
    for img in TEST_IMAGES:
        compare_models(img)
