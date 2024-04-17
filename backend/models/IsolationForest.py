import os

import pickle
import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest
from models.clean_up import clean_up
from models.abstract_model import abstract_model

import mlflow
from mlflow import MlflowClient


class isolationForestModel(abstract_model):
    def __init__(self, owner):
        try:
            model_name = 'default-IF'
            encoder_path = os.path.join(os.path.dirname(__file__), 'encoders/' + model_name + '-encoder.pickle')
            with open(encoder_path, 'rb') as encoder:
                encoder = pickle.load(encoder)
        except Exception as e:
            model_name, encoder = train_model(retrain = False)
            encoder_path = os.path.join(os.path.dirname(__file__), 'encoders/default-IF-encoder.pickle')
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
            prediction = model.predict(encoded_input)
            if (prediction == -1):
                prediction = 1
            elif (prediction == 1):
                prediction = 0
            return prediction
        except Exception as e:
            print("EXCEPTION: ", e)
            pass

    def predict_prob(self, X):
        # Not avaliable for this model
        return NULL
        
    def retrain(self, X):
        cleaned_input = pd.DataFrame(X, columns = ['trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt', 'city', 'job', 'dob', 'class'])
        model_name, encoder = train_model(cleaned_input, self.owner, retrain = True)
        encoder_path = os.path.join(os.path.dirname(__file__), 'encoders/' + model_name + '-encoder.pickle')
        with open(encoder_path, 'wb') as handle:
            pickle.dump(encoder, handle)
        self.model_name = model_name
        self.encoder = encoder

def train_model(data=pd.DataFrame(), owner=None, retrain=bool):
    remote_server_uri = "http://127.0.0.1:5000"
    mlflow.set_tracking_uri(remote_server_uri)

    train_path = os.path.join(os.path.dirname(__file__), 'fraudTrain.csv')
    train_data = pd.read_csv(train_path)
    if not data.empty:
        train_data = pd.concat([train_data, data])

    X_train, enc = clean_up(train_data.iloc[:, :-1])
    y_train = train_data.iloc[:, -1:]

    random_state = np.random.RandomState(42)

    model = IsolationForest(n_estimators=100,max_samples='auto',contamination=float(0.2),random_state=random_state)
    with mlflow.start_run() as run:
        model.fit(X_train, y_train)
        model_name = owner + '-IF' if retrain else 'default-IF' 
        
        mlflow.sklearn.log_model(
            sk_model = model,
            artifact_path = 'isolation-forest',
            registered_model_name = model_name
        )
    return model_name, enc
