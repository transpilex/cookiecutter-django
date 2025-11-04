# ruff: noqa: PLR0133
import json
import random
import shutil
import string
import subprocess
import sys
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


def remove_auth_files():
    auth_dir_path = Path("{{cookiecutter.project_slug}}", "templates", "account")
    if auth_dir_path.exists():
        shutil.rmtree(auth_dir_path)


def remove_gulp_files():
    file_names = ["gulpfile.js"]
    for file_name in file_names:
        Path(file_name).unlink()


def remove_vite_files():
    file_names = ["vite.config.js"]
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


def handle_js_runner(frontend_pipeline, ui_library):
    if frontend_pipeline == "Gulp":
        if ui_library == "Tailwind":
            scripts = {
                "dev": "gulp",
                "build": "gulp build"
            }
            remove_dev_deps = [
                "@tailwindcss/vite",
                "glob",
                "path",
                "vite",
                "sass",
                "gulp-sass",
                "gulp-sourcemaps",
                "gulp-rtlcss",
                "gulp-clean-css"
            ]
        else:
            scripts = {
                "dev": "gulp",
                "build": "gulp build",
                "rtl": "gulp rtl",
                "rtl-build": "gulp rtlBuild"
            }
            remove_dev_deps = [
                "@tailwindcss/postcss",
                "@tailwindcss/vite",
                "autoprefixer",
                "glob",
                "path",
                "vite"
            ]
        update_package_json(remove_dev_deps=remove_dev_deps, scripts=scripts)
        remove_vite_files()
    elif frontend_pipeline == "Vite":
        scripts = {
            "dev": "vite",
            "build": "vite build"
        }
        if ui_library == "Tailwind":
            remove_dev_deps = [
                "@tailwindcss/postcss",
                "autoprefixer",
                "cssnano",
                "gulp",
                "gulp-clean-css",
                "gulp-concat",
                "gulp-plumber",
                "gulp-npm-dist",
                "gulp-postcss",
                "gulp-rename",
                "gulp-rtlcss",
                "gulp-sass",
                "gulp-sourcemaps",
                "pixrem",
                "postcss",
                "sass"
            ]
        else:
            remove_dev_deps = [
                "@tailwindcss/postcss",
                "@tailwindcss/vite",
                "autoprefixer",
                "cssnano",
                "gulp",
                "gulp-clean-css",
                "gulp-concat",
                "gulp-plumber",
                "gulp-npm-dist",
                "gulp-postcss",
                "gulp-rename",
                "gulp-rtlcss",
                "gulp-sass",
                "gulp-sourcemaps",
                "pixrem",
                "postcss"
            ]

        update_package_json(remove_dev_deps=remove_dev_deps, scripts=scripts)
        remove_gulp_files()


def generate_random_string(length, using_digits=False, using_ascii_letters=False,
                           using_punctuation=False):  # noqa: FBT002
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
                f"system. Please, make sure to manually {flag} later.",
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
    return set_flag(
        file_path,
        "!!!SET DJANGO_SECRET_KEY!!!",
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )


def set_flags_in_settings_files():
    set_django_secret_key(Path("config", "settings", "local.py"))
    set_django_secret_key(Path("config", "settings", "test.py"))


def remove_drf_starter_files():
    Path("config", "api_router.py").unlink()
    shutil.rmtree(Path("{{cookiecutter.project_slug}}", "users", "api"))
    shutil.rmtree(Path("{{cookiecutter.project_slug}}", "users", "tests", "api"))


def main():
    set_flags_in_settings_files()

    if "{{ cookiecutter.frontend_pipeline }}" in ["None"]:
        remove_gulp_files()
        remove_vite_files()
        remove_packagejson_file()
    else:
        handle_js_runner("{{ cookiecutter.frontend_pipeline }}", "{{ cookiecutter.ui_library }}")

    if "{{ cookiecutter.use_drf }}".lower() == "n":
        remove_drf_starter_files()

    if "{{ cookiecutter.use_auth }}".lower() == "n":
        remove_auth_files()

    setup_dependencies()

    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)


def setup_dependencies():
    print("Installing python dependencies using uv...")

    uv_cmd = ["uv"]

    # Install production dependencies
    try:
        subprocess.run([*uv_cmd, "add", "--no-sync", "-r", "requirements/production.txt"], check=True)  # noqa: S603
    except subprocess.CalledProcessError as e:
        print(f"Error installing production dependencies: {e}", file=sys.stderr)
        sys.exit(1)

    # Install local (development) dependencies
    try:
        subprocess.run([*uv_cmd, "add", "--no-sync", "--dev", "-r", "requirements/local.txt"], check=True)  # noqa: S603
    except subprocess.CalledProcessError as e:
        print(f"Error installing local dependencies: {e}", file=sys.stderr)
        sys.exit(1)

    print("Setup complete!")


if __name__ == "__main__":
    main()
