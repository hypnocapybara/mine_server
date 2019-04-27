FROM python:3.6-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git gcc default-libmysqlclient-dev \
  && apt-get autoremove -y \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app
RUN mkdir /src
WORKDIR /app
ADD requirements.txt /app/
RUN pip install --src /src -r requirements.txt
ADD . /app
EXPOSE 8000
