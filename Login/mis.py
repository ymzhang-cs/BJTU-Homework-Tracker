from Login.abstract import LoginMethod

class Mis(LoginMethod):
    def __init__(self):
        self.cookie = dict()

    def login(self):
        raise NotImplementedError("MIS login not implemented yet")
    
    def getCookies(self):
        return self.cookie
