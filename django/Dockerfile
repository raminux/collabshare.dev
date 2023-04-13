FROM python:3.11
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --requirement requirements.txt
COPY . /app
# CMD python manage.py makemigrations; python manage.py migrate; python manage.py runserver 0.0.0.0:8000
CMD python manage.py wait_for_db; python manage.py makemigrations; python manage.py migrate; python manage.py test; python manage.py runserver 0.0.0.0:8000