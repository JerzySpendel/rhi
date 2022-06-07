FROM python:3.10

ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD python rhim/manage.py migrate && python rhim/manage.py runserver 0.0.0.0:8000