FROM python:3.6

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN groupadd -r app && useradd -r -g app app

RUN mkdir -p /app/media /app/static /app/media \
    && chown -R app:app /app/

RUN apt-get update && \
    apt-get install -y gettext

COPY ./streaming/requirements.txt /app/

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY ./streaming/ /app/

WORKDIR /app

EXPOSE 8080
