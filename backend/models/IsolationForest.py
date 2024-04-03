import os

import pickle
import numpy as np
import pandas as pd

from sklearn.metrics import confusion_matrix
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
from model.clean_up import clean_up

import mlflow
from mlflow import MlflowClient


def train_model():
    # enable autologging
    mlflow.sklearn.autolog()

    remote_server_uri = "http://127.0.0.1:5000"
    mlflow.set_tracking_uri(remote_server_uri)
    mlflow.set_experiment("test")

    ########################################
    ### needs to be replaced with big data pipeline
        
    train_data = pd.read_csv('backend/models/fraudTrain.csv')
    X_train, enc = clean_up(train_data.iloc[:, :-1])
    y_train = train_data.iloc[:, -1:]

    random_state = np.random.RandomState(42)
    test_data = pd.read_csv('backend/models/fraudTest.csv')
    X_test, enc = clean_up(test_data.iloc[:, :-1], enc)
    y_test = test_data.iloc[:, -1:]
    ##########################################

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
    return model, enc
    
class isolationForestModel():
    def __init__(self):
        try:
            model_path = os.path.join(os.path.dirname(__file__), 'IsolationForest.pickle')
            with open(model_path, 'rb') as model:
                self.model = pickle.load(model)
            encoder_path = os.path.join(os.path.dirname(__file__), 'Encoder.pickle')
            with open(encoder_path, 'rb') as encoder:
                self.encoder = pickle.load(encoder)
        except Exception as e:
            print("EXCEPTION: ", e)
            model, encoder = train_model()
            with open('backend/models/IsolationForest.pickle', 'wb') as handle:
                pickle.dump(model, handle)
            with open('backend/models/Encoder.pickle', 'wb') as handle:
                pickle.dump(encoder, handle)
            self.model = model
            self.encoder = encoder
        
    def predict(self, X):
        try:
            data_input = pd.DataFrame(X, columns=['trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt', 'city', 'job', 'dob'])
            encoded_input = clean_up(data_input, self.encoder)[0]
            prediction = self.model.predict(encoded_input)[0]
            if (prediction == -1):
                prediction = 1
            elif (prediction == 1):
                prediction = 0
            return prediction
        except Exception as e:
            print("EXCEPTION: ", e)
            pass

if __name__ == '__main__':
    badModel = isolationForestModel()