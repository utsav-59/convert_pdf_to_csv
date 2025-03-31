FROM python:3.12-slim as base

USER root

RUN apt-get update && \
    apt-get install -y openjdk-17-jdk-headless ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

WORKDIR /app

COPY requirements.txt .

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
