__author__ = "Serban Carlogea"
__email__  = "sherban.carlogea@gmail.com"

import os


class RunningException(Exception):
    pass


class Lock(object):

    def __del__(self):
        self.remove()

    def exists(self):
        raise NotImplemented

    def create(self):
        raise NotImplemented

    def remove(self):
        raise NotImplemented


class FileLock(Lock):

    __filename = None

    def __init__(self, filename):
        self.__filename = filename

    def create(self):
        try:
            with open(self.__filename, mode='w') as __file:
                __file.write(str(os.getpid()))
        except IOError:
            return False
        return True

    def exists(self):
        try:
            with open(self.__filename, mode='r'):
                pass
        except IOError:
            return False
        return True

    def remove(self):
        os.unlink(self.__filename)


class Running(object):

    def __init__(self, lock=None):
        if isinstance(lock, Lock):
            self.__lock = lock
        else:
            try:
                self.__lock = FileLock(self.__lock_filename)
            except AttributeError:
                pass
        
        if self.can_run() is False:
             raise RunningException

    def can_run(self):
        try:
            if not self.__lock.exists() and self.__lock.create():
                return True
        except AttributeError:
            return True
        return False

