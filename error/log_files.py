import logging


class DebugFilter(logging.Filter):
    #Переопределяем метод
    def filter(self, record):
        return record.levelname in ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
