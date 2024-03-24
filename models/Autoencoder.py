import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from tensorflow.keras.losses import MeanSquaredLogarithmicError
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

def find_threshold(model, x_train_scaled):
  reconstructions = model.predict(x_train_scaled)
  # provides losses of individual instances
  reconstruction_errors = tf.keras.losses.mae(reconstructions, x_train_scaled)

  # threshold for anomaly scores
  threshold = np.mean(reconstruction_errors.numpy()) +  2 * np.std(reconstruction_errors.numpy())
  return threshold

def get_predictions(model, x_test_scaled, threshold):
  predictions = model.predict(x_test_scaled)
  # provides losses of individual instances
  errors = tf.keras.losses.mae(predictions, x_test_scaled)
  # 1 = anomaly, 0 = normal
  anomaly_mask = pd.Series(errors) > threshold
  preds = anomaly_mask.map(lambda x: 1.0 if x == True else 0.0)
  return preds

class AutoEncoder(Model):
  def __init__(self, output_units, code_size=8):
    super().__init__()
    self.encoder = Sequential([
      Dense(64, activation='relu'),
      Dropout(0.1),
      Dense(32, activation='relu'),
      Dropout(0.1),
      Dense(16, activation='relu'),
      Dropout(0.1),
      Dense(code_size, activation='relu')
    ])
    self.decoder = Sequential([
      Dense(16, activation='relu'),
      Dropout(0.1),
      Dense(32, activation='relu'),
      Dropout(0.1),
      Dense(64, activation='relu'),
      Dropout(0.1),
      Dense(output_units, activation='sigmoid')
    ])
  
  def call(self, inputs):
    encoded = self.encoder(inputs)
    decoded = self.decoder(encoded)
    return decoded



data = pd.read_csv('fraudTrain.csv')
features = ['trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt', 'city', 'job', 'dob', 'is_fraud']
data = data[features]
data.dropna(ignore_index=True)
X = data.iloc[:, :-1]
y = data.iloc[:, -1:]

random_state = np.random.RandomState(42)

encoder = LabelEncoder()
X = clean_up(X, encoder)[0]

x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=random_state
)
# only the normal data for training
train_index = [i for i in y_train.index if y_train['is_fraud'][i] == 0]
train_data = x_train.loc[train_index]

min_max_scaler = MinMaxScaler(feature_range=(0, 1))
x_train_scaled = min_max_scaler.fit_transform(train_data.copy())
x_test_scaled = min_max_scaler.transform(validate_data.copy())

model = AutoEncoder(output_units=x_train_scaled.shape[1])
# configurations of model
model.compile(loss='msle', metrics=['mse'], optimizer='adam')

history = model.fit(
    x_train_scaled,
    x_train_scaled,
    epochs=10,
    batch_size=1000,
    validation_data=(x_test_scaled, x_test_scaled)
)

threshold = find_threshold(model, x_train_scaled)

test = pd.read_csv('fraudTest.csv')
test = test[features]
X_test_real = test.iloc[:, :-1]
y_test_real = test.iloc[:, -1:]

X_test_real = clean_up(X_test_real, encoder)[0]

X_test_real_scaled = min_max_scaler.transform(X_test_real.copy())

preds = get_predictions(model, X_test_real_scaled, threshold)
accuracy_score(preds, y_test_real)


confusion_matrix(y_test_real, preds)