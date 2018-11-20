#!/bin/bash

source ~/.bash_profile && \ 
source .env && \
git pull && \
pyenv activate venv && \
pip install -r requirements.txt && \
python manage.py migrate && \
python manage.py collectstatic --noinput && \

circusctl restart welldone



