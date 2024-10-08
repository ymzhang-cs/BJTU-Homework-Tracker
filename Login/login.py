import cookie as login_cookie
import mis as login_mis

class Login:
    '''
    登录类，支持通过cookie登录或通过MIS登录
    '''
    def __init__(self) -> None:
        Login.cookie = None

    def login(self, login_type: int|str):
        login_type = int(login_type)
        if login_type == 1:
            Login.cookie = login_cookie()
        elif login_type == 2:
            Login.cookie = login_mis()
        else:
            raise ValueError("Invalid login type")
