### Import Libraries

from time import sleep
from selenium import webdriver

def test_login_page(browser):
    home_page = HomePage(browser)
    login_page = home_page.go_to_login_page()
    login_page.login("<__mistyblu>", "<Justme@61925>")

    errors = browser.find_elements_by_css_selector('#error_message')
    assert len(errors) == 0