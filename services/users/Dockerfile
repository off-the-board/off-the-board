FROM python:3.7.2-alpine

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

ADD . /usr/src/app

RUN chmod +x /usr/src/app/entry-point.sh

LABEL com.circleci.preserve-entrypoint=true

CMD ["./entry-point.sh"]
