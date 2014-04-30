__author__ = "Serban Carlogea"
__email__  = "sherban.carlogea@gmail.com"

from running import Running
from browser import Browser
from scrapper import Scrapper
import logging
from lxml import etree
import queue


class Crawler(Running):

    __browser = None
    __links_xpath = []
    __next_url_xpath = None
    __scrape_queue = None
    __scrapper = None

    def __init__(self, scrapper=None, browser=None, logger=logging):
        self.__logger = logger
        Running.__init__(self)
        if isinstance(browser, Browser):
            self.__browser = browser
        else:
            self.__browser = Browser(logger=self.__logger)
        self.__scrape_queue = queue.Queue()
        self.__scrapper = scrapper

    def start(self, url=None):
        if not self.can_run():
            return self.done_running()
        return self.run(url=url)

    def run(self, url=None):
        html = self.download(url=url)
        if html is None:
            return self.done_running()

        content = etree.HTML(html)
        links = self.get_links(content)
        for link in links:
            self.__scrape_queue.put(link)

        if not self.__scrape_queue.empty():
            for i in range(5):
                if self.__scrapper is None:
                    scrapper = Scrapper(self.__scrape_queue, self.__browser, self.__logger)
                else:
                    scrapper = self.__scrapper(self.__scrape_queue, self.__browser, self.__logger)
                scrapper.daemon = True
                scrapper.start()
            self.__scrape_queue.join()

        url = self.get_next_url(content)
        if url is None:
            return self.done_running()

        return self.run(url=url)

    def get_links(self, content=None):
        links = []
        for xpath in self.get_links_xpath():
            try:
                links += content.xpath(xpath)
            except KeyError as ex:
                self.__logger.error(str(ex))
        return links

    def get_next_url(self, content=None):
        xpath = self.get_next_url_xpath()
        if xpath is None:
            return None
        try:
            url = content.xpath(xpath)
            return url[0]
        except KeyError as ex:
            self.__logger.error(str(ex))
            return None

    def download(self, url=None):
        return self.__browser.download(url)

    def set_links_xpath(self, xpath=None):
        self.__links_xpath = xpath

    def get_links_xpath(self):
        return self.__links_xpath

    def set_next_url_xpath(self, xpath=None):
        self.__next_url_xpath = xpath

    def get_next_url_xpath(self):
        return self.__next_url_xpath