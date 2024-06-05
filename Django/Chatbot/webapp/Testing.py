import sys
import pandas as pd
from sklearn.pipeline import Pipeline
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix
import pickle
from sklearn import metrics

class Testing:

    def detecting(test_file,model='rf_model.sav'):

        #train_news = pd.read_csv(train_file)
        test_ = pd.read_csv(test_file, encoding='cp1252')
        
        testdata=test_['Emotion']
        #print(testdata)
        #tfidf = TfidfVectorizer(stop_words='english',use_idf=True,smooth_idf=True) #TF-IDF
        #print(test_['Statement'])

        #knn_pipeline = Pipeline([('lrgTF_IDF', tfidf), ('lrg_mn', KNeighborsClassifier())])

        #pickle.dump(knn_pipeline.fit(train_news['review'], train_news['sentiment']), open(model, 'wb'))
        train = pickle.load(open(model, 'rb'))
        predicted_class = train.predict(test_['Statement'])
        print(model)
        r=Testing.model_assessment(testdata,predicted_class)

        

        return r

    def model_assessment(y_test, predicted_class):
        #print('')
        # Accuracy = (TP + TN) / ALL
        accuracy = accuracy_score(y_test, predicted_class)
        precision = metrics.precision_score(y_test, predicted_class, average='macro')
        recall = metrics.recall_score(y_test, predicted_class, average='macro')
        f1_score = metrics.f1_score(y_test, predicted_class, average='macro')

        print(accuracy, precision, recall, f1_score)

        return accuracy



if __name__ == "__main__":
    Testing.detecting('Testingdata.csv')

