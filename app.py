from flask import Flask, render_template, url_for, flash, request, redirect, session
import datetime
from werkzeug.utils import secure_filename
import os
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
from forms import UploadFileForm, RegistrationForm, LoginForm
import numpy as np
from functions import clear_files_folder, linechart, linechart_filled, bar_chart, horizontal_bar_chart, histogram, scatter_plot, encode_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
# from sklearn.tree import DecisionTreeRegressor
from linear_regression import plot_linear
from polynomial import plot_polynomial, simple_encoding
from svr import plot_svr
# from decision_tree import tree_graph


app = Flask(__name__)
app.config["SECRET_KEY"] = "a1e649990d4f16f4b7984fd0b64f3880"
app.config["UPLOAD_FOLDER"] = "static/files"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user-data.db"


today = datetime.date.today()
current_year = today.year
footer_message = f"© {current_year} Neapolis Univercity Pafos"
matplotlib.use("agg")
plt.style.use("ggplot")
plot_file = os.path.join("static", "plots", "plot.png")


file_check = False
@app.route("/", methods=["POST", "GET"])
def upload_file():
    global data
    global file_check
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
        flash("Only excel files are supported")
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
            elif action == "standard deviation":
                result = data[column_name].std()
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


@app.route("/plot", methods=["POST", "GET"])
def plot():
    plot_pic = os.path.join("static", "plots", "plot.png")
    return render_template("plot.html", plot_img=plot_pic)


@app.route("/plot_predict", methods=["POST", "GET"])
def plot_predict():
    plot_pic = os.path.join("static", "plots", "plot.png")
    if request.method == "POST":
        features = request.form["feature-values"].split(",")
        feature_list = [float(x) for x in features]
        prediction = regressor.predict([np.array(feature_list)])
        flash(f"Prediction = {prediction}")
    return render_template("plot_predict.html", plot_img=plot_pic)


@app.route("/plot_predict_poly", methods=["POST", "GET"])
def plot_predict_poly():
    plot_pic = os.path.join("static", "plots", "plot.png")
    if request.method == "POST":
        features = request.form["feature-values"].split(",")
        feature_list = [float(x) for x in features]
        prediction = regressor.predict(linear_reg_poly.fit_transform([np.array(feature_list)]))
        flash(f"Prediction = {prediction}")
    return render_template("plot_predict.html", plot_img=plot_pic)


@app.route("/plot_predict_svr", methods=["POST", "GET"])
def plot_predict_svr():
    plot_pic = os.path.join("static", "plots", "plot.png")
    if request.method == "POST":
        features = request.form["feature-values"].split(",")
        feature_list = [float(x) for x in features]
        prediction = scaler_y.inverse_transform(regressor.predict(scaler_x.transform([np.array(feature_list)])).reshape(-1,1))
        flash(f"Prediction = {prediction}")
    return render_template("plot_predict.html", plot_img=plot_pic)


@app.route("/visualize", methods=["POST", "GET"])
def visualize():
    plt.figure(figsize=(14, 5), facecolor="#e4f1fe")
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
            linechart(x_axis, y_axis, y_column, x_column, plot_type, plot_file)
            return redirect(url_for("plot"))
        if plot_type == "Linechart-filled":
            clear_files_folder()
            linechart_filled(x_axis, y_axis, y_column, x_column, plot_type, plot_file)
            return redirect(url_for("plot"))
        elif plot_type == "Bar-chart":
            clear_files_folder()
            bar_chart(x_axis, y_axis, y_column, x_column, plot_type, plot_file)
            return redirect(url_for("plot"))
        elif plot_type == "Horizontal-bar-chart":
            clear_files_folder()
            horizontal_bar_chart(x_axis, y_axis, y_column, x_column, plot_type, plot_file)
            return redirect(url_for("plot"))
        elif plot_type == "Histogram":
            clear_files_folder()
            histogram(x_axis, x_column,plot_type, plot_file)
            return redirect(url_for("plot"))
        elif plot_type == "Scatter-plot":
            clear_files_folder()
            scatter_plot(x_axis, y_axis, y_column, x_column, plot_type, plot_file)
            return redirect(url_for("plot"))
    return render_template("visualize.html", columns=column_names, footter_message=footer_message)


