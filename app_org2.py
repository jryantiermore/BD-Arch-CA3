# import modules and librari
import os
import uuid # ensures unique names for uploaded files
from PIL import Image
from inference.face_inference import FaceClassifier # import my model to determine face or no face
from flask import Flask, request, jsonify
from ingestion.upload_handler import handle_upload   # import my upload routine

app = Flask(__name__) # create an instance of my flask app

# temp safety net during dev but will remove before final submission
classifier = None #load model if available
try:
    classifier = FaceClassifier()
    print("Model loaded successfully.")
except FileNotFoundError:
    print("Model not found. /predict will not work until training is done, remember!!!.")


@app.route("/upload", methods=["POST"]) # set the /upload URl endpoint
def upload(): # creating function for the upload
    if "file" not in request.files:  # make sure a file was present or throws err
        return jsonify({"error": "No file part in request"}), 400
    file = request.files["file"] # extract the uploaded file
    result, error = handle_upload(file)
    if error: # if error return 400 code and if successful return the result plus 200 code
        return jsonify({"error": error}), 400
    return jsonify(result), 200


@app.route("/predict", methods=["POST"]) # set the predict URL endpoint
def predict(): # create prediction function
    if classifier is None: #checks if model failed to load (again, not needed any longer)
        return jsonify({"error": "Model not loaded. Train the model first."}), 400 # response
    if "file" not in request.files: # checks file was loaded and throws err if not
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try: # steps to validate the file 
        img = Image.open(file.stream) # load as image
        img.verify() # verify valid image format
        file.stream.seek(0) # rewind after verify
    except Exception:
        return jsonify({"error": "Invalid image file"}), 400 # returns an error if file not verified

    temp_path = f"/tmp/{uuid.uuid4()}.jpg" # save temp as unique file
    file.save(temp_path)

    result = classifier.predict(temp_path) # run prediction and save result

    os.remove(temp_path) # delete the temp path created for the image being predicted
    return jsonify(result), 200 # send result to VM


if __name__ == "__main__": # boots Flask app and makes is available
    app.run(host="0.0.0.0", port=5000)
