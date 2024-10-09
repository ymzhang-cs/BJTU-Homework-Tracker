from Login.abstract import LoginMethod

class Cookie(LoginMethod):
    def __init__(self):
        self.cookie = dict()

    def login(self) -> None:
        self.cookie["JSESSIONID"] = input("请输入JSESSIONID：")
        return
    
    def getCookies(self) -> dict:
        return self.cookie
