FROM python:3

ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD

WORKDIR /usr/src/app
COPY src/ ./
COPY docker/back/* /docker/

RUN mkdir -p /etc/uwsgi && \
    mkdir -p /logs && \
    cp /docker/uwsgi.ini /etc/uwsgi && \
    cp /docker/requirements.txt /usr/src/app && \
    /docker/project_settings.ini.sh > /etc/project_settings.ini && \
    pip install --no-cache-dir -r requirements.txt && \
    python manage.py collectstatic --noinput

CMD python manage.py migrate && uwsgi --ini /etc/uwsgi/uwsgi.ini && celery -A csvreader worker -B -l info