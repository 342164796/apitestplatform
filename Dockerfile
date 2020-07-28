FROM python:latest
RUN mkdir -p /data/apitestplatform &&\
    pip install --upgrade pip &&\
    pip install Django==2.0.1 &&\
    pip install Pymysql==0.8.0 &&\
    pip install Requests==2.18.4 &&\
    pip install uwsgi &&\
    pip install websocket-client==0.57.0 &&\
    pip install django-crontab
RUN apt-get update &&\
    apt-get install -y cron


COPY apitestplatform/ /data/apitestplatform/apitestplatform/
COPY base/ /data/apitestplatform/base/
COPY lib/ /data/apitestplatform/lib/
COPY static/ /data/apitestplatform/static/
COPY templates/ /data/apitestplatform/templates/
COPY manage.py /data/apitestplatform/
COPY start.sh /data/apitestplatform/
COPY uwsgi.ini /data/apitestplatform/

EXPOSE 8080
EXPOSE 8000

RUN chmod +x /data/apitestplatform/start.sh
WORKDIR /data/apitestplatform

RUN python manage.py crontab add
#ENTRYPOINT [ "/data/apitestplatform/start.sh" ]
CMD ["/bin/bash","/data/apitestplatform/start.sh"]