"""登录页 Page Object。"""

from selenium.webdriver.common.by import By

from tests.ui.pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    REMEMBER_ME = (By.ID, "remember-me")
    LOGIN_BTN = (By.ID, "login-btn")
    MESSAGE = (By.ID, "message")

    def open_page(self):
        self.open("/login")

    def login(self, username, password):
        self.find(self.USERNAME).clear()
        self.find(self.USERNAME).send_keys(username)
        self.find(self.PASSWORD).clear()
        self.find(self.PASSWORD).send_keys(password)
        self.find(self.LOGIN_BTN).click()

    def get_message(self):
        return self.wait_visible(self.MESSAGE).text

    def is_remember_me_selected(self):
        return self.find(self.REMEMBER_ME).is_selected()
