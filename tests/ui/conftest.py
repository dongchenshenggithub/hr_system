"""UI 测试共享 fixture：启动服务、提供 headless WebDriver。"""

import subprocess
import time

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="session", autouse=True)
def start_server():
    """启动 uvicorn 服务，测试结束后关闭。"""
    process = subprocess.Popen(
        ["./venv/bin/python", "-m", "uvicorn", "app.main:app", "--port", "8000"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # 等待服务就绪，最多 10 秒
    for _ in range(20):
        try:
            import requests
            if requests.get(f"{BASE_URL}/health", timeout=1).status_code == 200:
                break
        except Exception:
            time.sleep(0.5)
    yield
    process.terminate()
    process.wait()


@pytest.fixture
def driver():
    """提供 headless Chrome WebDriver，测试结束后退出。"""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")

    options.binary_location = "/snap/firefox/current/usr/lib/firefox/firefox"

    drv = webdriver.Firefox(options=options)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()
