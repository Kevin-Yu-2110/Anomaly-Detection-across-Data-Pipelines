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
### Run backend tests
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
### Run MLflow tracking server
```
cd models
mlflow server
```
### Train network models
```
cd models
python client_model.py
```