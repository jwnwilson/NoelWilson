FROM python:2.7

# Install sqlite
RUN apt-get update && apt-get install sqlite3

# Add project files to DIR
COPY . /app
WORKDIR /app/

ENV PORT 8000
ENV PYTHONUNBUFFERED TRUE

CMD python manage.py runserver 0.0.0.0:$PORT