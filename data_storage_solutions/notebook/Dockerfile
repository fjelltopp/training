FROM jupyter/base-notebook
USER root

RUN apt-get update -y && apt-get install -y postgresql-client libpq-dev build-essential

COPY exercises /home/jovyan/work
COPY requirements.txt /home/jovyan/requirements.txt
RUN chmod a+w /home/jovyan/work/*.ipynb


USER jovyan

RUN pip install -r /home/jovyan/requirements.txt
