FROM python:3.11-slim

ARG PORT=8000
ENV PORT $PORT

ARG TZ=Africa/Luanda
ENV TZ $TZ

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

RUN apt-get update \
  && apt-get install -y --no-install-recommends \ 
  make libpq-dev \
  python3-dev \
  build-essential \
  && rm -rf /var/lib/apt/lists/* \
  && apt clean

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN make install

EXPOSE $PORT
# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads. S"8xSa\E56.G9%:)
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind $HOST:$PORT --workers 1 --threads 8 --timeout 0 uhtred.wsgi:application
