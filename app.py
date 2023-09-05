from flask import Flask, render_template, url_for, flash, request, redirect
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
import datetime
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from flask_wtf.file import FileAllowed
import pandas as pd
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = "datathodoris1988#"
app.config["UPLOAD_FOLDER"] = "static/files"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///file-data.db"


db = SQLAlchemy()
db.init_app(app)


class UploadFileForm(FlaskForm):  #upload file form
    file = FileField("File", validators=[InputRequired(), FileAllowed(["xlsx"], "wrong format!")])
    submit = SubmitField("Upload File")


today = datetime.date.today()
current_year = today.year


@app.route("/", methods = ["POST", "GET"])
def upload_file():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data  #Grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], secure_filename(file.filename)))  #Find the root directory and save the file after it is validated as secure
        file_path = f"static/files/{file.filename}"
        data = pd.read_excel(file_path)
        os.remove(file_path)
        flash(f"File {file.filename} has been uploaded")
    return render_template("upload.html", year=current_year, form=form)


@app.route("/data", methods = ["POST", "GET"])
def get_data():
    return render_template("data.html")


if __name__ == "__main__":
    app.run(debug=True)
