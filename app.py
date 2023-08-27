from flask import Flask, render_template, url_for, flash, request, redirect
from werkzeug.utils import secure_filename
import datetime

app = Flask(__name__)

today = datetime.date.today()
current_year = today.year
print(current_year)

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {"xlsx"}

@app.route("/", methods = ["POST", "GET"])
def home():
    return render_template("home.html", year=current_year)


if __name__ == "__main__":
    app.run(debug=True)
