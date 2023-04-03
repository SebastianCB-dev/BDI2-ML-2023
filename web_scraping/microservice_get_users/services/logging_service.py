import logging


class LoggingService:

    def __init__(self):
      # Creamos un controlador que mostrará los mensajes de registro en la consola.
      self.console_handler = logging.StreamHandler()
      self.console_handler.setLevel(logging.INFO)
      self.console_formatter = logging.Formatter(
          '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
      self.console_handler.setFormatter(self.console_formatter)

      # Creamos otro controlador que guardará los mensajes de registro en un archivo.
      self.file_handler = logging.FileHandler('./logs/logs.txt')
      self.file_handler.setLevel(logging.WARNING)
      self.file_formatter = logging.Formatter(
          '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
      self.file_handler.setFormatter(self.file_formatter)

      # Añadimos ambos controladores al registro.
      self.logger = logging.getLogger()
      self.logger.addHandler(self.console_handler)
      self.logger.addHandler(self.file_handler)

    def getLogging(self):
      return self.logger