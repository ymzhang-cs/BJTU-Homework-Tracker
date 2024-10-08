from abc import ABC, abstractmethod

from .cookie import Cookie
from .mis import Mis

# 定义登录方法基类
class LoginMethod(ABC):
    @abstractmethod
    def login(self) -> None:
        pass
    @abstractmethod
    def getCookies(self) -> dict:
        pass

class Login:
    '''
    登录类，支持通过cookie登录或通过MIS登录
    '''
    def __init__(self) -> None:
        Login.cookie = None
        Login.method = None

    def login(self, login_type: int|str):
        login_type = int(login_type)
        if login_type == 1:
            Login.method = Cookie()
        elif login_type == 2:
            Login.method = Mis()
        else:
            raise ValueError("Invalid login type")
        
        Login.cookie = Login.method.login()
