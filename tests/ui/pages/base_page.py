"""所有 Page Object 的基类，封装通用操作。"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def open(self, path):
        """打开指定路径。"""
        self.driver.get(f"{self.base_url}{path}")

    def find(self, locator):
        """按定位器查找元素。"""
        return self.driver.find_element(*locator)

    def wait_visible(self, locator, timeout=10):
        """等待元素可见后返回。"""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
