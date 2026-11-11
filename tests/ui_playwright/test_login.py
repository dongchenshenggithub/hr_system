from playwright.sync_api import expect

def test_login_page_loaded(page, app_base_url):
    """login page should show the username,password,login button"""
    page.goto(f"{app_base_url}/login")
    expect(page.get_by_label("用户名")).to_be_visible()
    expect(page.get_by_label("密码")).to_be_visible()
    expect(page.get_by_role("button", name="登录")).to_be_visible()

def test_remember_me_default_unchecked(page, app_base_url):
    page.goto(f"{app_base_url}/login")
    expect(page.get_by_label("记住我")).not_to_be_checked()

def test_login_wrong_password_shows_message(page, app_base_url):
    page.goto(f"{app_base_url}/login")
    page.get_by_label("用户名").fill("nobody")
    page.get_by_label("密码").fill("fuck")
    page.get_by_role("button", name="登录").click()
    expect(page.locator("#message")).to_have_text("用户名或密码错误")
    expect(page).to_have_url(f"{app_base_url}/login")
