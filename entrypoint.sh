#!/bin/bash
echo 'start entrypoint'
flask db init
echo 'finish db init'
flask db migrate
echo 'finish db migrate'
flask db migrate
echo 'finish db migrate'
python3 data_to_db.py
echo 'finish python data_to_db.py'
#gunicorn --bind 0.0.0.0:"$PORT"  --workers=1 application
gunicorn --bind 0.0.0.0:8000  --workers=1 application
