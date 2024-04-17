import numpy as np
import pandas as pd

import os
import pickle
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import set_random_seed
from sklearn.preprocessing import MinMaxScaler
from models.clean_up import clean_up
from models.abstract_model import abstract_model

import mlflow
import mlflow.keras
from mlflow import MlflowClient

class NeuralNetworkModel(abstract_model):
    def __init__(self, owner):
        try:
            model_name = 'default-NN'
            encoder_path = os.path.join(os.path.dirname(__file__), 'encoders/' + model_name + '-encoder.pickle')
            with open(encoder_path, 'rb') as encoder:
                encoder = pickle.load(encoder)
        except Exception as e:
            model_name, encoder = train_model(retrain = False)
            encoder_path = os.path.join(os.path.dirname(__file__), 'encoders/default-NN-encoder.pickle')
            with open(encoder_path, 'wb') as handle:
                pickle.dump(encoder, handle)
        finally:
            self.model_name = model_name
            self.encoder = encoder
            self.owner = str(owner)
    
    def predict(self, X):
        try:
            data_input = pd.DataFrame(X, columns=['trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt', 'city', 'job', 'dob'])
            encoded_input = clean_up(data_input, self.encoder)[0]
            
            remote_server_uri = "http://127.0.0.1:5000"
            mlflow.set_tracking_uri(remote_server_uri)
            model = mlflow.pyfunc.load_model('models:/' + self.model_name + "/latest")
            prediction = model.predict(encoded_input) > 0.6
            return prediction
        except Exception as e:
            print("EXCEPTION: ", e)
            pass

    def predict_prob(self, X):
        # Not avaliable for this model
        return NULL
        
    def retrain(self, X):
        cleaned_input = pd.DataFrame(X, columns = ['trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt', 'city', 'job', 'dob', 'is_fraud'])
        model_name, encoder = train_model(cleaned_input, self.owner, retrain = True)
        encoder_path = os.path.join(os.path.dirname(__file__), 'encoders/' + self.model_name + '-encoder.pickle')
        with open(encoder_path, 'wb') as handle:
            pickle.dump(encoder, handle)
        self.model_name = model_name
        self.encoder = encoder


def train_model(data=pd.DataFrame(), owner=None, retrain=bool):
    set_random_seed(20)

    remote_server_uri = "http://127.0.0.1:5000"
    mlflow.set_tracking_uri(remote_server_uri)

    train_path = os.path.join(os.path.dirname(__file__), 'fraudTrain.csv')
    train_data = pd.read_csv(train_path)
    features = ['trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt', 'city', 'job', 'dob', 'is_fraud']
    train_data = train_data[features]
    if not data.empty:
        train_data = pd.concat([train_data, data])

    x_train = train_data.iloc[:, :-1]
    y_train = train_data.iloc[:, -1:]
    x_train, encoder = clean_up(x_train)

    test_path = os.path.join(os.path.dirname(__file__), 'fraudTest.csv')
    test_data = pd.read_csv(test_path)
    test_data = test_data[features]
    x_test = test_data.iloc[:, :-1]
    y_test = test_data.iloc[:, -1:]
    x_test = clean_up(x_test, encoder)[0]

    min_max_scaler = MinMaxScaler(feature_range=(0, 1))
    x_train_scaled = min_max_scaler.fit_transform(x_train.copy())
    x_test_scaled = min_max_scaler.transform(x_test.copy())

    model = Sequential() 
    model.add(Dense(128, activation='relu', input_dim=x_train.shape[1]))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(4, activation='relu'))
    model.add(Dense(1, activation='sigmoid')) 
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy']) 
    
    with mlflow.start_run() as run:
        model.fit(x_train_scaled, y_train, validation_data=(x_test_scaled, y_test), epochs=10, batch_size=256, verbose=0)
        model_name = owner + '-NN' if retrain else 'default-NN' 
        
        mlflow.keras.log_model(
            model,
            artifact_path = 'neural-network',
            registered_model_name = model_name
        )
    return model_name, encoder