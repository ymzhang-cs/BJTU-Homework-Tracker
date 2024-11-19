import requests
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Login.abstract import LoginMethod


class Mis(LoginMethod):
    def __init__(self):
        self.cookie = dict()

    def login(self, webdriver_path: str = None) -> None:
        """
        通过MIS系统跳转本科生院，登录智慧课程平台获取JSESSIONID
        """

        login_url = 'https://mis.bjtu.edu.cn/module/module/104/'
        jump_page = 'https://bksycenter.bjtu.edu.cn/NoMasterJumpPage.aspx?URL=jwcZhjx&FPC=page:jwcZhjx'

        # 配置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument("--log-level=1")  # 不在控制台输出INFO
        # chrome_options.add_argument("--headless")  # 无头模式运行

        # 如果没有传入webdriver_path，且未安装ChromeDriver，自动安装
        if not webdriver_path:
            chromedriver_autoinstaller.install()

        # 初始化ChromeDriver
        service = Service(executable_path=webdriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # 用户手动登录MIS跳转本科生院
        driver.get(login_url)

        # 等待页面跳转
        WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.ID, 'divLogin')))

        # 跳转智慧课程平台
        driver.get(jump_page)

        # 获取 JSESSIONID
        cookies = driver.get_cookies()
        for cookie in cookies:
            if cookie['name'] == 'JSESSIONID':
                self.cookie['JSESSIONID'] = cookie['value']
                break
        print(f"已获取JSESSIONID: {self.cookie['JSESSIONID']}")

        # 退出浏览器
        print("浏览器退出中...")
        driver.quit()
    
    def getCookies(self):
        return self.cookie
