from sklearn.linear_model import LinearRegression
from sklearn.metrics import explained_variance_score, mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt


# - Fit, train and test the model 
def linear_regression_train(x_train, y_train, x_test):
    '''
    Fits the model to the training data and runs the prediction 
    on the test data
    '''
    regressor = LinearRegression()
    regressor.fit(x_train, y_train)
    y_pred = regressor.predict(x_test) 
    return y_pred   

#plot the test results vs the target
def plot_linear(column_list, x_test, y_test, y_pred, plot_file):
    var_score = round(explained_variance_score(y_test, y_pred), 3)
    mean_score = round(mean_absolute_error(y_test, y_pred), 3)
    mean_sqr_score = round(mean_squared_error(y_test, y_pred), 3)
    fig, ax = plt.subplots(nrows=1, ncols=len(column_list), constrained_layout=True, figsize=(17,5), facecolor="#e4f1fe")
    fig.suptitle(f"Explained variance score = {var_score}, Mean absolute score = {mean_score}, Mean squared error = {mean_sqr_score}", fontsize="small")
    for n in range(len(column_list)):
        ax[n].scatter(x=x_test[:, n], y=y_test, marker="o", c="b")
        ax[n].scatter(x=x_test[:, n], y=y_pred, marker="x", c="r")
        ax[n].set_title(f"{column_list[n]}")
        ax[n].set_ylabel("target-prediction")
    plt.savefig(plot_file)
    plt.close()



