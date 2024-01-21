from sklearn.metrics import explained_variance_score, mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

def simple_encoding(lst):
    '''
    Assignes numbers to unique values
    '''
    temp = {i: j for i, j in enumerate(set(lst))}
    new_lst = [temp[i] for i in lst]
    return new_lst


def plot_polynomial(x, y, y_pred, plot_file, column_names):
    var_score = round(explained_variance_score(y, y_pred), 3)
    mean_score = round(mean_absolute_error(y, y_pred), 3)
    mean_sqr_score = round(mean_squared_error(y, y_pred), 3)
    r2 = round(r2_score(y, y_pred), 3)
    plt.scatter(x, y, color="blue", marker="x")
    plt.plot(x, y_pred, color="red", linewidth=2)
    plt.title(f"Explained variance score = {var_score}, Mean absolute score = {mean_score}, Mean squared error = {mean_sqr_score}, R² Score = {r2}", fontsize="small")
    plt.xlabel(f"{column_names[0]}")
    plt.ylabel(f"{column_names[-1]}")
    plt.savefig(plot_file)
    plt.close()