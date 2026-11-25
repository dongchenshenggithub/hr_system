"""Playwright UI 测试共享配置。

- app_base_url：被测服务地址
- auth_storage_state：注册并登录一次，保存 storageState 到 user.json
- browser_context_args：让每个测试的 context 加载这份登录态
"""

import uuid
from pathlib import Path

import pytest
import requests
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"
AUTH_FILE = str(Path(__file__).parent / ".auth" / "user.json")


import os

# 在 conftest 加载时立即移除代理变量，影响后续所有 fixture 和浏览器启动
for var in ("http_proxy", "https_proxy", "all_proxy",
            "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"):
    os.environ.pop(var, None)

@pytest.fixture(scope="session")
def app_base_url():
    """被测服务的基础地址，session 级复用。"""
    return BASE_URL


@pytest.fixture(scope="session")
def auth_storage_state(app_base_url, browser):
    """注册并登录，用插件提供的 browser 保存登录态。"""
    Path(AUTH_FILE).parent.mkdir(parents=True, exist_ok=True)

    username = f"e2e_{uuid.uuid4().hex[:8]}"
    password = "Secret123"

    # 注册用户（用 requests，绕过代理）
    session = requests.Session()
    session.trust_env = False
    resp = session.post(
        f"{app_base_url}/api/auth/register",
        json={"username": username, "password": password},
    )
    assert resp.status_code == 201, f"注册失败: {resp.status_code} {resp.text}"
    session.close()

    # 用插件提供的 browser 创建上下文，不再手动 sync_playwright()
    context = browser.new_context()
    page = context.new_page()

    page.goto(f"{app_base_url}/login")
    page.get_by_label("用户名").fill(username)
    page.get_by_label("密码").fill(password)
    page.get_by_role("button", name="登录").click()
    page.wait_for_url("**/employees")

    context.storage_state(path=AUTH_FILE)
    context.close()

    return AUTH_FILE


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, auth_storage_state):
    """让每个测试的浏览器上下文都加载登录态。"""
    args = {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 800},
        "storage_state": auth_storage_state,
    }