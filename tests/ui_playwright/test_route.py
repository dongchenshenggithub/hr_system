import json
from playwright.sync_api import expect

def test_employee_empty_state_with_mock_up_api(page, app_base_url):
    """模拟 /api/employee 返回空列表，验证页面空状态 """
    def handle_employee(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps([]),
        )

    page.route("**/api/employees/", handle_employee)
    page.goto(f"{app_base_url}/employees")
    page.wait_for_selector("#employee-form")
    expect(page.locator("#employee-tbody tr")).to_have_count(0)

def test_employee_name_modified_by_route(page, app_base_url):
    """拦截真实响应，把第一个员工的名字改成“大傻逼”,验证页面显示"""

    def handle_employee(route):
        response = route.fetch()
        data = response.json()
        if data:
            data[0]["name"]="大傻逼"
        route.fulfill(
            status=200,
            content_type="application/json",
            json=data,
            )

    page.route("**/api/employees/", handle_employee)
    page.goto(f"{app_base_url}/employees")
    page.wait_for_selector("#employee-form")
    expect(page.locator("#employee-tbody")).to_contain_text("大傻逼")

def test_department_api_failure(page, app_base_url):
    """模拟部门接口网络失败，验证下拉框只有请选择"""

    def abort_departments(route):
        route.abort("connectionrefused")

    page.route("**/api/employees/departments", abort_departments)
    page.goto(f"{app_base_url}/employees")
    page.wait_for_selector("#employee-form")
    options = page.get_by_label("部门").locator("option").all_text_contents()
    assert options == ["请选择"]

def test_login_with_modified_request(page, app_base_url):
    """拦截登录请求，把密码改成错误值，验证前端显示错误"""

    def modify_login(route):
        request = route.request
        body = json.loads(request.post_data)
        body['password'] = "wrong_password"
        route.continue_(post_data=json.dumps(body))

    page.route("**/api/auth/login", modify_login)
    page.goto(f"{app_base_url}/login")
    page.get_by_label("用户名").fill("admin")
    page.get_by_label("密码").fill("admin123")
    page.get_by_role("button", name="登录").click()
    expect(page.locator("#message")).to_have_text("用户名或密码错误")