import os
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import time
import unittest


def check_upload(driver, file_path):

    upload_button = driver.find_element(By.XPATH, '//label[@for="id_file"]')
    upload_button.click()
    print("Upload button clicked")
    time.sleep(2)

    # Step 2: Locate and Upload the File

    try:
        file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        print(file_input)
        file_input.send_keys(file_path)  # Upload the file
        print("File uploaded successfully")
        time.sleep(5)

        pyautogui.press("esc")  # Press Enter to confirm and close
    except Exception as e:
        print("Error uploading file:", e)

    time.sleep(5)


# Function to test file download
def handle_replace_dialog():
    """
    Handles the 'Replace file' dialog that appears when a file with the same name exists.
    Assumes the dialog box is in focus.
    """
    time.sleep(2)  # Wait for the dialog to appear
    pyautogui.press("tab")  # Navigate to the "Replace" button if not focused by default
    pyautogui.press("enter")  # Confirm replacement


def handle_download_dialog(file_name):
    time.sleep(2)  # Adjust based on when the dialog box appears
    pyautogui.write(file_name, interval=0.1)
    time.sleep(10)
    pyautogui.press("enter")

    try:
        # Assume the dialog appears if we can't proceed further
        handle_replace_dialog()
        print("Replace dialog handled.")
    except Exception as e:
        print(f"Error handling replace dialog: {e}")
    time.sleep(10)


def download_file(driver, file_name):

    # Locate the file to download (adjust XPath or search logic)

    file_rows = driver.find_elements(By.XPATH, '//*[@id="userUploads"]/tr')

    for file in file_rows:
        file_name_element = file.find_element(By.XPATH, " ./td[1]/div/small")

        if file_name_element.text == file_name:
            download_button = file.find_element(By.XPATH, './td[5]/div/a[@title="Download"]')
            download_button.click()
            time.sleep(5)

            handle_download_dialog(file_name)  # Handle the dialog box
            print(f"File '{file_name}' downloaded successfully.")
            time.sleep(3)
            return

    print(f"File '{file_name}' not found.")


# Function to test file deletion


def delete_file(driver, file_name):

    file_rows = driver.find_elements(By.XPATH, '//*[@id="userUploads"]/tr')

    for file in file_rows:
        file_name_element = file.find_element(By.XPATH, " ./td[1]/div/small")

        if file_name_element.text == file_name:
            delete_button = file.find_element(By.XPATH, './td[5]/div/button[@title="Delete"]')
            delete_button.click()
            time.sleep(2)

            # Switch to the alert and click OK to confirm deletion
            try:

                alert = Alert(driver)
                alert.accept()  # Click the OK button on the popup
                time.sleep(2)  # Wait for deletion to complete
                print(f"file {file_name} is successfully deleted")

            except Exception as e:
                print(f"Error occurred while handling alert: {e}")
            return

    print(f"File '{file_name}' not found.")  # If file is not found


def rename_file(driver, file_name, new_file_name):

    file_rows = driver.find_elements(By.XPATH, '//*[@id="userUploads"]/tr')

    for file in file_rows:
        file_name_element = file.find_element(By.XPATH, " ./td[1]/div/small")

        if file_name_element.text == file_name:
            rename_button = file.find_element(By.XPATH, './td[5]/div/button[@title="Rename"]')
            rename_button.click()
            time.sleep(5)

            rename_input = driver.find_element(By.XPATH, '//*[@id="renameFormControlInput"]')
            rename_input.send_keys(new_file_name)
            save_changes_button = driver.find_element(By.XPATH, '//*[@id="renameModal"]/div/div/form/div[3]/button')
            save_changes_button.click()
            time.sleep(2)
            return

    print(f"Could not file {file_name}")
