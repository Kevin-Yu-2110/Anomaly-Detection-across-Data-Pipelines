### Initial Requirements
- node.js (v20.11.1)
- create-react-app (v18.2.0)
- python (v3.11.5)
### Node packages
Node package dependencies are listed in package.json and can be installed via the 'npm install' command.
### Python packages
Python package dependencies are listed within requirements.txt and can be installed via 'pip install -r requirements.txt'.
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
### Run MLflow tracking server
```
cd models
mlflow server
```