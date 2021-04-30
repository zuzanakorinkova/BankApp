FROM python:3.8-alpine

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /app/

COPY requirements.txt /app/.
WORKDIR /app/

RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install psycopg2
RUN apk del .tmp

COPY . /app

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]

# migrate the database: $ docker-compose run app python manage.py migrate