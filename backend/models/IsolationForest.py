import os

import pickle
import numpy as np
import pandas as pd

from sklearn.metrics import confusion_matrix
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
from clean_up import clean_up
from abstract_model import abstract_model

import mlflow
from mlflow import MlflowClient


class isolationForestModel(abstract_model):
    def __init__(self, owner):
        try:
            encoder_path = os.path.join(os.path.dirname(__file__), 'Encoder.pickle')
            with open(encoder_path, 'rb') as encoder:
                encoder = pickle.load(encoder)
            model_name = 'default-IF'
        except Exception as e:
            model_name, encoder = train_model()
            encoder_path = os.path.join(os.path.dirname(__file__), 'Encoder.pickle')
            with open(encoder_path, 'wb') as handle:
                pickle.dump(encoder, handle)
            print(encoder)
        finally:
            self.model_name = model_name
            self.encoder = encoder
            self.owner = owner
        
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
        
    def retrain(self, X):
        model_name, encoder = train_model(pd.DataFrame(X, columns = ['trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt', 'city', 'job', 'dob', 'class']), self.owner)
        encoder_path = os.path.join(os.path.dirname(__file__), 'Encoder.pickle')
        with open(encoder_path, 'wb') as handle:
            pickle.dump(encoder, handle)
        self.encoder = encoder

def train_model(data=pd.DataFrame(), owner=None):
    # enable autologging
    mlflow.sklearn.autolog()

    remote_server_uri = "http://127.0.0.1:5000"
    mlflow.set_tracking_uri(remote_server_uri)
    mlflow.set_experiment("isolationforest")

    train_path = os.path.join(os.path.dirname(__file__), 'fraudTrain.csv')
    train_data = pd.read_csv(train_path)
    if not data.empty:
        train_data = pd.concat([train_data, data])

    X_train, enc = clean_up(train_data.iloc[:, :-1])
    y_train = train_data.iloc[:, -1:]

    random_state = np.random.RandomState(42)
    test_data = pd.read_csv('backend/models/fraudTest.csv')
    X_test, enc = clean_up(test_data.iloc[:, :-1], enc)
    y_test = test_data.iloc[:, -1:]

    model = IsolationForest(n_estimators=100,max_samples='auto',contamination=float(0.2),random_state=random_state)
    with mlflow.start_run() as run:
        model.fit(X_train, y_train)

        y_actual = y_test.to_numpy().transpose()[0]
        y_predict = model.predict(X_test)
        y_predict[y_predict == 1] = 0
        y_predict[y_predict == -1] = 1
        count = (y_actual == y_predict).sum()
        mlflow.log_metric("accuracy", count/len(y_actual))
        false_positives = sum(1 if (y_actual[i] == 0 and y_predict[i] == 1) else 0 for i in range(len(y_actual)))
        mlflow.log_metric("false positive rate", false_positives/len(y_actual))
        false_negatives = sum(1 if (y_actual[i] == 1 and y_predict[i] == 0) else 0 for i in range(len(y_actual)))
        mlflow.log_metric("false negative rate", false_negatives/len(y_actual))
        print(confusion_matrix(y_actual, y_predict))
        model_name = owner + '-IF' if owner else 'default-IF' 
        
        mlflow.sklearn.log_model(
            sk_model = model,
            artifact_path = 'isolation-forest',
            registered_model_name = model_name
        )
    return model_name, enc
