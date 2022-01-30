"""
Data Literacy - WiSe 21
Project: Assessment of Spotify Chart Preferences across Different Countries
Authors: Florian Kriegel (5746680), Jonathan Waehrer (5776535)

Purpose of this script performs linear and logistic regression on pre-selected song features to predict the popularity
of a song.
"""
# --------------------------------------------------- PACKAGES ------------------------------------------------------- #
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import make_scorer
from sklearn.linear_model import LogisticRegression


# ---------------------------------------------- FUNCTIONS/UTILITY --------------------------------------------------- #
def get_root_mean_squared_error(predictions, labels):
    rmse = 0
    for pred, label in zip(predictions, labels):
        rmse += (label - pred) ** 2
    return np.sqrt(1 / len(predictions) * rmse)


def print_linear_regression_performance(reg, X_train, X_test, y_train, y_test):
    """
    Prints training, CV and test RMSE for a trained linear regression model.

    Parameters
    ----------
    reg
    X_train
    X_test
    y_train
    y_test

    Returns
    -------

    """
    predictions = reg.predict(X_train)
    rmse = np.sqrt(mean_squared_error(y_train, predictions))
    print(f'train error: {rmse}')

    # cross validation
    model = LinearRegression()
    scorer = make_scorer(get_root_mean_squared_error)
    cv = KFold(n_splits=5, shuffle=True)
    scores = cross_val_score(model, X_train, y_train, cv=cv, scoring=scorer)
    print(f'mean cross validation error: {scores.mean()}')

    # get test error
    predictions_training = reg.predict(X_test)
    print(f'test error: {np.sqrt(mean_squared_error(y_test, predictions_training))}')


def print_log_regression_performance(clf, X_train, X_test, y_train, y_test):
    print(f'training score: {clf.score(X_train, y_train)}')
    print(f'test score: {clf.score(X_test, y_test)}')


def train_linear_regression_model(X_train, y_train):
    # perform linear regerssion and evaluate
    reg = LinearRegression().fit(X_train, y_train)
    return reg


def train_logistic_regression_model(X_train, y_train):
    clf = LogisticRegression().fit(X_train, y_train)
    return clf


def get_logistic_regression_data_sets(y, training_data):
    """
    binaryzes popularity by setting all values above 50 to one, all other to zero. Next, a split of the data in test and
    training set is performed.
    :param y: labels
    :param training_data: data
    :return: training and test data sets
    """
    y_logistic = np.zeros(len(y))
    y_logistic[y > 50] = 1
    # split data into test and training set
    X_train, X_test, y_train, y_test = train_test_split(training_data, y_logistic, test_size=0.33,
                                                        random_state=42)
    return X_train, X_test, y_train, y_test


def create_four_fearure_data_set(training_data):
    """
    extracts the four most informative features from data and creates new training set with it
    """
    training_data_four_params = training_data[['danceability', 'energy', 'valence', 'loudness']]
    return training_data_four_params


# ---------------------------------------------------- MAIN ---------------------------------------------------------- #
def main():
    # read in data
    training_data = pd.read_csv('../dat/training_data.csv')
    y = pd.read_csv('../dat/response.csv').values[:, 0]

    # linear regression
    print('\nlinear regression:')
    X_train, X_test, y_train, y_test = train_test_split(training_data, y, test_size=0.33, random_state=42)
    reg = train_linear_regression_model(X_train, y_train)
    print_linear_regression_performance(reg, X_train, X_test, y_train, y_test)

    # logistic regression
    print('\nlogistic regression:')
    X_train, X_test, y_train, y_test = get_logistic_regression_data_sets(y, training_data)
    log_reg = train_logistic_regression_model(X_train, y_train)
    print_log_regression_performance(log_reg, X_train, X_test, y_train, y_test)

    # logistic regression on four features
    print('\nlogistic regression on four most informative features:')
    training_data_four_params = create_four_fearure_data_set(training_data)
    X_train, X_test, y_train, y_test = get_logistic_regression_data_sets(y, training_data_four_params)
    log_reg = train_logistic_regression_model(X_train, y_train)
    print_log_regression_performance(log_reg, X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    main()
