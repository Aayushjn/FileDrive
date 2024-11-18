# FileDrive

## Getting Started

Install the requirements with `pip install -r requirements/development.txt`.

Install the pre-commit Git hook using `pre-commit install`.

All the below commands should be run from the [filedrive](./filedrive/) directory.

Generate the secret key

```bash
python -c "from django.core.management.utils import get_random_secret_key;import os;from base64 import b64encode;print(f'SECRET_KEY={b64encode(get_random_secret_key().encode('utf-8')).decode('utf-8')}')" > .env
```

Start the server with `python manage.py runserver`

When starting the server for the first time, let it generate database files, then quit and run the following commands:

```bash
python manage.py makemigrations
python manage.py migrate # needs to be run after every change to any DB models
```

To run the tests, simply run `pytest`
