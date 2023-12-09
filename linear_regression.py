import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression


# - Encode categorical data
def encode_categorical(x, column_index):
    '''
    Encodes the categorical data
    '''
    ct = ColumnTransformer(transformers=[("encoder", OneHotEncoder(), [column_index])], remainder="passthrough")
    x_new = np.array(ct.fit_transform(x))
    return x_new

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


