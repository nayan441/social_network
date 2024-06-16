FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000
RUN python manage.py makemigrations 
RUN python manage.py migrate
RUN python manage.py create_users

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
