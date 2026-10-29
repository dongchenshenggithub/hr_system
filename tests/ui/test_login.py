"""登录页 UI 测试。"""

import pytest

from tests.ui.conftest import BROWSER_BASE_URL
from tests.ui.pages.login_page import LoginPage


@pytest.fixture
def login_page(driver):
    return LoginPage(driver, BROWSER_BASE_URL)


def test_login_page_loaded(login_page):
    """登录页应加载出用户名、密码、登录按钮。"""
    login_page.open_page()
    assert login_page.wait_visible(login_page.USERNAME).is_displayed()
    assert login_page.find(login_page.PASSWORD).is_displayed()
    assert login_page.find(login_page.LOGIN_BTN).is_displayed()


def test_remember_me_default_unchecked(login_page):
    """“记住我”复选框默认未选中。"""
    login_page.open_page()
    assert login_page.is_remember_me_selected() is False


def test_login_wrong_password_shows_message(login_page, driver):
    """密码错误时页面显示错误提示，不跳转。"""
    login_page.open_page()
    login_page.login("nobody", "wrongpass")
    assert "用户名或密码错误" in login_page.get_message()
    assert "/login" in driver.current_url
