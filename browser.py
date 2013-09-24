__author__ = 'Serban Carlogea'
__email__  = 'sherban.carlogea@gmail.com'

import logging


class Browser(object):

    def __init__(self, proxy=None, user_agent=None, logger=logging):
        self.__proxy = proxy
        self.__user_agent = user_agent
        self.__logger = logger
