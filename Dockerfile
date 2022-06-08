FROM python:3.10

ADD requirements.txt /code/requirements.txt
ADD wait-for-it.sh /scripts/wait-for-it.sh
RUN chmod +x /scripts/wait-for-it.sh
WORKDIR /code
RUN pip install -r requirements.txt
CMD bash /scripts/wait-for-it.sh db:5432 && python rhim/manage.py migrate && python rhim/manage.py load_data && python rhim/manage.py runserver 0.0.0.0:8000