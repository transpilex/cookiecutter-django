import json
import random
import shutil
import string
from pathlib import Path

try:
    # Inspired by
    # https://github.com/django/django/blob/main/django/utils/crypto.py
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

DEBUG_VALUE = "debug"

def remove_custom_user_manager_files():
    users_path = Path("{{cookiecutter.project_slug}}", "users")
    (users_path / "managers.py").unlink()
    (users_path / "tests" / "test_managers.py").unlink()


def remove_pycharm_files():
    idea_dir_path = Path(".idea")
    if idea_dir_path.exists():
        shutil.rmtree(idea_dir_path)

    docs_dir_path = Path("docs", "pycharm")
    if docs_dir_path.exists():
        shutil.rmtree(docs_dir_path)


def remove_utility_files():
    shutil.rmtree("utility")


def remove_heroku_files():
    file_names = ["Procfile", "requirements.txt"]
    for file_name in file_names:
        if file_name == "requirements.txt" and "{{ cookiecutter.ci_tool }}".lower() == "travis":
            # don't remove the file if we are using travisci but not using heroku
            continue
        Path(file_name).unlink()
    shutil.rmtree("bin")


def remove_gulp_files():
    file_names = ["gulpfile.js"]
    for file_name in file_names:
        Path(file_name).unlink()


def remove_packagejson_file():
    file_names = ["package.json"]
    for file_name in file_names:
        Path(file_name).unlink()


def update_package_json(remove_dev_deps=None, remove_keys=None, scripts=None):
    remove_dev_deps = remove_dev_deps or []
    remove_keys = remove_keys or []
    scripts = scripts or {}
    package_json = Path("package.json")
    content = json.loads(package_json.read_text())
    for package_name in remove_dev_deps:
        content["devDependencies"].pop(package_name)
    for key in remove_keys:
        content.pop(key)
    content["scripts"].update(scripts)
    updated_content = json.dumps(content, ensure_ascii=False, indent=2) + "\n"
    package_json.write_text(updated_content)


def handle_js_runner(choice, use_docker, use_async):
    if choice == "Gulp":
        update_package_json(
            scripts={
                "dev": "gulp",
                "build": "gulp build",
            },
        )


def remove_celery_files():
    file_paths = [
        Path("config", "celery_app.py"),
        Path("{{ cookiecutter.project_slug }}", "users", "tasks.py"),
        Path("{{ cookiecutter.project_slug }}", "users", "tests", "test_tasks.py"),
    ]
    for file_path in file_paths:
        file_path.unlink()


def remove_async_files():
    file_paths = [
        Path("config", "asgi.py"),
        Path("config", "websocket.py"),
    ]
    for file_path in file_paths:
        file_path.unlink()


def generate_random_string(length, using_digits=False, using_ascii_letters=False, using_punctuation=False):
    """
    Example:
        opting out for 50 symbol-long, [a-z][A-Z][0-9] string
        would yield log_2((26+26+50)^50) ~= 334 bit strength.
    """
    if not using_sysrandom:
        return None

    symbols = []
    if using_digits:
        symbols += string.digits
    if using_ascii_letters:
        symbols += string.ascii_letters
    if using_punctuation:
        all_punctuation = set(string.punctuation)
        # These symbols can cause issues in environment variables
        unsuitable = {"'", '"', "\\", "$"}
        suitable = all_punctuation.difference(unsuitable)
        symbols += "".join(suitable)
    return "".join([random.choice(symbols) for _ in range(length)])


def set_flag(file_path: Path, flag, value=None, formatted=None, *args, **kwargs):
    if value is None:
        random_string = generate_random_string(*args, **kwargs)
        if random_string is None:
            print(
                "We couldn't find a secure pseudo-random number generator on your "
                "system. Please, make sure to manually {} later.".format(flag)
            )
            random_string = flag
        if formatted is not None:
            random_string = formatted.format(random_string)
        value = random_string

    with file_path.open("r+") as f:
        file_contents = f.read().replace(flag, value)
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    return value


def set_django_secret_key(file_path: Path):
    django_secret_key = set_flag(
        file_path,
        "!!!SET DJANGO_SECRET_KEY!!!",
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )
    return django_secret_key


def set_django_admin_url(file_path: Path):
    django_admin_url = set_flag(
        file_path,
        "!!!SET DJANGO_ADMIN_URL!!!",
        formatted="{}/",
        length=32,
        using_digits=True,
        using_ascii_letters=True,
    )
    return django_admin_url

def append_to_gitignore_file(ignored_line):
    with Path(".gitignore").open("a") as gitignore_file:
        gitignore_file.write(ignored_line)
        gitignore_file.write("\n")


def set_flags_in_envs():
    production_django_envs_path = Path(".envs", ".production", ".django")

    set_django_secret_key(production_django_envs_path)
    set_django_admin_url(production_django_envs_path)


def set_flags_in_settings_files():
    set_django_secret_key(Path("config", "settings", "local.py"))
    set_django_secret_key(Path("config", "settings", "test.py"))


def remove_envs_and_associated_files():
    shutil.rmtree(".envs")
    Path("merge_production_dotenvs_in_dotenv.py").unlink()
    shutil.rmtree("tests")


def remove_drf_starter_files():
    Path("config", "api_router.py").unlink()
    shutil.rmtree(Path("{{cookiecutter.project_slug}}", "users", "api"))
    shutil.rmtree(Path("{{cookiecutter.project_slug}}", "users", "tests", "api"))


def main():

    set_flags_in_envs()

    set_flags_in_settings_files()

    if "{{ cookiecutter.username_type }}" == "username":
        remove_custom_user_manager_files()

    if "{{ cookiecutter.editor }}" != "PyCharm":
        remove_pycharm_files()

    if "{{ cookiecutter.use_docker }}".lower() == "y":
        remove_utility_files()

    if "{{ cookiecutter.use_heroku }}".lower() == "n":
        remove_heroku_files()

    if "{{ cookiecutter.use_docker }}".lower() == "n" and "{{ cookiecutter.use_heroku }}".lower() == "n":
        if "{{ cookiecutter.keep_local_envs_in_vcs }}".lower() == "y":
            print(
                INFO + ".env(s) are only utilized when Docker Compose and/or "
                "Heroku support is enabled so keeping them does not make sense "
                "given your current setup." + TERMINATOR
            )
        remove_envs_and_associated_files()
    else:
        append_to_gitignore_file(".env")
        append_to_gitignore_file(".envs/*")
        if "{{ cookiecutter.keep_local_envs_in_vcs }}".lower() == "y":
            append_to_gitignore_file("!.envs/.local/")

    if "{{ cookiecutter.frontend_pipeline }}" in ["None", "Django Compressor"]:
        remove_gulp_files()
        remove_packagejson_file()
    else:
        handle_js_runner(
            "{{ cookiecutter.frontend_pipeline }}",
            use_docker=("{{ cookiecutter.use_docker }}".lower() == "y"),
            use_async=("{{ cookiecutter.use_async }}".lower() == "y"),
        )

    if "{{ cookiecutter.cloud_provider }}" == "None" and "{{ cookiecutter.use_docker }}".lower() == "n":
        print(
            WARNING + "You chose to not use any cloud providers nor Docker, "
            "media files won't be served in production." + TERMINATOR
        )

    if "{{ cookiecutter.use_celery }}".lower() == "n":
        remove_celery_files()

    if "{{ cookiecutter.use_drf }}".lower() == "n":
        remove_drf_starter_files()

    if "{{ cookiecutter.use_async }}".lower() == "n":
        remove_async_files()

    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)


if __name__ == "__main__":
    main()
