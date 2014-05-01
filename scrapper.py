__author__ = "Serban Carlogea"
__email__  = "sherban.carlogea@gmail.com"

import threading
import logging
from lxml import etree


class Scrapper(threading.Thread):

    __queue = None
    __logger = None
    __browser = None
    __content = None

    def __init__(self, queue, browser, logger=logging):
        self.__queue = queue
        self.__logger = logger
        self.__browser = browser
        super(Scrapper, self).__init__()

    def run(self):
        while True:
            try:
                url = self.__queue.get()
            except TypeError:
                continue
            if self.is_valid_url(url) is False:
                self.__queue.task_done()
                continue

            html = self.__browser.download(url)
            if html:
                try:
                    self.__content = etree.HTML(html)
                except KeyError:
                    continue

            self.__logger.info("task done: %s" % url)

            self.__queue.task_done()

    def is_valid_url(self, url=None):
        self.__logger.info("is_valid_url: %s" % url)
        return True