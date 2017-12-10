'''
Module to handle logs
'''
import logging
import sys
class Logger:
    logger = None
    def __init__(self, logger_name=None,filename=None, mode='w', is_verbose=True):
        self.is_verbose = is_verbose

        if(Logger.logger is None):           
            Logger.logger = self.create_logger(logger_name)
            Logger.logger.addHandler(self.create_stream_handler())
            Logger.logger.addHandler(self.create_file_handler(filename, mode))
    
    def create_logger(self, logger_name, level=logging.DEBUG):
        if Logger.logger is None:
            Logger.logger = logging.getLogger(logger_name)
            Logger.logger.setLevel(level)
        return Logger.logger

    def get_formatter(self):
        return logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def create_stream_handler(self):
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(self.get_formatter())
        return stream_handler

    def create_file_handler(self, filename, mode):
        file_handler = logging.FileHandler(filename, mode=mode, encoding="UTF-8", delay=False)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(self.get_formatter())
        return file_handler

    def info(self, message):
        if self.is_verbose is False:
            Logger.logger.debug(message)
            return
        Logger.logger.info(message)

    def debug(self, message):
        Logger.logger.debug(message)