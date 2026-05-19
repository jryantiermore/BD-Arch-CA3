# import modules and librari
import os
import uuid # ensures unique names for uploaded files
from PIL import Image
from inference.face_inference import FaceClassifier # import my model to determine face or no face
from flask import Flask, request, jsonify
from ingestion.upload_handler import handle_upload   # import my upload routine

app = Flask(__name__) # create an instance of my flask app

classifier_blue = None
classifier_green = None

try:
    classifier_blue = FaceClassifier(model_path="/models/blue.pkl")
    classifier_green = FaceClassifier(model_path="/models/green.pkl")
    print("Blue and Green models loaded.")
except FileNotFoundError:
    print("One or both models missing.")


@app.route("/upload", methods=["POST"]) # set the /upload URl endpoint
def upload(): # creating function for the upload
    if "file" not in request.files:  # make sure a file was present or throws err
        return jsonify({"error": "No file part in request"}), 400
    file = request.files["file"] # extract the uploaded file
    result, error = handle_upload(file)
    if error: # if error return 400 code and if successful return the result plus 200 code
        return jsonify({"error": error}), 400
    return jsonify(result), 200


# two new endpoints for blue green
@app.route("/predict-blue", methods=["POST"])
def predict_blue():
    return run_prediction(classifier_blue)

@app.route("/predict-green", methods=["POST"])
def predict_green():
    return run_prediction(classifier_green)


# function to avoid duplication
def run_prediction(model):
    if model is None:
        return jsonify({"error": "Model not loaded"}), 400

    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        img = Image.open(file.stream)
        img.verify()
        file.stream.seek(0)
    except Exception:
        return jsonify({"error": "Invalid image file"}), 400

    temp_path = f"/tmp/{uuid.uuid4()}.jpg"
    file.save(temp_path)

    result = model.predict(temp_path)
    os.remove(temp_path)

    return jsonify(result), 200


if __name__ == "__main__": # boots Flask app and makes is available
    app.run(host="0.0.0.0", port=5000)
