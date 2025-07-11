# app.py
from flask import Flask, request, jsonify, send_from_directory
import tensorflow as tf
import numpy as np
import cv2
from pose_vector_utils import extract_pose_vector
import os

app = Flask(__name__)
model = tf.keras.models.load_model("converted_model/model.h5")

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["frame"]
    in_memory_file = file.read()
    np_arr = np.frombuffer(in_memory_file, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    vec = extract_pose_vector(image)  # 22 joint * (x,y) = 44 dim
    prediction = model.predict(vec[None, ...])
    class_id = int(np.argmax(prediction))
    confidence = float(np.max(prediction))

    return jsonify({"class": class_id, "confidence": confidence})

if __name__ == "__main__":
    app.run(debug=True)
