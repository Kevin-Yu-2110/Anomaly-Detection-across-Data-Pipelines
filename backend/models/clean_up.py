import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder


def clean_up(X, enc = None):
    numerical_X = X[["amt"]].copy()
    date_information = pd.DatetimeIndex(pd.to_datetime(X["trans_date_trans_time"]))
    numerical_X["year"] = date_information.year
    numerical_X["month"] = date_information.month
    numerical_X["day"] = date_information.day
    numerical_X["time"] = date_information.second + 60 * date_information.minute + 3600 * date_information.second
    numerical_X["age"] = (pd.to_datetime(X["trans_date_trans_time"]) - pd.to_datetime(X["dob"])).dt.days
    categorical_X = X[["cc_num", "merchant", "category", "city", "job"]].copy()
    categorical_X['merchant'] = categorical_X['merchant'].str[6:]
    if not enc:
        enc = LabelEncoder()
    for column in categorical_X:
        categorical_X[column] = enc.fit_transform(categorical_X[column])
    return pd.concat([numerical_X, categorical_X], axis = 1), enc
