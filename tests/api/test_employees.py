"""员工接口测试：鉴权、创建与列表。"""
import pytest
import uuid

pytestmark = pytest.mark.smoke

def test_list_employees_without_token(client):
    """未带 token 访问员工列表应返回 401。"""
    response = client.get("/api/employees/")
    assert response.status_code == 401


def test_create_employee_without_token(client):
    """未带 token 创建员工应返回 401。"""
    response = client.post("/api/employees/", json={
        "name": "张三",
        "email": "zhangsan@example.com",
    })
    assert response.status_code == 401


def test_list_employees_with_invalid_token(client):
    """带无效 token 应返回 401。"""
    response = client.get(
        "/api/employees/",
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert response.status_code == 401


def test_create_employee(client, auth_headers):
    """登录后创建员工应返回 201，并带回数据库生成的 id。"""
    response = client.post("/api/employees/", json={
        "name": "张三",
        "email": "zhangsan@example.com",
        "department": "研发部",
    }, headers=auth_headers)
    assert response.status_code == 201
    body = response.json()
    assert body["id"] > 0
    assert body["name"] == "张三"


def test_list_employees_empty(client, auth_headers):
    """登录后查询空列表应返回 200 和空数组。"""
    response = client.get("/api/employees/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_list_employees_after_create(client, auth_headers):
    """登录后创建一个员工，列表应能查到它。"""
    client.post("/api/employees/", json={
        "name": "李四",
        "email": "lisi@example.com",
    }, headers=auth_headers)
    response = client.get("/api/employees/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "李四"

def test_delete_employee_returns_204(client, auth_headers):
    """删除存在的员工应返回 204。"""
    create_resp = client.post("/api/employees/", json={
        "name": "待删除",
        "email": f"del_{uuid.uuid4().hex[:8]}@example.com",
    }, headers=auth_headers)
    employee_id = create_resp.json()["id"]

    response = client.delete(f"/api/employees/{employee_id}", headers=auth_headers)
    assert response.status_code == 204
    assert response.content == b""  # 204 不应该有响应体


def test_delete_nonexistent_employee_returns_404(client, auth_headers):
    """删除不存在的员工应返回 404。"""
    response = client.delete("/api/employees/999999", headers=auth_headers)
    assert response.status_code == 404
    assert "不存在" in response.json()["detail"]


def test_delete_employee_without_token_returns_401(client):
    """未登录删除员工应返回 401。"""
    response = client.delete("/api/employees/1")
    assert response.status_code == 401