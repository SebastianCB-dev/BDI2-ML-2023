FROM --platform=amd64 ubuntu:22.10

RUN apt update && apt install -y \
  python3-pip \
  libpq-dev \ 
  libxss1 \
  libappindicator1 \
  libindicator7 \ 
  wget \
  gnupg2 \
  ca-certificates   

# Download 
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -

# Añadir el repositorio de Google Chrome a la lista de fuentes de paquetes
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

RUN apt update && apt install google-chrome-stable -y

# Actualizar la lista de paquetes e instalar Google Chrome
RUN mkdir /app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]