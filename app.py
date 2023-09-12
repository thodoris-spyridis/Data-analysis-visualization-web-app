from flask import Flask, render_template, url_for, flash, request, redirect, render_template_string
from flask_plots import Plots
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
plots = Plots(app)
app.config["SECRET_KEY"] = "datathodoris1988#"
app.config["UPLOAD_FOLDER"] = "static/files"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///file-data.db"


db = SQLAlchemy()
db.init_app(app)


class UploadFileForm(FlaskForm):  # upload file form
    file = FileField(
        "File", validators=[InputRequired(), FileAllowed(["xlsx"], "wrong format!")]
    )
    submit = SubmitField("Upload File")


today = datetime.date.today()
current_year = today.year


@app.route("/", methods=["POST", "GET"])
def upload_file():
    global my_data
    global file_check
    file_check = False

    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data  # Grab the file
        file.save(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                app.config["UPLOAD_FOLDER"],
                secure_filename(file.filename),
            )
        )  # Find the root directory and save the file after it is validated as secure
        file_path = f"static/files/{file.filename}"
        my_data = pd.read_excel(file_path, dtype=object)
        my_data = my_data.reset_index(drop=True)
        os.remove(file_path)
        file_check = True
        flash(f"File {file.filename} has been uploaded")
    else:
        flash("No file")
    return render_template("upload.html", year=current_year, form=form)


@app.route("/no_data", methods=["POST", "GET"])
def no_my_data():
    flash("No data available!")
    return render_template("no_data.html")


@app.route("/data", methods=["POST", "GET"])
def get_data():
    if file_check == False:
        return redirect("/no_data")
    else:
        display_rows = my_data[0:10]
        column_names = display_rows.columns
        row_count = my_data.shape[0]
        column_count = my_data.shape[1]
    if request.method == "POST":
        column_name = request.form["column-name"]
        action = request.form["action"]
        try:
            if action == "average":
                result = round(my_data[column_name].mean(), 2)
            elif action == "min":
                result = my_data[column_name].min()
            elif action == "max":
                result = my_data[column_name].max()
            else:
                unique_values = {value for value in my_data[column_name].to_list()}
                result = len(unique_values)
        except:
            flash("Action can not be performed on this column")
        else:
            flash(f"{action}: {result}")
    return render_template(
        "data.html",
        year=current_year,
        preview=display_rows,
        columns=column_names,
        all_my_data=my_data,
        number_of_rows=row_count,
        number_of_columns=column_count
    )


if __name__ == "__main__":
    app.run(debug=True)
