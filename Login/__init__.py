from Login.abstract import LoginMethod
from Login.cookie import Cookie
from Login.mis import Mis
from Login.config import Config

class Login:
    """
    登录类，支持通过cookie登录或通过MIS登录
    """
    def __init__(self, method: str = None) -> None:
        self.cookie = None
        self.enabled_methods = {
            "mis": Mis,
            "cookie": Cookie
        }
        if method is not None:
            self.method = self.enabled_methods.get(method, None)()

    def show_methods(self) -> None:
        print("支持的登录方式：")
        for i, method in enumerate(self.enabled_methods.keys()):
            print(f"{i + 1}. {method}")

    def set_method(self, method: str) -> None:
        self.method = self.enabled_methods.get(method, None)()

    def user_select_method(self) -> None:
        self.show_methods()
        method = int(input("请选择登录方式：\n"))
        if method < 1 or method > len(self.enabled_methods):
            print("输入错误")
            return
        self.method = list(self.enabled_methods.values())[method - 1]()

    def login(self, **kwargs) -> None:
        """
        登录
        :return:
        """
        if self.method is None:
            raise Exception("未设置登录方式")
        self.method.login(**kwargs)
        self.cookie = self.method.getCookies()
