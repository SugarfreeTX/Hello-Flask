import re
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask import Flask
import os 

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


@app.route("/api/data/")
def get_data():
    return app.send_static_file("data.json")

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



if __name__ == '__main__':
    app.run(debug=True)