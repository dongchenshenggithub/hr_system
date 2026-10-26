"""认证接口测试：注册与登录。"""


def test_register_success(client):
    """注册新用户应返回 201，且响应中不包含密码字段。"""
    response = client.post("/api/auth/register", json={
        "username": "alice",
        "password": "secret123",
    })
    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "alice"
    # 密码和哈希都不应出现在响应里，避免泄露
    assert "password" not in body
    assert "password_hash" not in body


def test_register_duplicate_username(client):
    """重复注册同一用户名应返回 400。"""
    payload = {"username": "bob", "password": "secret123"}
    client.post("/api/auth/register", json=payload)
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 400
    assert "已存在" in response.json()["detail"]


def test_login_success(client):
    """注册后用正确密码登录应返回 200 和 access_token。"""
    client.post("/api/auth/register", json={"username": "carol", "password": "secret123"})
    response = client.post("/api/auth/login", json={"username": "carol", "password": "secret123"})
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_wrong_password(client):
    """密码错误应返回 401。"""
    client.post("/api/auth/register", json={"username": "dave", "password": "secret123"})
    response = client.post("/api/auth/login", json={"username": "dave", "password": "wrong"})
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    """用户不存在也应返回 401，且不泄露“用户不存在”这一信息。"""
    response = client.post("/api/auth/login", json={"username": "nobody", "password": "x"})
    assert response.status_code == 401
