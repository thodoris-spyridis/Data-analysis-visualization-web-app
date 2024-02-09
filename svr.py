import matplotlib.pyplot as plt
from sklearn.metrics import explained_variance_score, mean_absolute_error, mean_squared_error, r2_score

def plot_svr(scaler_x, scaler_y, x, y, y_pred_svr, plot_file, column_names):
    var_score = round(explained_variance_score(y, scaler_y.inverse_transform(y).reshape(-1,1)), 3)
    mean_score = round(mean_absolute_error(y, scaler_y.inverse_transform(y).reshape(-1,1)), 3)
    mean_sqr_score = round(mean_squared_error(y, scaler_y.inverse_transform(y).reshape(-1,1)), 3)/2
    r2 = round(r2_score(y, scaler_y.inverse_transform(y).reshape(-1,1)), 3)
    plt.scatter(scaler_x.inverse_transform(x).reshape(-1,1), scaler_y.inverse_transform(y).reshape(-1,1), color="blue", marker="x")
    plt.plot(scaler_x.inverse_transform(x).reshape(-1,1), y_pred_svr, color="red", linewidth=2)
    plt.title(f"Explained variance score = {var_score}, Mean absolute score = {mean_score}, Mean squared error = {mean_sqr_score}, R² Score = {r2}", fontsize="small")
    plt.xlabel(f"{column_names[0]}")
    plt.ylabel(f"{column_names[-1]}")
    plt.savefig(plot_file)
    plt.close()

