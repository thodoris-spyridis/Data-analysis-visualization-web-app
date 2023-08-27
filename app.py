from flask import Flask, render_template, url_for, flash, request, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {"xlsx"}

@app.route("/", methods = ["POST", "GET"])
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
