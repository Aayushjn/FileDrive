# FileDrive

## Getting Started

### Installation
Install the requirements with `pip install -r requirements/development.txt`.

Install the pre-commit Git hook using `pre-commit install`.

### Configuration

All the below commands should be run from the [filedrive](./filedrive/) directory.

#### Generate the secret key

```bash
python -c "from django.core.management.utils import get_random_secret_key;import os;from base64 import b64encode;print(f'SECRET_KEY={b64encode(get_random_secret_key().encode('utf-8')).decode('utf-8')}')" > .env
```

#### Create a superuser

You can register a new user from the UI, however, that won't be a superuser and you will be unable to access the admin page. If you register via the UI, you can give superuser access via the shell (`python manage.py shell`).

```python
from core.models import User
u = User.objects.get(email="<my_email_id")
u.is_superuser = True
u.is_staff = True
u.save()
```

Alternatively, you can run `python manage.py createsuperuser`. Note that you will have to set the first and last name from the shell or the admin page.

#### Starting the server

Start the server with `python manage.py runserver`

When starting the server for the first time, let it generate database files, then quit and run the following commands:

```bash
python manage.py makemigrations
python manage.py migrate # needs to be run after every change to any DB models
```

#### Testing

To run the unit tests, simply run `pytest`

#### Prerequisites
Ensure the following are installed:
- **Python 3.x**
- **pytest**: `pip install pytest`
- **pytest-cov**: `pip install pytest-cov` for coverage testing.

#### Steps

1. **Navigate to the directory**:
   ```bash
   cd FileDrive\filedrive
   ```

2. **Run Tests**:
   ```bash
   pytest --verbose
   ```

3. **Test for Code Coverage**:
   ```bash
   pytest --cov=<tests_folder_path> --cov-report=html
   ```
    Replace `<tests_folders_path>` with your tests folder path.

1. **Generate Allure Report**:
   ```bash
   allure generate --single-file .\allure-results\
   ```

Ensure all dependencies are set up and paths adjusted as needed. This will run all tests and generate an Allure report in the `allure-report` directory. Open the `index.html` file in a web browser to view the report.