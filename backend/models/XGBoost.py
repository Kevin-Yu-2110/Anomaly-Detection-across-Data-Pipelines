import numpy as np
import pandas as pd

import os
import pickle
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
from models.clean_up import clean_up
from models.abstract_model import abstract_model

import mlflow
from mlflow import MlflowClient

class XGBoostModel(abstract_model):
    def __init__(self, owner):
        try:
            model_name = 'default-XG'
            encoder_path = os.path.join(os.path.dirname(__file__), 'encoders/' + model_name + '-encoder.pickle')
            with open(encoder_path, 'rb') as encoder:
                encoder = pickle.load(encoder)
        except Exception as e:
            model_name, encoder = train_model(retrain = False)
            encoder_path = os.path.join(os.path.dirname(__file__), 'encoders/default-XG-encoder.pickle')
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
            model = mlflow.xgboost.load_model('models:/' + self.model_name + "/latest")
            prediction = model.predict(encoded_input)
            prob = model.predict_proba(encoded_input)
            return [prediction, prob]
        except Exception as e:
            print("EXCEPTION: ", e)
            pass


    def retrain(self, X):
        cleaned_input = pd.DataFrame(X, columns = ['trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt', 'city', 'job', 'dob', 'is_fraud'])
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
    features = ['trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt', 'city', 'job', 'dob', 'is_fraud']
    train_data = train_data[features]
    if not data.empty:
        train_data = pd.concat([train_data, data])

    x_train = train_data.iloc[:, :-1]
    y_train = train_data.iloc[:, -1:]
    x_train, encoder = clean_up(x_train)

    x_train, y_train = SMOTE().fit_resample(x_train, y_train)

    random_state = np.random.RandomState(20)

    model = XGBClassifier(n_estimators=50, 
                        tree_method='hist', 
                        enable_categorical=True,
                        eval_metric='auc',
                        eta=0.1,
                        max_depth=10,
                        min_child_weight=10,
                        random_state=random_state)
    
    with mlflow.start_run() as run:
        model.fit(x_train, y_train)
        model_name = owner + '-XG' if retrain else 'default-XG' 
        
        mlflow.xgboost.log_model(
            xgb_model = model,
            artifact_path = 'XGBoost',
            registered_model_name = model_name,
            model_format="ubj",
        )
    return model_name, encoder