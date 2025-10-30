# Cookiecutter Django


## Features

- For Django 5.2
- Works with Python 3.13
- Renders Django projects with 100% starting test coverage
- [12-Factor](https://12factor.net) based settings via [django-environ](https://github.com/joke2k/django-environ)
- Secure by default. We believe in SSL.
- Optimized development and production settings
- Registration via [django-allauth](https://github.com/pennersr/django-allauth)
- Comes with custom user model ready to go
- Optional basic ASGI setup for Websockets
- Optional custom static build using Gulp or Webpack
- Send emails via [Anymail](https://github.com/anymail/django-anymail) (using [Mailgun](http://www.mailgun.com/) by default or Amazon SES if AWS is selected cloud provider, but switchable)
- Media storage using Amazon S3, Google Cloud Storage, Azure Storage or nginx
- Run tests with unittest or pytest

## Usage

Let's pretend you want to create a Django project called "redditclone". Rather than using `startproject`
and then editing the results to include your name, email, and various configuration issues that always get forgotten until the worst possible moment, get [cookiecutter](https://github.com/cookiecutter/cookiecutter) to do all the work.

First, get Cookiecutter. Trust me, it's awesome:

    uv tool install "cookiecutter>=1.7.0"

Now run it against this repo:

    uvx cookiecutter https://github.com/transpilex/cookiecutter-django

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
    version [1.0.0]: 0.0.1
    Select open_source_license:
    1 - MIT
    2 - BSD
    3 - GPLv3
    4 - Apache Software License 2.0
    5 - Not open source
    Choose from 1, 2, 3, 4, 5 [1]: 1
    Select cloud_provider:
    1 - AWS
    2 - GCP
    3 - Azure
    4 - None
    Choose from 1, 2, 3, 4 [1]: 1
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
    Select ui_library:
    1 - None
    2 - Bootstrap
    3 - Tailwind
    Choose from 1, 2, 3 [1]: 1
    Select frontend_pipeline:
    1 - None
    2 - Gulp
    3 - Vite
    Choose from 1, 2, 3 [1]: 1
    use_auth [n]: n
