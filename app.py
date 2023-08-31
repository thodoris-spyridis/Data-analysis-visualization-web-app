from flask import Flask, render_template, url_for, flash, request, redirect
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
import datetime
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from flask_wtf.file import FileAllowed

app = Flask(__name__)
app.config["SECRET_KEY"] = "datathodoris1988#"
app.config["UPLOAD_FOLDER"] = "static/files"


class UploadFileForm(FlaskForm):
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
        return "File has been uploaded"
    return render_template("upload.html", year=current_year, form=form)



if __name__ == "__main__":
    app.run(debug=True)
