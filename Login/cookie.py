from login import LoginMethod

class Cookie(LoginMethod):
    def __init__(self):
        self.cookie = dict()

    def login(self):
        self.cookie["JSESSIONID"] = input("请输入JSESSIONID：")
        return
    
    def getCookies(self):
        return self.cookie
