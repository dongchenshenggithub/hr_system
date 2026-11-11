from playwright.sync_api import expect

def test_login_page_loaded(page, app_base_url):
    page.goto(f"{app_base_url}/login")
    expect(page.get_by_label("用户名")).to_be_visible()
