import requests
import chromedriver_autoinstaller
import edgedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from Login.abstract import LoginMethod


class Mis(LoginMethod):
    def __init__(self):
        self.cookie = dict()

    def login(self, browser: str = 'chrome', webdriver_path: str = None) -> None:

        login_url = 'https://mis.bjtu.edu.cn/module/module/104/'
        jump_page = 'https://bksycenter.bjtu.edu.cn/NoMasterJumpPage.aspx?URL=jwcZhjx&FPC=page:jwcZhjx'

        if browser == 'chrome':
            options = ChromeOptions()
            options.add_argument("--log-level=1")
            if not webdriver_path:
                webdriver_path = chromedriver_autoinstaller.install()
            service = ChromeService(executable_path=webdriver_path)
            driver = webdriver.Chrome(service=service, options=options)

        elif browser == 'edge':
            options = EdgeOptions()
            options.add_argument("--log-level=1")
            if not webdriver_path:
                webdriver_path = edgedriver_autoinstaller.install()
            service = EdgeService(executable_path=webdriver_path)
            driver = webdriver.Edge(service=service, options=options)

        else:
            raise ValueError("不支持的类型，请选择chorme或者edge")

        driver.get(login_url)
        WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.ID, 'divLogin')))
        driver.get(jump_page)
        cookies = driver.get_cookies()
        for cookie in cookies:
            if cookie['name'] == 'JSESSIONID':
                self.cookie['JSESSIONID'] = cookie['value']
                break
        print(f"已获取JSESSIONID: {self.cookie['JSESSIONID']}")
        print("浏览器退出中...")
        driver.quit()

    def getCookies(self):
        return self.cookie
