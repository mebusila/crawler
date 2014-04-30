__author__ = "Serban Carlogea"
__email__  = "sherban.carlogea@gmail.com"

from running import Running
from browser import Browser
import logging


class Crawler(Running):

    __browser = None

    def __init__(self, browser=None, logger=logging):
        self.__logger = logger
        Running.__init__(self)
        if isinstance(browser, Browser):
            self.__browser = browser
        else:
            self.__browser = Browser(logger=self.__logger)

    def run(self, start_with_url=None):
        if not self.can_run():
            return

