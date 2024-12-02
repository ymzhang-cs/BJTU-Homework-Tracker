from Login.abstract import LoginMethod
from Login.cookie import Cookie
from Login.mis import Mis
from Login.config import Config
from Login.cp import CoursePlatform


from GLOBAL import GLOBAL_CONFIG

class Login:
    """
    登录类，支持通过cookie登录或通过MIS登录
    """
    def __init__(self, method: str = None) -> None:
        self.cookie = None
        self.enabled_methods = {
            "mis": Mis,
            "cookie": Cookie,
            "cp": CoursePlatform
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
        if type(self.method) == Mis:
            #在这里选择浏览器
            browser = ""
            if GLOBAL_CONFIG['use_config_workflows']:
                browser = GLOBAL_CONFIG['login']['mis']['browser']
            else:   
                print("请选择你的浏览器")
                print("1. Chrome")
                print("2. Edge")
                browser_choice = int(input().strip())
                if browser_choice == 1:
                    browser = 'chrome'
                elif browser_choice == 2:
                    browser = 'edge'
                else:
                    raise ValueError("请选择1或者2")

            kwargs['browser'] = browser
        self.method.login(**kwargs)
        self.cookie = self.method.getCookies()
