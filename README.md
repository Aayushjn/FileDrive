# FileDrive

## Getting Started

Install the requirements with `pip install -r requirements/development.txt`.

All the below commands should be run from the [filedrive](./filedrive/) directory.

Before starting the server for the first time

```bash
python manage.py makemigrations
python manage.py migrate # needs to be run after every change to any DB models
```

Start the server with `python manage.py runserver`

To run the tests, simply run `pytest`
