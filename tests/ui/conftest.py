"""UI 测试共享 fixture：启动被测服务、连接 Docker 中的 Selenium。"""

import subprocess
import time

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# 被测服务的地址。
# UI 测试的浏览器跑在 Docker 容器里，容器内的 127.0.0.1 是容器自己，
# 所以要用 host.docker.internal 指向宿主机。
# BASE_URL = "http://host.docker.internal:8000"
HOST_BASE_URL = "http://127.0.0.1:8000"
# Selenium 容器的地址。容器把 4444 端口映射到宿主机，pytest 从宿主机连接它。
SELENIUM_URL = "http://127.0.0.1:4444"
BROWSER_BASE_URL = "http://host.docker.internal:8000"

@pytest.fixture(scope="session", autouse=True)
def start_server():
    """启动 uvicorn 服务，测试结束后关闭。"""
    process = subprocess.Popen(
        [
            "./venv/bin/python", "-m", "uvicorn", "app.main:app",
            "--host", "0.0.0.0", "--port", "8000",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # 等待服务就绪，最多 10 秒
    for _ in range(20):
        try:
            if requests.get(f"http://127.0.0.1:8000/health", timeout=1).status_code == 200:
                break
        except Exception:
            time.sleep(0.5)
    yield
    process.terminate()
    process.wait()


@pytest.fixture
def driver():
    """连接 Docker 中的 Selenium Firefox，测试结束后关闭会话。"""
    options = Options()
    # Firefox 的窗口尺寸参数是 --width / --height，不是 Chrome 的 --window-size
    options.add_argument("--width=1280")
    options.add_argument("--height=800")

    drv = webdriver.Remote(
        command_executor=SELENIUM_URL,
        options=options,
    )
    drv.implicitly_wait(5)
    yield drv
    drv.quit()