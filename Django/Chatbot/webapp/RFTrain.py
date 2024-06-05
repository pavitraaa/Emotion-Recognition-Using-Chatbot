import sys
import pandas as pd
from sklearn.pipeline import Pipeline
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn import svm

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix
import pickle

class RFTrain:

    def train(train_file):
        train = pd.read_csv(train_file,encoding='cp1252')
        tfidf = TfidfVectorizer(stop_words='english',use_idf=True,smooth_idf=True) #TF-IDF
        print("Start RF Classification")
        pipeline = Pipeline([('lrgTF_IDF', tfidf), ('lrg_mn', RandomForestClassifier(criterion="gini", n_estimators = 100))])
        
        filename = 'rf_model.sav'
        pickle.dump(pipeline.fit(train['Statement'], train['Emotion']), open(filename, 'wb'))

        print("RF Model Successfully Trained")

