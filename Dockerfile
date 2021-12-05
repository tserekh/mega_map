# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 5000
WORKDIR /code
COPY . /code/
#COPY requirements.txt /code/
RUN pip install -r requirements.txt
#CMD python manage.py
ENTRYPOINT ["./entrypoint.sh"]

