FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /app
WORKDIR /app

COPY . /app

RUN pip install -U pip && \
    pip install -Ur requirements.txt

EXPOSE 5000

CMD python app.py
