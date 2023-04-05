# Base image: https://hub.docker.com/_/python
FROM python:3.11.2-alpine3.17

# Dependencies for chromium
RUN apk add --no-cache \
  chromium \
  chromium-chromedriver \
  xvfb \
  wait4ports \
  libxi-dev \
  libxext-dev \
  libxrender-dev \
  ca-certificates \
  openssl

# Set directory for the app
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt requirements.txt
RUN \
  apk add --no-cache python3 postgresql-libs && \
  apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
  python3 -m pip install -r requirements.txt --no-cache-dir && \
  apk --purge del .build-deps

# Copy the rest of the app
COPY . .

# Execute the app
CMD ["python", "app.py"]