'''
Module to handle logs
'''
import logging
import sys
class Logger:
    def __init__(self, logger_name=None,filename=None, mode='w', is_verbose=True):
        self.is_verbose = is_verbose
        self.logger = None

        if(self.logger is None):           
            self.logger = self.create_logger(logger_name)
            self.logger.addHandler(self.create_stream_handler())
            self.logger.addHandler(self.create_file_handler(filename, mode))
    
    def create_logger(self, logger_name, level=logging.DEBUG):
        if self.logger is None:
            self.logger = logging.getLogger(logger_name)
            self.logger.setLevel(level)
        return self.logger

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
            self.logger.debug(message)
            return
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)