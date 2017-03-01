FROM jupyter/base-notebook
USER root

RUN apt-get update -y && apt-get install -y postgresql-client libpq-dev build-essential

USER jovyan
COPY requirements.txt /home/jovyan/requirements.txt

RUN pip install -r /home/jovyan/requirements.txt

COPY exercises /home/jovyan/work