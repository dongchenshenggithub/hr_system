import re
import pytest
from playwright.sync_api import Playwright, sync_playwright, expect

@pytest.mark.parametrize("username, password, employee_name, mailbox", [
    ("admin","admin123","朱老八", "laoba.zhu@example.com")
])
def test_e2e_add_employee(page, username, password, employee_name, mailbox):
    page.goto("http://127.0.0.1:8000/login")
    page.get_by_role("textbox", name="用户名").fill(username)
    page.get_by_role("textbox", name="密码").fill(password)
    page.get_by_role("checkbox", name="记住我").check()
    page.get_by_role("button", name="登录").press("Enter")
    page.get_by_role("textbox", name="姓名").fill(employee_name)
    page.get_by_role("textbox", name="邮箱").fill(mailbox)
    page.get_by_label("部门 请选择 研发部产品部测试部人事部财务部").select_option("财务部")
    page.get_by_role("textbox", name="入职日期").fill("2026-11-19")
    page.get_by_role("radio", name="实习").check()
    page.get_by_role("checkbox", name="远程办公").check()
    page.get_by_role("textbox", name="备注").fill("纯牛马")
    page.get_by_role("button", name="添加").click()
    page.get_by_role("link", name="退出登录").click()

# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("http://127.0.0.1:8000/login")
#     page.get_by_role("textbox", name="用户名").fill("admin")
#     page.get_by_role("textbox", name="密码").fill("admin123")
#     page.get_by_role("checkbox", name="记住我").check()
#     page.get_by_role("button", name="登录").press("Enter")
#     page.get_by_role("textbox", name="姓名").fill("马老七")
#     page.get_by_role("textbox", name="邮箱").fill("laoqi.ma@example.com")
#     page.get_by_label("部门 请选择 研发部产品部测试部人事部财务部").select_option("财务部")
#     page.get_by_role("textbox", name="入职日期").fill("2026-11-19")
#     page.get_by_role("radio", name="实习").check()
#     page.get_by_role("checkbox", name="远程办公").check()
#     page.get_by_role("textbox", name="备注").fill("纯牛马")
#     page.get_by_role("button", name="添加").click()
#     page.get_by_role("link", name="退出登录").click()

#     # ---------------------
#     context.close()
#     browser.close()


# with sync_playwright() as playwright:
#     run(playwright)
