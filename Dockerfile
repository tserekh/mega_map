# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 5000 5001
WORKDIR /code
COPY . /code/
RUN apt-get update
RUN pip install -r requirements.txt
RUN chmod 777 /code/entrypoint.sh
ENTRYPOINT ["pwd"]
