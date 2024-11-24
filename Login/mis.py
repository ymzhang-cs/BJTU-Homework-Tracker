import requests
import sys
import winreg
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
            path = self.find_path("chrome")
            path = path + r"\chrome.exe"
            options.binary_location = path
            options.add_argument("--log-level=1")
            if not webdriver_path:
                webdriver_path = chromedriver_autoinstaller.install()
            service = ChromeService(executable_path=webdriver_path)
            driver = webdriver.Chrome(service=service, options=options)

        elif browser == 'edge':
            options = EdgeOptions()
            path = self.find_path("edge")
            path = path + r"\msedge.exe"
            options.binary_location = path
            options.add_argument("--log-level=1")
            if not webdriver_path:
                webdriver_path = edgedriver_autoinstaller.install()
            service = EdgeService(executable_path=webdriver_path)
            driver = webdriver.Edge(service=service, options=options)

        else:
            raise ValueError("不支持的类型，请选择chrome或者edge")

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

    def find_path(self,software_name=None):
        if software_name == "chrome":
            software_name = "chrome.exe"
        elif software_name == "edge":
            software_name = "msedge.exe"
        else:
            raise ValueError("不支持的类型，请选择chrome或者edge")
        try:
            #打开windows注册表
            reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
            key = winreg.OpenKey(reg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths")

            #遍历注册表
            for i in range(winreg.QueryInfoKey(key)[0]):
                sub_key_name = winreg.EnumKey(key, i)
                try:
                    sub_key = winreg.OpenKey(key, sub_key_name)
                    path = winreg.QueryValueEx(sub_key, "Path")[0]
                    if software_name == sub_key_name:
                        return path
                except OSError:
                    pass

            #关闭注册表
            winreg.CloseKey(key)
            winreg.CloseKey(reg)
        except OSError:
            pass
        return None