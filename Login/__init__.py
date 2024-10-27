from Login.abstract import LoginMethod
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
        self.enabled_methods = {
            "mis": Mis,
            "cookie": Cookie,
            "config": Config
        }

    def show_methods(self) -> None:
        print("支持的登录方式：")
        for i, method in enumerate(self.enabled_methods.keys()):
            print(f"{i + 1}. {method}")

    def login(self):
        self.show_methods()

        login_type = int(input("请选择登录方式：\n"))
        if login_type < 1 or login_type > len(self.enabled_methods):
            print("输入错误")
            return
        self.method: LoginMethod = list(self.enabled_methods.values())[login_type - 1]()
        
        self.method.login()
        self.cookie = self.method.getCookies()
