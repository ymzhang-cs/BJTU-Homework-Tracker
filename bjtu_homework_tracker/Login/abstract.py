from abc import ABC, abstractmethod

# 定义登录方法基类
class LoginMethod(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def login(self) -> None:
        pass
    
    @abstractmethod
    def getCookies(self) -> dict:
        """
        返回JSESSIONID
        """
        pass