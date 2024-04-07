# Gradient boosted tree classifier

import numpy as np
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
from imblearn.over_sampling import SMOTE
from models.clean_up import clean_up
from models.abstract_model import abstract_model


def train_model():
    data = pd.read_csv('fraudTrain.csv')
    features = ['trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt', 'city', 'job', 'dob', 'is_fraud']
    data = data[features]
    data.dropna(ignore_index=True)
    x_train = data.iloc[:, :-1]
    y_train = data.iloc[:, -1:]
    x_train, encoder = clean_up(x_train)

    test = pd.read_csv('fraudTest.csv')
    test = test[features]
    x_test = test.iloc[:, :-1]
    y_test = test.iloc[:, -1:]
    x_test = clean_up(x_test, encoder)[0]

    x_train, y_train = SMOTE().fit_resample(x_train, y_train)

    model = HistGradientBoostingClassifier(learning_rate=0.1)
    model.fit(x_train, y_train)

    return model, encoder

class GBTModel(abstract_model):
    def __init__(self):
        try:
            model_path = os.path.join(os.path.dirname(__file__), 'GBTModel.pickle')
            with open(model_path, 'rb') as model:
                self.model = pickle.load(model)
            encoder_path = os.path.join(os.path.dirname(__file__), 'Encoder.pickle')
            with open(encoder_path, 'rb') as encoder:
                self.encoder = pickle.load(encoder)
        except Exception as e:
            print("EXCEPTION: ", e)
            model, encoder = train_model()
            with open('GBTModel.pickle', 'wb') as handle:
                pickle.dump(model, handle)
            with open('Encoder.pickle', 'wb') as handle:
                pickle.dump(encoder, handle)
            self.model = model
            self.encoder = encoder
        
    def predict(self, X):
        try:
            data_input = pd.DataFrame(X, columns=['trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt', 'city', 'job', 'dob'])
            encoded_input = clean_up(data_input, self.encoder)[0]
            prediction = self.model.predict(encoded_input)[0]
            return prediction
        except Exception as e:
            print("EXCEPTION: ", e)
            pass
    
    def retrain(self, X):
        model, encoder = train_model(pd.DataFrame(X, columns = ['trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt', 'city', 'job', 'dob', 'class']))
        self.model = model
        self.encoder = encoder
