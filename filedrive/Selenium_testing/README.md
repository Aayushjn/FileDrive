# Selenium Testing Suite

## Overview

This project automates the testing of a web application using Selenium WebDriver. The test suite includes functionalities for authentication, file management, and navigation. It is built using Python's `unittest` framework and generates HTML reports with `HtmlTestRunner`.

## Features

- **Authentication Tests**: Register, login, and logout functionality.
- **File Management Tests**: File upload, download, rename, and delete operations.
- **Navigation Tests**: Validate navigation between different sections of the application.
- **HTML Test Reports**: Detailed and user-friendly reports for test results.

---

## Getting Started


### Installation

Install dependency

   ```bash 
    pip install -r requirements.txt
```

### Configuration

  Setting Up ChromeDriver
  webdriver-manager automatically handles ChromeDriver installation. Ensure the version of ChromeDriver matches your Chrome browser version.


#### Update the test script to use your application URL, email, and password. For example, in test_suite.py:

```bash
website = "http://127.0.0.1:8000/"
email = "your-email@example.com"
password = "your-password"

```

### File Paths in file_management.py
In file_management.py, you need to specify the correct file paths for the files to be uploaded, renamed, or deleted. Modify the file paths in file_management.py to point to the correct locations on your machine.

For example, if the file to upload is located at C:\Users\YourUsername\Documents\example_file.pdf, update the file_path variable like this:

```bash
file_path = r"C:\Users\YourUsername\Documents\example_file.pdf"
```

Ensure that you also adjust paths for other file operations (such as renaming or deleting files) to reflect the correct files and locations on your local machine.

Example paths:

```bash

# File to upload
file_path = r"C:\path\to\your\file_to_upload.pdf"

# File to download (ensure this file exists in your UI before running tests)
file_name = "lec1.pdf"

# File to rename
file_name = "lec1.pdf"
new_file_name = "lec1_updated.pdf"

# File to delete
file_to_delete = "example_file_to_delete.pdf"
```

### Running the Tests

#### Executing the Full Test Suite

Run the following command to execute all test cases and generate an HTML report:

```bash

python test_suite.py
```
This script uses HtmlTestRunner to generate an HTML report located in the reports/ folder after execution.

#### Running Individual Test Scripts

To run specific test scripts, execute:

```bash

python testing.py
```

**Note: The testing.py script does not generate a report. It runs the tests but doesn't use HtmlTestRunner.** 

After running test_suite.py, HTML reports will be generated in the reports directory. Open the report file in a browser to view detailed results.

### Folder Structure

```bash
├── Selenium_testing/
│   ├── file_management.py      # Handles file upload, download, delete, rename
│   ├── login_test.py           # Manages authentication (login, logout, registration)
│   ├── other_testing.py        # Navigation-related test functions
│   ├── test_suite.py           # Main test suite for all test cases, generates HTML reports
│   ├── testing.py              # Script for standalone testing (no report generation)
│   ├── reports/                # Generated HTML reports
│   ├── requirements.txt        # Project dependencies
│   ├── README.md               # Project documentation
│
└── ...
```
### If you get error "HTMLTestRunner " module is not found, then try following steps.

```bash
pip install html_testRunner
```
And in test_suit.py make the following changes.

Replace

```bash
import HTMLTestRunnner
```

With

```bash
import HtmlTestRunnner
```
