from abc import ABC, abstractmethod

from Search import Search

# 定义输出处理基类
class OutputProcessor(ABC):

    @abstractmethod
    def __init__(self, search: Search):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def process(self) -> str:
        """
        处理搜索内容
        """
        pass

    @abstractmethod
    def save(self, path: str) -> None:
        """
        保存处理后的内容
        :param path: 保存路径，不包括文件名，推荐文件名为当前时间
        """
        pass

