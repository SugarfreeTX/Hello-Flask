from flask_cors import CORS
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask import Flask, json, jsonify, send_from_directory
import os 
import json
import numpy as np 
import cv2

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
SHAPE_FOLDER = 'shape'
app.config['SHAPE_FOLDER'] = SHAPE_FOLDER

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


@app.route("/api/data/", methods=['POST'])
def prepare():
    file = request.files['file']
    res = preprocessing(file)
    return json.dumps({"image": res.tolist()})

@app.route("/recommends/")
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

# @app.route('/model')
# def model():
#     json_data = json.load(open("./model_js/model.json"))
#     return jsonify(json_data)


# @app.route('/<path:path>')
# def load_shards(path):
#     return send_from_directory('model_js', path)

def preprocessing(file):
    in_memory_file = io.BytesIO()
    file.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    img = cv2.imdecode(data, 0)
    res = cv2.resize(img, dsize=(28, 28), interpolation=cv2.INTER_CUBIC)
    # file.save("static/UPLOAD/img.png") # saving uploaded img
    # cv2.imwrite("static/UPLOAD/test.png", res) # saving processed image
    return res

if __name__ == '__main__':
    app.run(debug=True)