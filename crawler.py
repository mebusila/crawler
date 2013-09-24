__author__ = "Serban Carlogea"
__email__  = "sherban.carlogea@gmail.com"

from running import Running
from browser import Browser
import logging

class Crawler(Running):
    
    def __init__(self, browser=None, logger=logging):
        Running.__init__(self)
        pass

    def set_browser(self, browser=None):
        if isinstance(browser, Browser):
            self.__browser = browser
        else:
            self.__browser = Browser()

    def get_browser(self):
        return self.__browser

    def set_logger(self, logger=None):
        self.__logger = logger

    def get_logger(self):
        return self.__logger
