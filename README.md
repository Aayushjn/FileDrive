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

Code coverage can be tested using `pytest --cov=<tests_folder_path> --cov-report=html`

A report for all tests can be generated using `allure generate --single-file .\allure-results\`
