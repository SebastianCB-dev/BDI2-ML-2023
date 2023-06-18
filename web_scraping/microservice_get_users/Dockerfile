FROM ubuntu:22.10

# Set the working directory to /app
WORKDIR /app

# Install apt dependencies
RUN apt update && apt install -y \
  python3-pip \ 
  libpq-dev \ 
  libxss1 \
  libappindicator1 \
  libindicator7 \ 
  wget \
  gnupg2 \
  ca-certificates \
  xvfb \
  dbus-x11 \
  xorg

# Other installations
RUN apt-get -y install gtk2-engines-pixbuf
RUN apt-get -y install xfonts-base xfonts-100dpi xfonts-75dpi xfonts-cyrillic xfonts-scalable

# Download Google Chrome Key
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
# Añadir el repositorio de Google Chrome a la lista de fuentes de paquetes
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y google-chrome-stable
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy Files
COPY . .

# Set up X server, display environment and Chrome binary
RUN Xvfb -ac :99:0 -screen 0 1280x1024x16 &> xvfb.log 2>&1
ENV CHROME_BIN=/usr/bin/google-chrome

# Give Permissions to execute
RUN chmod +x /app/drivers/chromedriver*

# Run the Scraper
CMD ["python3", "app.py"]