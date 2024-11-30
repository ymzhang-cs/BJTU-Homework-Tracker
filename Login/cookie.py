from Login import LOGIN_CONFIG
from Login.abstract import LoginMethod


mod = LOGIN_CONFIG.register_module("cookie")
mod.register_item("JSESSIONID", tybe=str, prompt="请输入JSESSIONID")

class Cookie(LoginMethod):
    def __init__(self):
        self.cookie = dict()

    def login(self) -> None:
        self.cookie["JSESSIONID"] = mod.item("JSESSIONID").value()

    def getCookies(self) -> dict:
        return self.cookie
