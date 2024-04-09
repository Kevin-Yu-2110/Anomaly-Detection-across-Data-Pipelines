### Initial Requirements
- node.js (v20.11.1)
- create-react-app (v18.2.0)
- python (v3.11.5)
### Install Node packages
```
cd frontend
npm install
```
### Install Python packages
```
pip install -r requirements.txt
```
### Install Model Training Data
Training set must be manually installed due to git file size limitations. \
Source from https://www.kaggle.com/datasets/kartik2112/fraud-detection?select=fraudTrain.csv.
Unzip and move fraudTrain.csv and fraudTest.csv to the backend/models directory.
### Run the frontend
```
cd frontend
npm start
```
### Run the backend
```
cd backend
python manage.py runserver
```
### Run the MLflow tracking server
```
cd backend
cd models
mlflow server
```
### Run backend tests
first run the MLflow tracking server then
```
cd backend
python manage.py test
```
### Update Database Schema to reflect backend changes
```
cd backend
python manage.py makemigrations
python manage.py migrate
```
### Train network models
```
cd models
python client_model.py
```