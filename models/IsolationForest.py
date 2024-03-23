import os

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder


import mlflow
from mlflow import MlflowClient

def fetch_logged_data(run_id):
    client = MlflowClient()
    data = client.get_run(run_id).data
    tags = {k: v for k, v in data.tags.items() if not k.startswith("mlflow.")}
    artifacts = [f.path for f in client.list_artifacts(run_id, "model")]
    return data.params, data.metrics, tags, artifacts

# enable autologging
mlflow.sklearn.autolog()

remote_server_uri = "http://127.0.0.1:5000"
mlflow.set_tracking_uri(remote_server_uri)
mlflow.set_experiment("test")

########################################
### needs to be replaced with big data pipeline
def clean_up(X, enc = None):
    numerical_X = X[["amt"]]
    date_information = pd.DatetimeIndex(pd.to_datetime(X["trans_date_trans_time"]))
    numerical_X["year"] = date_information.year
    numerical_X["month"] = date_information.month
    numerical_X["day"] = date_information.day
    numerical_X["time"] = date_information.second + 60 * date_information.minute + 3600 * date_information.second
    numerical_X["age"] = (pd.to_datetime(X["trans_date_trans_time"]) - pd.to_datetime(X["dob"])).dt.days
    categorical_X = X[["cc_num", "merchant", "category", "city", "job"]]
    if not enc:
        enc = LabelEncoder()
    for column in categorical_X:
        categorical_X[column] = enc.fit_transform(categorical_X[column])
    return pd.concat([numerical_X, categorical_X], axis = 1), enc
    
train_data = pd.read_csv('models/fraudTrain.csv')
X_train, enc = clean_up(train_data.iloc[:, :-1])
y_train = train_data.iloc[:, -1:]

random_state = np.random.RandomState(42)
test_data = pd.read_csv('models/fraudTest.csv')
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