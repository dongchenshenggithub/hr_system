"""员工接口测试：创建与列表。"""


def test_create_employee(client):
    """创建员工应返回 201，并带回数据库生成的 id。"""
    response = client.post("/api/employees/", json={
        "name": "张三",
        "email": "zhangsan@example.com",
        "department": "研发部",
    })
    assert response.status_code == 201
    body = response.json()
    assert body["id"] > 0
    assert body["name"] == "张三"


def test_list_employees_empty(client):
    """没有数据时列表应返回空数组，而不是 null 或 404。"""
    response = client.get("/api/employees/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_employees_after_create(client):
    """创建一个员工后，列表应能查到它。"""
    client.post("/api/employees/", json={
        "name": "李四",
        "email": "lisi@example.com",
    })
    response = client.get("/api/employees/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "李四"
