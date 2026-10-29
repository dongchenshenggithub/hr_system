"""员工管理页 UI 测试：表单元素、提交、列表刷新。"""

import uuid

import pytest
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.ui.conftest import BROWSER_BASE_URL, HOST_BASE_URL
from tests.ui.pages.employees_page import EmployeesPage
from tests.ui.pages.login_page import LoginPage
from selenium.webdriver.common.by import By

@pytest.fixture
def ui_user():
    """通过真实 HTTP 服务注册一个测试用户，返回用户名密码。"""
    payload = {"username": "uiuser", "password": "secret123"}
    requests.post(f"{HOST_BASE_URL}/api/auth/register", json=payload)
    return payload

@pytest.fixture
def employees_page(driver, ui_user):
    login = LoginPage(driver, BROWSER_BASE_URL)
    login.open_page()
    login.login(ui_user["username"], ui_user["password"])

    try:
        WebDriverWait(driver, 10).until(EC.url_contains("/employees"))
    except Exception:
        print(f"等待超时，当前 URL: {driver.current_url}")
        print(f"页面提示信息: {driver.find_element(By.ID, 'message').text}")
        print(f"localStorage token: {driver.execute_script('return localStorage.getItem(\"token\")')}")
        raise

    return EmployeesPage(driver, BROWSER_BASE_URL)


'''
@pytest.fixture
def employees_page(driver, ui_user):
    """先登录，等跳转到员工页后再返回页面对象。"""
    login = LoginPage(driver, BASE_URL)
    login.open_page()
    login.login(ui_user["username"], ui_user["password"])
    WebDriverWait(driver, 10).until(EC.url_contains("/employees"))
    return EmployeesPage(driver, BASE_URL)
'''
'''
import uuid
import pytest

from tests.ui.conftest import BASE_URL
from tests.ui.pages.employees_page import EmployeesPage
from tests.ui.pages.login_page import LoginPage


@pytest.fixture
def employees_page(driver, registered_user):
    """先登录，再进入员工页。"""
    login = LoginPage(driver, BASE_URL)
    login.open_page()
    login.login(registered_user["username"], registered_user["password"])
    page = EmployeesPage(driver, BASE_URL)
    page.open_page()
    return page
'''

def test_form_elements_present(employees_page, driver):
    """员工页应包含下拉框、日期、单选框、复选框、文本域、禁用按钮。"""
    print(f"当前 URL: {driver.current_url}")
    print(f"页面源码前 1500 字符: {driver.page_source[:1500]}")    
    assert employees_page.find(employees_page.DEPARTMENT).is_displayed()
    assert employees_page.find(employees_page.HIRE_DATE).is_displayed()
    assert employees_page.find(employees_page.REMOTE).is_displayed()
    assert employees_page.find(employees_page.NOTES).is_displayed()
    assert employees_page.is_reset_button_enabled() is False


def test_department_dropdown_has_options(employees_page):
    """部门下拉框应包含后端返回的部门。"""
    from selenium.webdriver.support.ui import Select
    select = Select(employees_page.find(employees_page.DEPARTMENT))
    options = [o.text for o in select.options]
    assert "研发部" in options
    assert "测试部" in options


def test_employment_type_radio(employees_page):
    """单选框默认选中全职，点击兼职后切换。"""
    assert employees_page.is_employment_type_selected("full_time") is True
    employees_page.select_employment_type("part_time")
    assert employees_page.is_employment_type_selected("part_time") is True
    assert employees_page.is_employment_type_selected("full_time") is False


def test_remote_checkbox_toggle(employees_page):
    """复选框点击后选中，再点取消。"""
    assert employees_page.is_remote_selected() is False
    employees_page.toggle_remote()
    assert employees_page.is_remote_selected() is True
    employees_page.toggle_remote()
    assert employees_page.is_remote_selected() is False


def test_hire_date_and_notes_input(employees_page):
    """日期和文本域能输入并读回值。"""
    employees_page.set_hire_date("2026-10-28")
    assert employees_page.get_hire_date() == "2026-10-28"
    employees_page.set_notes("测试备注")
    assert employees_page.get_notes() == "测试备注"


def test_add_employee_updates_table(employees_page):
    """填写表单提交后，列表出现新员工。"""
    unique_email = f"ui_{uuid.uuid4().hex[:8]}@example.com"
    employees_page.fill_employee("王五", unique_email, "测试部")
    employees_page.submit()
    assert "添加成功" in employees_page.get_form_message()
    rows = employees_page.get_table_rows()
    assert len(rows) >= 1
