import os
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import login_test
import file_management
import other_testing
from selenium.webdriver.chrome.options import Options
import HtmlTestRunner


website = "http://127.0.0.1:8000/"
email = "vandanaluhana810@gmail.com"
password = "Insane_1704"
file_path = (
    r"D:\BITS Pilani\Software System\SEM 3\STM\Combinatorial Testing Strategies.pdf"  # file to upload while testing
)
file_name = "lec1.pdf"  # file to download and rename
new_file_name = "lec1_updated.pdf"


# Initialize WebDriver
def setup_driver():
    options = Options()
    options.add_argument("--disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    prefs = {
        "download.prompt_for_download": True,  # Enable dialog prompt
    }
    options.add_experimental_option("prefs", prefs)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    return driver


# Main test sequence
def test_application():
    driver = setup_driver()

    try:

        login_test.register(driver, "abc@gmail.com", "John", "Peter", "insane810")
        login_test.login(driver, website, email, password)

        other_testing.check_shared_with_me(driver)
        other_testing.check_home_button(driver)
        other_testing.check_shared_files(driver)

        file_management.check_upload(driver, file_path)
        time.sleep(5)
        file_management.download_file(driver, file_name)
        file_management.delete_file(driver, "clock-full.pdf")
        time.sleep(5)
        # file_management.rename_file(driver,file_name,new_file_name)
        login_test.logout(driver)

    finally:
        driver.quit()


test_application()
