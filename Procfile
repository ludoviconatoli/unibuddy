
web: set FLASK_CONFIG="development"
set FLASK_APP="app.py"
flask run -h 0.0.0.0
web: gunicorn app:app -b "0.0.0.0:$PORT" -w 3
python-3.10