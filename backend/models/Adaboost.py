# AdaBoost Classifier

import numpy as np
import pandas as pd
import os
import pickle
from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import AdaBoostClassifier
from imblearn.over_sampling import SMOTE
from models.clean_up import clean_up
from models.abstract_model import abstract_model

def train_model(data = None):
    train_data = pd.read_csv('fraudTrain.csv')
    features = ['trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt', 'city', 'job', 'dob', 'is_fraud']
    train_data = train_data[features]
    if data:
        train_data = pd.concat([train_data, data])

    x_train = train_data.iloc[:, :-1]
    y_train = train_data.iloc[:, -1:]
    x_train, encoder = clean_up(x_train)

    x_train, y_train = SMOTE().fit_resample(x_train, y_train)
    
    model = AdaBoostClassifier(algorithm='SAMME.R', learning_rate=0.1)
    model.fit(x_train, y_train)

    return model, encoder

class AdaBoostModel(abstract_model):
    def __init__(self):
        try:
            model_path = os.path.join(os.path.dirname(__file__), 'AdaBoostModel.pickle')
            with open(model_path, 'rb') as model:
                self.model = pickle.load(model)
            encoder_path = os.path.join(os.path.dirname(__file__), 'Encoder.pickle')
            with open(encoder_path, 'rb') as encoder:
                self.encoder = pickle.load(encoder)
        except Exception as e:
            print("EXCEPTION: ", e)
            model, encoder = train_model()
            with open('AdaboostModel.pickle', 'wb') as handle:
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
        model, encoder = train_model(pd.DataFrame(X, columns = ['trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt', 'city', 'job', 'dob', 'is_fraud']))
        self.model = model
        self.encoder = encoder