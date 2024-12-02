from Login.abstract import LoginMethod
import yaml

class Config(LoginMethod):
    def __init__(self):
        self.cookie = dict()

    def login(self) -> None:
        with open("config.yaml", "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        self.cookie["JSESSIONID"] = config['cookie']
        return
    
    def getCookies(self) -> dict:
        return self.cookie
