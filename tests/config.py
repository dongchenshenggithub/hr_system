import os

#pytest, request, playwright 都从宿主机访问服务
APP_BASE_URL = os.getenv("APP_BASE_URL", "http://127.0.0.1:8000")

#selenium在容器内，必须用host.docker.internal 才能访问宿主机上的被测服务
BROWSER_BASE_URL = os.getenv("BROWSER_BASE_URL", "http://host.docker.internal:8000")

#selenium浏览器驱动地址
SELENIUM_URL = os.getenv("SELENIUM_URL", "http://127.0.0.1:4444")