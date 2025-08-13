# Cookiecutter Django


## Features

- For Django 5.1
- Works with Python 3.12
- Renders Django projects with 100% starting test coverage
- [12-Factor](https://12factor.net) based settings via [django-environ](https://github.com/joke2k/django-environ)
- Secure by default. We believe in SSL.
- Optimized development and production settings
- Registration via [django-allauth](https://github.com/pennersr/django-allauth)
- Comes with custom user model ready to go
- Optional basic ASGI setup for Websockets
- Optional custom static build using Gulp
- Send emails via [Anymail](https://github.com/anymail/django-anymail) (using [Mailgun](http://www.mailgun.com/) by default or Amazon SES if AWS is selected cloud provider, but switchable)
- Media storage using Amazon S3, Google Cloud Storage, Azure Storage or nginx
- [Procfile](https://devcenter.heroku.com/articles/procfile) for deploying to Heroku
- Instructions for deploying to [PythonAnywhere](https://www.pythonanywhere.com/)
- Run tests with unittest or pytest
- Default integration with [pre-commit](https://github.com/pre-commit/pre-commit) for identifying simple issues before submission to code review


## Usage

Let's pretend you want to create a Django project called "redditclone". Rather than using `startproject`
and then editing the results to include your name, email, and various configuration issues that always get forgotten until the worst possible moment, get [cookiecutter](https://github.com/cookiecutter/cookiecutter) to do all the work.

First, get Cookiecutter. Trust me, it's awesome:

    pip install "cookiecutter>=1.7.0"

Now run it against this repo:

    cookiecutter https://github.com/transpilex/cookiecutter-django

You'll be prompted for some values. Provide them, then a Django project will be created for you.

Answer the prompts with your own desired [options](http://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/project-generation-options.html). For example:

    Cloning into 'cookiecutter-django'...
    remote: Counting objects: 550, done.
    remote: Compressing objects: 100% (310/310), done.
    remote: Total 550 (delta 283), reused 479 (delta 222)
    Receiving objects: 100% (550/550), 127.66 KiB | 58 KiB/s, done.
    Resolving deltas: 100% (283/283), done.
    project_name [My Awesome Project]: Reddit Clone
    project_slug [reddit_clone]: reddit
    description []: A reddit clone.
    author_name []: Dan
    domain_name [example.com]: myreddit.com
    email [daniel-greenfeld@example.com]: pydanny@gmail.com
    version [0.1.0]: 0.0.1
    Select open_source_license:
    1 - MIT
    2 - BSD
    3 - GPLv3
    4 - Apache Software License 2.0
    5 - Not open source
    Choose from 1, 2, 3, 4, 5 [1]: 1
    Select username_type:
    1 - username
    2 - email
    Choose from 1, 2 [1]: 1
    timezone [UTC]: America/Los_Angeles
    windows [n]: n
    Select an editor to use. The choices are:
    1 - None
    2 - PyCharm
    3 - VS Code
    Choose from 1, 2, 3 [1]: 1
    use_docker [n]: n
    Select cloud_provider:
    1 - AWS
    2 - GCP
    3 - None
    Choose from 1, 2, 3 [1]: 1
    Select mail_service:
    1 - Mailgun
    2 - Amazon SES
    3 - Mailjet
    4 - Mandrill
    5 - Postmark
    6 - Sendgrid
    7 - Brevo (formerly SendinBlue)
    8 - SparkPost
    9 - Other SMTP
    Choose from 1, 2, 3, 4, 5, 6, 7, 8, 9 [1]: 1
    use_async [n]: n
    use_drf [n]: y
    Select frontend_pipeline:
    1 - None
    2 - Django Compressor
    3 - Gulp
    Choose from 1, 2, 3 [1]: 1
    use_celery [n]: y
    use_mailpit [n]: n
    use_sentry [n]: y
    use_whitenoise [n]: n
    use_heroku [n]: y
    Select ci_tool:
    1 - None
    2 - Travis
    3 - Gitlab
    4 - Github
    Choose from 1, 2, 3, 4 [1]: 4
    keep_local_envs_in_vcs [y]: y
    debug [n]: n
    auth [n]: n
