from collections import deque
from time import time


class Stack():

    def __init__(self, width = 100):
        self.__width = width
        self.__history = deque()

    def knock(self):
        self.__history.append(time())
        if len(self.__history) > self.__width:
            self.__history.popleft()

    @property
    def history(self):
        return self.__history