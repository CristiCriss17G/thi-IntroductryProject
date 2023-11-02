# to get RUN-output: export DOCKER_BUILDKIT=0 in shell before docker compose build
FROM python:3.8-slim
# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

ENV DEBIAN_FRONTEND noninteractive
RUN apt update && apt upgrade -y && \
     apt-get -y install wget gcc g++ mono-mcs && \
     rm -rf /var/lib/apt/lists/*
WORKDIR /app
#COPY . .

COPY requirements.txt requirements.txt

RUN python3 -m pip install --upgrade pip
RUN pip install -U pip setuptools wheel
RUN pip install --no-deps -r requirements.txt

HEALTHCHECK --interval=5s --timeout=5s --start-period=5s --retries=5 CMD wget --quiet --tries=1 --spider http://localhost:8000/healthcheck || exit 1

