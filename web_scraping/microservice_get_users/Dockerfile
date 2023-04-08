FROM ubuntu:22.10

# Downlo
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -

# Añadir el repositorio de Google Chrome a la lista de fuentes de paquetes
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

RUN apt-get update && apt-get install -y \
    python3-pip \
    libpq-dev \ 
    libxss1 \
    libappindicator1 \
    libindicator7 \ 
    wget \
    gnupg2 \
    ca-certificates \ 
    google-chrome-stable

# Actualizar la lista de paquetes e instalar Google Chrome
RUN mkdir /app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["python3", "app.py"]