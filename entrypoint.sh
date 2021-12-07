#!/usr/bin/env bash
flask db init
flask db migrate
flask db upgrade
python data_to_db.py
gunicorn --bind 0.0.0.0:5000 app
