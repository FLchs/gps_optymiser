FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7


# Run the application:
COPY ./app /app
RUN pip install -r /app/requirements.txt