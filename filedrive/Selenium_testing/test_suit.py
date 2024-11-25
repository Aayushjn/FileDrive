import os
import unittest
import HTMLTestRunner
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import login_test
import file_management
import other_testing
import time


class BaseTest(unittest.TestCase):
    """Base test class to manage shared setup and teardown."""

    website = "http://127.0.0.1:8000/"
    email = "vandanaluhana810@gmail.com"
    password = "Insane_1704"

    @classmethod
    def setUpClass(cls):
        """Initialize the WebDriver and log in once for the test class."""
        options = Options()
        options.add_argument("--disable-infobars")
        options.add_argument("start-maximized")
        options.add_argument("--disable-extensions")
        prefs = {"download.prompt_for_download": True}
        options.add_experimental_option("prefs", prefs)

        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=options)

        # Perform login once for the test class
        cls.driver.get(cls.website)
        WebDriverWait(cls.driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        login_test.login(cls.driver, cls.website, cls.email, cls.password)
        print("Logged in successfully!")

    @classmethod
    def tearDownClass(cls):
        """Quit the WebDriver after all tests."""
        cls.driver.quit()
        print("WebDriver session closed.")


class FileManagementTests(BaseTest):
    """Tests for file management functionalities."""

    file_path = r"D:\BITS Pilani\Software System\SEM 3\STM\Combinatorial Testing Strategies.pdf"
    file_name = "lec1.pdf"
    new_file_name = "lec1_updated.pdf"

    def test_01_file_upload(self):
        """Test file upload functionality."""
        file_management.check_upload(self.driver, self.file_path)
        print("File upload test completed.")

    def test_02_file_download(self):
        """Test file download functionality."""
        file_management.download_file(self.driver, self.file_name)
        print("File download test completed.")

    def test_03_file_delete(self):
        """Test file deletion functionality."""
        file_management.delete_file(self.driver, "RTS_Aayushs_notes.pdf")
        print("File deletion test completed.")

    def test_04_file_rename(self):
        """Test file rename functionality."""
        file_management.rename_file(self.driver, self.file_name, self.new_file_name)
        print("File rename test completed.")


class NavigationTests(BaseTest):
    """Tests for navigation functionalities."""

    def test_01_shared_with_me(self):
        """Test navigation to Shared with Me section."""
        other_testing.check_shared_with_me(self.driver)
        print("Navigation to Shared with Me test completed.")

    def test_02_home_button(self):
        """Test navigation to Home section."""
        other_testing.check_home_button(self.driver)
        print("Navigation to Home test completed.")


class AuthenticationTests(BaseTest):
    """Tests for authentication functionalities."""

    new_email = "abc@gmail.com"
    first_name = "John"
    last_name = "Peter"
    new_password = "insane810"

    def test_01_registration(self):
        """Test user registration functionality."""
        login_test.register(self.driver, self.new_email, self.first_name, self.last_name, self.new_password)
        print("User registration test completed.")

    def test_02_login_logout(self):
        """Test login and logout functionality."""
        login_test.login(self.driver, self.website, self.email, self.password)
        login_test.logout(self.driver)
        print("Login and logout test completed.")


def create_test_suite():
    """Create a test suite combining all test classes."""
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(AuthenticationTests))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(FileManagementTests))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(NavigationTests))
    return suite


if __name__ == "__main__":
    # Configure the HTMLTestRunner
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
    os.makedirs(output_dir, exist_ok=True)

    runner = HTMLTestRunner.HTMLTestRunner(
        output=output_dir,
        report_name="TestReport",
        report_title="Application Functional Test Report",
        combine_reports=True,
    )

    # Run the test suite
    runner.run(create_test_suite())
