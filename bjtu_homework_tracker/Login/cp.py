from io import BytesIO
import logging
import re
from PIL import Image
import pytesseract
from Login.abstract import LoginMethod
import requests
import hashlib

logging.basicConfig(level=logging.INFO)

class CoursePlatform(LoginMethod):
    def __init__(self):
        self.session = requests.session()

    def login(self, student_id: str = None, password: str = None):
        BASE_URL = 'http://123.121.147.7:88/ve'

        # 先读一次主页
        self.session.get(BASE_URL + '/')

        # 获取验证码
        self.session.get(BASE_URL + '/GetImg')
        # 将验证码图片转换为PIL.Image
        image = Image.open(BytesIO(self.session.get(BASE_URL + '/GetImg').content))
        # 使用pytesseract识别验证码
        passcode = pytesseract.image_to_string(image)
        # 使用正则表达式去除验证码中的非数字
        passcode = re.sub(r'[^0-9]', '', passcode)
        # 显示验证码
        # image.show()
        logging.info(f"验证码: {passcode}")

        # 输入学号
        student_id = student_id if student_id is not None else input('请输入学号: ')

        # 输入密码
        password = password if password is not None else \
            input('请输入密码,\n如果是md5请以hash:开头,\n如果是明文密码请以pass:开头,\n留空则使用默认密码:\n')

        # 判断密码格式
        if len(password) == 0:
            password_hash = hashlib.md5(f'Bjtu@{student_id}'.encode()).hexdigest()
        elif password.startswith('hash:'):
            password_hash = password[len('hash:'):]
        else:
            if password.startswith('pass:'):
                password = password[len('pass:'):]
            password_hash = hashlib.md5(password.encode()).hexdigest()
        logging.info(f"哈希密码: {password_hash}")
        # 登录
        req_data = {
            'login': 'main_2',
            'qxkt_type': '',
            'qxkt_url': '',
            'username': student_id,
            'password': password_hash,
            'passcode': passcode
        }
        logging.info(f"请求数据: {req_data}")
        resp = self.session.post(BASE_URL + '/s.shtml', data=req_data, allow_redirects=True)
        logging.info(f"登录响应: {resp.content.decode(resp.encoding or 'utf-8')}")
        if not 200 <= resp.status_code < 300 or resp.content.decode(resp.encoding or 'utf-8').find('alert(') != -1:
            raise Exception('Failed logging in.')

    def getCookies(self) -> dict:
        return self.session.cookies.get_dict()
