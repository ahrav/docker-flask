FROM python:3.7.2-stretch

ENV APP /APP
WORKDIR ${APP}

EXPOSE 5000

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uwsgi", "--ini", "app.ini"]