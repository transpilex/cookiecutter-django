# {{cookiecutter.project_name}}

{{ cookiecutter.description }}

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

- Django : 5.1.11
- Python : 3.12

## Settings

Moved to [settings](https://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/settings.html).

## Basic Commands

### Running Development Server

- To create a **Virtual Environment** on linux or mac, use this command:

      $ python3 -m venv environment_name
      $ source environment_name/bin/activate
- To create a **Virtual Environment** on windows, use this command:

      $ python -m venv environment_name
      $ environment_name/Scripts/activate

- To install **Dependencies**, use this command:

      $ pip install -r requirements/local.txt
- To sync **Database**, use this command:

      $ python manage.py migrate
- To run **Local Server**, use this command:

      $ python manage.py runserver

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy {{cookiecutter.project_slug}}

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest
