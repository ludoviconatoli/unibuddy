
web: export FLASK_CONFIG="production" && export FLASK_APP="app.py" && flask run
web: gunicorn app:app -b "0.0.0.0:$PORT" -w 3