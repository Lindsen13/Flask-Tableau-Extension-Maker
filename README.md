# Flask-Tableau-Extension-Maker

A application based on Python's Flask framework to create custom Tableau extensions that allow you to create a button in Tableau that executes a GET API call.

## How to set up

Download the repository, and run the following commands:

```
python3 -m venv
source env/bin/activate
pip3 install -r requirements.txt
export FLASK_APP=extension_app
flask init-db
flask run
```

Your application will run on http://localhost:5000/

*Note, the application has its backend developed only. The front end is just the bare minimum.*
