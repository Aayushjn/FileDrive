import os
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import time
import unittest

# Function to check the "Shared with me" section


def check_shared_with_me(driver):
    shared_with_me_button = driver.find_element(by="xpath", value="/html/body/div/nav/div[1]/a[2]")
    shared_with_me_button.click()
    time.sleep(3)
    print("Checked 'Shared with me' section")


# Function to check another option (e.g., "Home button" where all files uploaded by the user are visible)


def check_home_button(driver):
    home_button = driver.find_element(by="xpath", value="/html/body/div/nav/div[1]/a[1]")
    home_button.click()
    time.sleep(3)
    print("Checked 'All files' section")
