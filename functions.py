import os
import numpy as np
from matplotlib import pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

def clear_files_folder():
    '''clears the files folder so we always have one plot to display'''
    dir = r"static\files"
    if len(list(os.scandir(dir))) != 0:
        os.remove(r"static\plots\plot.png")
    else:
        return


# - Encode categorical data
def encode_categorical(x, column_index):
    '''
    Encodes the categorical data
    '''
    ct = ColumnTransformer(transformers=[("encoder", OneHotEncoder(), [column_index])], remainder="passthrough")
    x_new = np.array(ct.fit_transform(x))
    return x_new


def linechart(x_axis, y_axis, y_column, x_column,plot_type, plot_file):
    clear_files_folder()
    plt.plot(x_axis, y_axis, linewidth=2)
    plt.ylabel(y_column)
    plt.xlabel(x_column)
    plt.title(f"{y_column} by {x_column} {plot_type}")
    plt.tight_layout()
    plt.legend(fontsize=5)
    plt.savefig(plot_file)
    plt.close()


def linechart_filled(x_axis, y_axis, y_column, x_column,plot_type, plot_file):
    plt.plot(x_axis, y_axis, linewidth=2)
    plt.ylabel(y_column)
    plt.xlabel(x_column)
    plt.title(f"{y_column} by {x_column} {plot_type}")
    plt.fill_between(x_axis, y_axis, alpha=0.25)
    plt.tight_layout()
    plt.legend(fontsize=5)
    plt.savefig(plot_file)
    plt.close()


def bar_chart(x_axis, y_axis, y_column, x_column,plot_type, plot_file):
    plt.bar(x_axis, y_axis, edgecolor="white", width=10)
    plt.ylabel(y_column)
    plt.xlabel(x_column)
    plt.title(f"{y_column} by {x_column} {plot_type}")
    plt.tight_layout()
    plt.legend(fontsize=5)
    plt.savefig(plot_file)
    plt.close()


def horizontal_bar_chart(x_axis, y_axis, y_column, x_column,plot_type, plot_file):
    plt.barh(x_axis, y_axis, edgecolor="white", height=10)
    plt.ylabel(x_column)
    plt.xlabel(y_column)
    plt.title(f"{y_column} by {x_column} {plot_type}")
    plt.tight_layout()
    plt.legend(fontsize=5)
    plt.savefig(plot_file)
    plt.close()


def histogram(x_axis, x_column,plot_type, plot_file):
    plt.hist(x_axis, bins=5, edgecolor="white")
    plt.xlabel(x_column)
    plt.title(f"{x_column} {plot_type}")
    plt.tight_layout()
    plt.legend(fontsize=5)
    plt.savefig(plot_file)
    plt.close()


def scatter_plot(x_axis, y_axis, y_column, x_column,plot_type, plot_file):
    colors = x_axis
    plt.scatter(x_axis, y_axis, c=colors, cmap="Reds", edgecolor="white", linewidths=1, alpha=0.75)
    plt.title(f"{y_column} by {x_column} {plot_type}")
    plt.tight_layout()
    plt.savefig(plot_file)
    plt.close()