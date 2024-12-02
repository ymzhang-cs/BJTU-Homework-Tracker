from Login.abstract import LoginMethod

class Cookie(LoginMethod):
    def __init__(self):
        self.cookie = dict()

    def login(self, JSESSIONID: str = None) -> None:
        if JSESSIONID:
            self.cookie["JSESSIONID"] = JSESSIONID
        else:
            self.cookie["JSESSIONID"] = input("请输入JSESSIONID：")
        return
    
    def getCookies(self) -> dict:
        return self.cookie
