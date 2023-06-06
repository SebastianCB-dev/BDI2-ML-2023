# Stage 1: Base image for amd64 architecture
FROM python:3.9-slim as amd64

# Install dependencies
RUN apt-get update && apt-get install -y \
  libpq-dev \
  libxss1 \
  libappindicator1 \
  libindicator7 \
  wget \
  gnupg2 \
  ca-certificates

# Download Google Chrome for amd64
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install google-chrome-stable -y

# Stage 2: Base image for arm64 architecture
FROM ubuntu:22.10 as arm64

# Install dependencies
RUN apt-get update && apt-get install -y \
  python3-pip \
  libpq-dev \
  libxss1 \
  libappindicator1 \
  libindicator7 \
  wget \
  gnupg2 \
  ca-certificates

# Download Google Chrome for arm64
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=arm64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install google-chrome-stable -y

# Stage 3: Final image
FROM arm64 as final

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Set the entrypoint command
CMD ["python3", "app.py"]