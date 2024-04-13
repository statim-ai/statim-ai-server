import logging


class SimpleLogger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._logger = logging.getLogger()
            cls._instance._logger.setLevel(logging.INFO)
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            cls._instance._logger.addHandler(stream_handler)
        return cls._instance

    def info(self, message):
        self._logger.info(message)

    def debug(self, message):
        self._logger.debug(message)

    def warning(self, message):
        self._logger.warning(message)

    def error(self, message):
        self._logger.error(message)

    def critical(self, message):
        self._logger.critical(message)
