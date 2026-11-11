import uuid
import pytest
from playwright.sync_api import expect

@pytest.fixture
def ui_user(app_base_url):
    import requests
    payload = {"username": f"uiuser_{uuid.uuid4().hex[:8]}", "password": "Secrect123"}
    resp = requests.post(
        f"{app_base_url}/api/auth/register",
        json=payload,
        proxies={"http": None, "https": None, "all": None},
    )
    print(f"注册状态码: {resp.status_code}")
    return payload

@pytest.fixture
def employee_page(page, app_base_url, ui_user):
    page.goto(f"{app_base_url}/login")
    page.get_by_label("用户名").fill(ui_user["username"])
    page.get_by_label("密码").fill(ui_user["password"])
    page.get_by_role("button", name="登录").click()
    try:
        page.wait_for_url("**/employees", timeout=10000)
    except Exception:
        print(f"等待超时，当前 URL: {page.url}")
        print(f"页面提示: {page.locator('#message').text_content()}")
        print(f"localStorage token: {page.evaluate('localStorage.getItem(\"token\")')}")
        raise
    return page

def test_form_elements_present(employee_page):
    """employee page should have some elements"""
    expect(employee_page.get_by_label("部门")).to_be_visible()
    expect(employee_page.get_by_label("入职日期")).to_be_visible()
    expect(employee_page.get_by_label("远程办公")).to_be_visible()
    expect(employee_page.get_by_label("备注")).to_be_visible()
    expect(employee_page.get_by_role("button", name="重置")).to_be_disabled()

def test_department_dropdown_has_option(employee_page):
    options = employee_page.get_by_label("部门").locator("option").all_text_contents()
    assert "产品部" in options
    assert "研发部" in options

def test_employee_type_radio(employee_page):
    expect(employee_page.get_by_label("全职")).to_be_checked()
    employee_page.get_by_label("兼职").check()
    expect(employee_page.get_by_label("兼职")).to_be_checked()
    expect(employee_page.get_by_label("全职")).not_to_be_checked()

def test_remote_checkbox_toggle(employee_page):
    remote = employee_page.get_by_label("远程办公")
    expect(remote).not_to_be_checked()
    remote.check()
    expect(remote).to_be_checked()
    remote.uncheck()
    expect(remote).not_to_be_checked()

def test_hire_date_and_notes_input(employee_page):
    employee_page.get_by_label("入职日期").fill("2020-01-01")
    expect(employee_page.get_by_label("入职日期")).to_have_value("2020-01-01")
    employee_page.get_by_label("备注").fill("测试备注")
    expect(employee_page.get_by_label("备注")).to_have_value("测试备注")

def test_add_employee_updates_table(employee_page):
    unique_email = f"ui_{uuid.uuid4().hex[:8]}@example.com"
    employee_page.get_by_label("姓名").fill("王老五")
    employee_page.get_by_label("邮箱").fill(unique_email)
    employee_page.get_by_label("部门").select_option("测试部")
    employee_page.get_by_role("button", name="添加").click()
    expect(employee_page.locator("#form-message")).to_have_text("添加成功")
    expect(employee_page.locator("#employee-tbody")).to_contain_text("王老五")