
import numpy.random as numrandom
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC
from sklearn import svm
from sklearn.svm import LinearSVC
from sklearn import metrics


def classfy():
    # Split the data into columns and read

    datainput = pd.read_csv("dataset.csv")
    # Set the outcome and dedlete it
    y = datainput['State']
    del datainput['State']
    # Split data into Test & Training set where test data is 30% & raining data is 70%
    x_train, x_test, y_train, y_test = train_test_split(datainput, y, test_size=0.3)

    # Next use Bayesian Classifier
    classify3 = BernoulliNB()
    # Train the model
    classify3.fit(x_train, y_train)
    # Use the model on the test data
    predicted3 = classify3.predict(x_test)
    nb = metrics.accuracy_score(y_test, predicted3) * 100
    print("The accuracy score using the Naive Bayes Classifier is ->")
    print(metrics.accuracy_score(y_test, predicted3))
    print('---------------------------------------------- ')

    


