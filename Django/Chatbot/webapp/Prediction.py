import warnings
import sys

import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

import pickle



class Prediction:

    def do(msg):

        msg=[msg]

        filename = 'rf_model.sav'
        
        train = pickle.load(open(filename, 'rb'))
        predicted_class = train.predict(msg)
        
        return predicted_class[0]



if __name__ == "__main__":
    print(Prediction.do("I hate my lawn mower. If it had a soul, I'd condemn it to the fiery pits of Hell. "))

