from flask import Flask, render_template, url_for, flash, request, redirect
import datetime
from werkzeug.utils import secure_filename
import os
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
from forms import UploadFileForm, RegistrationForm, LoginForm
import numpy as np
from functions import clear_files_folder, linechart, linechart_filled, bar_chart, horizontal_bar_chart, histogram, scatter_plot


app = Flask(__name__)
app.config["SECRET_KEY"] = "a1e649990d4f16f4b7984fd0b64f3880"
app.config["UPLOAD_FOLDER"] = "static/files"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user-data.db"


today = datetime.date.today()
current_year = today.year
footer_message = f"© {current_year} Neapolis Univercity Pafos"



@app.route("/", methods=["POST", "GET"])
def upload_file():
    global data
    global file_check
    file_check = False

    file_form = UploadFileForm()
    if file_form.validate_on_submit():
        file = file_form.file.data  # Grab the file
        file.save(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                app.config["UPLOAD_FOLDER"],
                secure_filename(file.filename),
            )
        )  # Find the root directory and save the file after it is validated as secure
        file_path = f"static/files/{file.filename}".replace(" ", "_")
        data = pd.read_excel(file_path)
        data = data.reset_index(drop=True)
        os.remove(file_path)
        file_check = True
        flash(f"File {file.filename} has been uploaded", "success")
    else:
        flash("No file")
    return render_template("upload.html", footter_message=footer_message, form=file_form)


@app.route("/register", methods=["POST", "GET"])
def register():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        flash(f"Account created for {register_form.username.data}.", "success")
        return redirect(url_for("upload_file"))
    return render_template("register.html", footter_message=footer_message, form=register_form)


@app.route("/login", methods=["POST", "GET"])
def login():
    login_form = LoginForm()
    return render_template("login.html", footter_message=footer_message, form=login_form)



@app.route("/no_data", methods=["POST", "GET"])
def no_data():
    flash("No data available!")
    return render_template("no_data.html", footter_message=footer_message)


@app.route("/data", methods=["POST", "GET"])
def get_data():
    if file_check == False:
        return redirect(url_for("no_data"))
    else:
        column_names = data.columns
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
            elif action == "sum":
                result = data[column_name].sum()
            else:
                unique_values = {value for value in data[column_name].to_list()}
                result = len(unique_values)
        except:
            flash("Action can not be performed on this column")
        else:
            flash(f"{action}: {result}")
    return render_template(
        "data.html",
        footter_message=footer_message,
        preview=data,
        columns=column_names,
        all_data=data,
        number_of_rows=row_count,
        number_of_columns=column_count
    )


@app.route("/visualize", methods=["POST", "GET"])
def visualize():
    matplotlib.use("agg")
    plt.style.use("ggplot")
    plt.figure(figsize=(14, 5), facecolor="#e4f1fe")
    plot_file = os.path.join("static", "plots", "plot.png")
    img_check = False
    if file_check == False:
        return redirect(url_for("no_data"))
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
            linechart(x_axis, y_axis, y_column, x_column,plot_type, plot_file)
        if plot_type == "Linechart-filled":
            clear_files_folder()
            linechart_filled(x_axis, y_axis, y_column, x_column,plot_type, plot_file)
        elif plot_type == "Bar-chart":
            clear_files_folder()
            bar_chart(x_axis, y_axis, y_column, x_column,plot_type, plot_file)
        elif plot_type == "Horizontal-bar-chart":
            clear_files_folder()
            horizontal_bar_chart(x_axis, y_axis, y_column, x_column,plot_type, plot_file)
        elif plot_type == "Histogram":
            clear_files_folder()
            histogram(x_axis, x_column,plot_type, plot_file)
        elif plot_type == "Scatter-plot":
            clear_files_folder()
            scatter_plot(x_axis, y_axis, y_column, x_column,plot_type, plot_file)
        img_check = True
    return render_template("visualize.html", columns=column_names, plot_pic=plot_file, footter_message=footer_message, img_check=img_check)


if __name__ == "__main__":
    app.run(debug=True)