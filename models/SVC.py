# Support Vector 

import datetime
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
from sklearn.model_selection import train_test_split 
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score 
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix


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

data = pd.read_csv('fraudTrain.csv')
features = ['trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt', 'city', 'job', 'dob', 'is_fraud']
data = data[features]
data.dropna(ignore_index=True)
x_train = data.iloc[:, :-1]
y_train = data.iloc[:, -1:]

encoder = LabelEncoder()
x_train = clean_up(x_train, encoder)[0]

model = SVC()
model.fit(x_train, y_train)

test = pd.read_csv('fraudTest.csv')
test = test[features]
x_test = test.iloc[:, :-1]
y_test = test.iloc[:, -1:]

x_test = clean_up(x_test, encoder)[0]

preds = model.predict(x_test)
accuracy_score(preds, y_test)

confusion_matrix(y_test, preds)