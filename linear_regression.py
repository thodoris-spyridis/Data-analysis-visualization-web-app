from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import explained_variance_score, mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt


# - Split the dataset to train and test data with a test size of 20% of the initial dataset
def train_split(x, y, size):
    '''
    Splits the dataset to training and test data
    '''
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size, random_state=0)
    return x_train, x_test, y_train, y_test

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
def plot_results(column_list, x_test, y_test, y_pred, plot_file):
    var_score = round(explained_variance_score(y_test, y_pred), 3)
    mean_score = round(mean_absolute_error(y_test, y_pred), 3)
    mean_sqr_score = round(mean_squared_error(y_test, y_pred), 3)
    r2 = round(r2_score(y_test, y_pred), 3)
    fig, ax = plt.subplots(nrows=1, ncols=len(column_list), constrained_layout=True, figsize=(17,5), facecolor="#e4f1fe")
    fig.suptitle(f"Explained variance score = {var_score}, Mean absolute score = {mean_score}, Mean squared error = {mean_sqr_score}, R² score = {r2}", fontsize="small")
    for n in range(len(column_list)):
        ax[n].scatter(x=x_test[:, n], y=y_test, marker="o", c="b")
        ax[n].scatter(x=x_test[:, n], y=y_pred, marker="x", c="r")
        ax[n].set_title(f"{column_list[n]}")
        ax[n].set_ylabel("target-prediction")
    plt.savefig(plot_file)
    plt.close()



