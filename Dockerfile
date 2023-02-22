# syntax=docker/dockerfile:1
FROM python:3
USER root
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 5000 5001
WORKDIR /code
COPY . /code/
RUN apt-get update
RUN pip install -r requirements.txt
RUN chmod -R 777 /code/
CMD /code/entrypoint.sh
