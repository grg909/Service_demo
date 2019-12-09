web: flask db upgrade; flask translate compile; gunicorn -c gunicorn_config.py microblog:app
worker: rq worker grg909-task1