@app.route("/linear_regression", methods=["POST", "GET"])
def linear_regression():
    if file_check == False:
        return redirect(url_for("no_data"))
    else:
        column_names = data.columns[:-1]
        column_list = list(column_names)
        global x
        x = data.iloc[:, :-1].values
        y = data.iloc[:, -1].values
    if request.method == "POST":
        if request.form["categorical-column"] != "None":
            column_index = data.columns.get_loc(request.form["categorical-column"])
            x = encode_categorical(x, column_index)
        size = float(request.form["percent-input"]) / 100
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size, random_state=0) 
        global regressor
        regressor = LinearRegression()
        regressor.fit(x_train, y_train)
        y_pred = regressor.predict(x_test)
        clear_files_folder()
        plot_linear(column_list, x_test, y_test, y_pred, plot_file) 
        return redirect(url_for("plot_predict"))
    return render_template("linear_regression.html", columns=column_names,  footter_message=footer_message)


@app.route("/polynomial", methods=["POST", "GET"])
def polynomial():
    if file_check == False:
        return redirect(url_for("no_data"))
    else:
        column_names = data.columns[:-1]
        global x
        x = data.iloc[:, -2:-1].values
        y = data.iloc[:, -1].values
    if request.method == "POST":
        if request.form["categorical-column"] != "None":
            x = np.array(simple_encoding(list(x)))
        degree = int(request.form["degree"])
        global regressor
        global linear_reg_poly
        linear_reg_poly = PolynomialFeatures(degree=degree)
        x_poly = linear_reg_poly.fit_transform(x)
        regressor = LinearRegression()
        regressor.fit(x_poly, y)
        y_pred_poly = regressor.predict(x_poly)
        clear_files_folder()
        plt.figure(figsize=(14, 5), facecolor="#e4f1fe")
        plot_polynomial(x, y, y_pred_poly, plot_file, data.columns) 
        return redirect(url_for("plot_predict_poly"))
    return render_template("polynomial.html", columns=column_names,  footter_message=footer_message)


@app.route("/non_linear_svr", methods=["POST", "GET"])
def non_linear_svr():
    if file_check == False:
        return redirect(url_for("no_data"))
    else:
        column_names = data.columns[:-1]
        global x
        x = data.iloc[:, -2:-1].values
        y = data.iloc[:, -1].values.reshape(-1,1)
    if request.method == "POST":
        global scaler_y     
        global scaler_x   
        scaler_x = StandardScaler()
        scaler_y = StandardScaler()
        x = scaler_x.fit_transform(x)
        y = scaler_y.fit_transform(y)
        global regressor
        regressor = SVR(kernel="rbf")
        regressor.fit(x, y)
        y_pred_svr = scaler_y.inverse_transform(regressor.predict(x).reshape(-1,1))
        clear_files_folder()
        plt.figure(figsize=(14, 5), facecolor="#e4f1fe")
        plot_svr(scaler_x, scaler_y, x, y, y_pred_svr, plot_file, column_names)
        return redirect(url_for("plot_predict_svr"))
    return render_template("svr.html", columns=column_names,  footter_message=footer_message)


# @app.route("/decision_tree", methods=["POST", "GET"])
# def decision_tree():
#     if file_check == False:
#         return redirect(url_for("no_data"))
#     else:
#         column_names = data.columns[:-1]
#         x = data.iloc[:, :-1].values
#         y = data.iloc[:, -1].values
#     if request.method == "POST":
#         if request.form["categorical-column"] != "None":
#             column_index = data.columns.get_loc(request.form["categorical-column"])
#             x = encode_categorical(x, column_index)
#         tree_reg = DecisionTreeRegressor(max_depth=3, random_state=1234)
#         tree_reg.fit(x, y)      
#         feature_names=list(data.columns)[:-1] 
#         clear_files_folder()
#         tree_graph(tree_reg, plot_file, feature_names)
#         return redirect(url_for("plot"))
#     return render_template("decision_tree.html", columns=column_names,  footter_message=footer_message)


if __name__ == "__main__":
    app.run(debug=True)