import pandas as pd
import numpy as np
from app import data
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression



# - We need to encode the categorical data (State [index 3] in this case)
def encode_categorical(x, column_index):
    '''
    Encodes the categorical data
    '''

    ct = ColumnTransformer(transformers=[("encoder", OneHotEncoder(), [column_index])], remainder="passthrough")
    x_new = np.array(ct.fit_transform(x))
    return x_new

# - Split the dataset to train and test data with a test size of 20% of the initial dataset
def train_split(x, y, size, random):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size, random_state=random)
    return x_train, x_test, y_train, y_test


# - Fit and train the model
# regressor = LinearRegression()
# regressor.fit(x_train, y_train)

# - Predict the test dataset and show the prediction next to the test poredictions
# y_pred = regressor.predict(x_test)


# np.set_printoptions(precision=2) #show values with 2 decimal precision
# print(np.concatenate((y_pred.reshape(len(y_pred), 1), y_test.reshape(len(y_test), 1)), axis=1))