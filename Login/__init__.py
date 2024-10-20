from Login.cookie import Cookie
from Login.mis import Mis
from Login.config import Config

class Login:
    """
    登录类，支持通过cookie登录或通过MIS登录
    """
    def __init__(self) -> None:
        self.cookie = None
        self.method = None

    def login(self, login_type: int|str):
        login_type = int(login_type)
        if login_type == 1:
            self.method = Cookie()
        elif login_type == 2:
            self.method = Mis()
        elif login_type == 3:
            self.method = Config()
        else:
            raise ValueError("Invalid login type")
        
        self.method.login()
        self.cookie = self.method.getCookies()
