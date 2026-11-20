import pytest
from playwright.sync_api import sync_playwright
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"
#AUTH_FIlE = "test/ui_playwright/.auth/user.json"
AUTH_FILE = str(Path(__file__).parent / ".auth" / "user.json")


@pytest.fixture(scope="session")
def app_base_url():
    return BASE_URL 

# @pytest.fixture(scope="session")
# def auth_storage_state(app_base_url):
#     """一次登录，存cookie和Localstorage到user.json"""
#     Path(AUTH_FILE).parent.mkdir(parents=True, exist_ok=True)
#     with sync_playwright() as p:
#         browser = p.chromium.launch()
#         context = browser.new_context()
#         page = context.new_page()

#         page.goto(f"{app_base_url}/login")
#         page.get_by_label("用户名").fill("admin")
#         page.get_by_label("密码").fill("admin123")
#         page.get_by_label("记住我").check()
#         page.get_by_role("button", name="登录").click()
#         page.wait_for_url("**/employees")

#         context.storage_state(path=AUTH_FIlE)
#         context.close()
#         browser.close()
    
#     return AUTH_FILE 

@pytest.fixture(scope="session")
def auth_storage_state(app_base_url, browser):
    """一次登录，存cookie和Localstorage到user.json"""
    Path(AUTH_FILE).parent.mkdir(parents=True, exist_ok=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto(f"{app_base_url}/login")
    page.get_by_label("用户名").fill("admin")
    page.get_by_label("密码").fill("admin123")
    page.get_by_label("记住我").check()
    page.get_by_role("button", name="登录").click()
    page.wait_for_url("**/employees")

    context.storage_state(path=AUTH_FILE)
    context.close()
    return AUTH_FILE


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, auth_storage_state):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 800},
        "storage_state": auth_storage_state
            }