from abc import ABC, abstractmethod

# 定义设置基类
class Settings(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass