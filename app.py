from flask import Flask, render_template, url_for, flash, request, redirect
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
import datetime
from werkzeug.utils import secure_filename
import os, glob
from wtforms.validators import InputRequired
from flask_wtf.file import FileAllowed
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.figure import Figure



app = Flask(__name__)
app.config["SECRET_KEY"] = "datathodoris1988#"
app.config["UPLOAD_FOLDER"] = "static/files"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///file-data.db"


db = SQLAlchemy()
db.init_app(app)


class UploadFileForm(FlaskForm):  # upload file form
    file = FileField("File", validators=[InputRequired(), FileAllowed(["xlsx"], "wrong format!")])
    submit = SubmitField("Upload File")


today = datetime.date.today()
current_year = today.year


def clear_files_folder():
    '''clears the files folder so we have on plot to display every time it runs'''
    dir = r"static\files"
    if len(list(os.scandir(dir))) != 0:
        os.remove(r"static\files\plot.png")
    else:
        return


@app.route("/", methods=["POST", "GET"])
def upload_file():
    global data
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
        data = pd.read_excel(file_path, dtype=object)
        data = data.reset_index(drop=True)
        os.remove(file_path)
        file_check = True
        flash(f"File {file.filename} has been uploaded")
    else:
        flash("No file")
    return render_template("upload.html", year=current_year, form=form)


@app.route("/no_data", methods=["POST", "GET"])
def no_data():
    flash("No data available!")
    return render_template("no_data.html")


@app.route("/data", methods=["POST", "GET"])
def get_data():
    if file_check == False:
        return redirect("/no_data")
    else:
        display_rows = data[0:10]
        column_names = display_rows.columns
        row_count = data.shape[0]
        column_count = data.shape[1]
    if request.method == "POST":
        clear_files_folder()
        column_name = request.form["column-name"]
        action = request.form["action"]
        try:
            if action == "average":
                result = round(data[column_name].mean(), 2)
            elif action == "min":
                result = data[column_name].min()
            elif action == "max":
                result = data[column_name].max()
            else:
                unique_values = {value for value in data[column_name].to_list()}
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
        all_data=data,
        number_of_rows=row_count,
        number_of_columns=column_count
    )


@app.route("/visualize", methods=["POST", "GET"])
def visualize():
    matplotlib.use("agg")
    plt.style.use("fivethirtyeight")
    plot_file = os.path.join("static", "files", "plot.png")
    if file_check == False:
        return redirect("/no_data")
    else:
        column_names = data.columns
    if request.method == "POST":
        x_column = request.form["x-axis"]
        y_column = request.form["y-axis"]
        x_axis = data[x_column].to_list()
        y_axis = data[y_column].to_list()
        plot_type = request.form["plot-type"]
        if plot_type == "Linechart":
            clear_files_folder()
            plt.plot(x_axis, y_axis)
            plt.ylabel(y_column)
            plt.xlabel(x_column)
            plt.title(f"{y_column} by {x_column} {plot_type}")
            plt.tight_layout()
            plt.savefig(plot_file)
            plt.close()
        elif plot_type == "Bar-chart":
            clear_files_folder()
            plt.bar(x_axis, y_axis)
            plt.ylabel(y_column)
            plt.xlabel(x_column)
            plt.title(f"{y_column} by {x_column} {plot_type}")
            plt.tight_layout()
            plt.savefig(plot_file)
            plt.close()
    return render_template("visualize.html", columns=column_names, plot_pic=plot_file)




if __name__ == "__main__":
    app.run(debug=True)