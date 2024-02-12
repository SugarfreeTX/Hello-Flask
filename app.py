from flask_cors import CORS
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask import Flask, json, jsonify, send_from_directory
import os 
import json
import numpy as np 
import cv2
import io 
import huggingface_hub
from huggingface_hub import InferenceClient
import PIL
from flask import Response

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
SHAPE_FOLDER = 'shape'
app.config['SHAPE_FOLDER'] = SHAPE_FOLDER
client = InferenceClient()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signup/")
def signup():
    return render_template("signup.html")

@app.route("/hello_there/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")


@app.route("/recommends/", methods=['GET'])
def get_recommendations():
    return render_template("get_recommendations.html")

@app.route("/upload/", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file[]']
        if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join(UPLOAD_FOLDER, filename))
        # return redirect(url_for('get_recommendations'))
    return render_template('get_recommendations.html')

@app.route("/upload_shape/", methods=['GET', 'POST'])
def upload_shape():
    if request.method == 'POST':
        f = request.files['file[]']
        if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join(SHAPE_FOLDER, filename))
    return render_template('get_recommendations.html')

@app.route('/model')
def model():
    json_data = json.load(open("./model_js/model.json"))
    return jsonify(json_data)

# # this is the inference function - MIGHT NOT NEED!!
# def inference(text):
#     image = client.text_to_image(text)
#     return image.show()

# this is the get method 
@app.route('/text_to_image', methods=['GET'])
def text_to_image():
    return render_template("text_to_image.html")

# this is the post method
@app.route('/text_to_image', methods=['POST'])
def text_to_image_post():
    text = request.form['text']
    image = client.text_to_image(text)
    # image.save("static/UPLOAD/text_to_image.png")
    image_data = io.BytesIO()
    image.save(image_data, format='PNG')
    image_data.seek(0)
    return Response(image_data, mimetype='image/png')

@app.route('/<path:path>')
def load_shards(path):
    return send_from_directory('model_js', path)

@app.route("/api/data/", methods=['POST'])
def prepare():
    file = request.files['file']
    res = preprocessing(file)
    return json.dumps({"image": res.tolist()})

def preprocessing(file):
    in_memory_file = io.BytesIO()
    file.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    img = cv2.imdecode(data, 1) 
    res = cv2.resize(img, dsize=(224, 224), interpolation=cv2.INTER_CUBIC)
    # file.save("static/UPLOAD/img.png") # saving uploaded img
    # cv2.imwrite("static/UPLOAD/test.png", res) # saving processed image
    return res

if __name__ == '__main__':
    app.run(debug=True)