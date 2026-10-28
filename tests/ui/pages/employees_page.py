"""员工管理页 Page Object。"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from tests.ui.pages.base_page import BasePage


class EmployeesPage(BasePage):
    NAME = (By.ID, "emp-name")
    EMAIL = (By.ID, "emp-email")
    DEPARTMENT = (By.ID, "emp-department")
    HIRE_DATE = (By.ID, "emp-hire-date")
    REMOTE = (By.ID, "emp-remote")
    NOTES = (By.ID, "emp-notes")
    ADD_BTN = (By.ID, "add-btn")
    RESET_BTN = (By.ID, "reset-btn")
    FORM_MESSAGE = (By.ID, "form-message")
    TABLE_BODY = (By.ID, "employee-tbody")
    LOGOUT_LINK = (By.ID, "logout-link")

    def open_page(self):
        self.open("/employees")

    def fill_employee(self, name, email, department=None):
        self.find(self.NAME).clear()
        self.find(self.NAME).send_keys(name)
        self.find(self.EMAIL).clear()
        self.find(self.EMAIL).send_keys(email)
        if department:
            Select(self.find(self.DEPARTMENT)).select_by_visible_text(department)

    def submit(self):
        self.find(self.ADD_BTN).click()

    def get_form_message(self):
        return self.wait_visible(self.FORM_MESSAGE).text

    def get_table_rows(self):
        return self.find(self.TABLE_BODY).find_elements(By.TAG_NAME, "tr")

    def select_employment_type(self, value):
        self.find((By.CSS_SELECTOR, f'input[name="employment_type"][value="{value}"]')).click()

    def is_employment_type_selected(self, value):
        return self.find((By.CSS_SELECTOR, f'input[name="employment_type"][value="{value}"]')).is_selected()

    def toggle_remote(self):
        self.find(self.REMOTE).click()

    def is_remote_selected(self):
        return self.find(self.REMOTE).is_selected()

    def is_reset_button_enabled(self):
        return self.find(self.RESET_BTN).is_enabled()

    def set_hire_date(self, date_str):
        self.find(self.HIRE_DATE).send_keys(date_str)

    def get_hire_date(self):
        return self.find(self.HIRE_DATE).get_attribute("value")

    def set_notes(self, text):
        self.find(self.NOTES).send_keys(text)

    def get_notes(self):
        return self.find(self.NOTES).get_attribute("value")
