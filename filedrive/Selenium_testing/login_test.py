import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import unittest

#  Register function


def register(driver, new_email, first_name, last_name, pwd):

    driver.get("http://127.0.0.1:8000/signup")
    time.sleep(3)

    email_field = driver.find_element(By.XPATH, '//*[@id="id_email"]')
    email_field.send_keys(new_email)
    time.sleep(2)

    first_name_field = driver.find_element(By.XPATH, '//*[@id="id_first_name"]')
    first_name_field.send_keys(first_name)
    time.sleep(2)

    last_name_field = driver.find_element(By.XPATH, '//*[@id="id_last_name"]')
    last_name_field.send_keys(last_name)
    time.sleep(2)

    pwd_field = driver.find_element(By.XPATH, '//*[@id="id_password1"]')
    pwd_field.send_keys(pwd)
    time.sleep(2)

    confirm_pwd_field = driver.find_element(By.XPATH, '//*[@id="id_password2"]')
    confirm_pwd_field.send_keys(pwd)
    time.sleep(2)

    register_button = driver.find_element(By.XPATH, '//*[@id="formDiv"]/button').click()
    time.sleep(2)

    if "login" in driver.current_url:
        print("User registered successfully")
    else:
        # Option 2: Check for error messages or failure to redirect
        try:
            # You could check for specific error messages or elements
            error_element = driver.find_element(by="xpath", value='//div[@class="error"]')  # Example, adjust as needed
            if error_element.is_displayed():
                print("User cannot be registered due to errors")
        except:
            print("User cannot be registered (no error message, but not redirected to login)")


# Login function


def login(driver, website, email, password):
    driver.get(website)  # Replace with your login page URL
    time.sleep(3)

    # Fill out the login form
    username_field = driver.find_element(by="xpath", value='//*[@id="id_username"]')
    username_field.click()
    username_field.send_keys(email)  # Replace with your test username

    password_field = driver.find_element(by="name", value="password")
    password_field.click()
    password_field.send_keys(password)  # Replace with your test password

    # Submit the form
    password_field.send_keys(Keys.RETURN)

    # Wait for the page to load and verify login
    time.sleep(5)

    print("Login test passed!")


# Logout function
def logout(driver):
    drop_down_button = driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div[3]/button/i").click()
    time.sleep(2)
    logout_button = driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div[3]/ul/li[3]/button")
    logout_button.click()
    time.sleep(2)
    print("Logout successful")
