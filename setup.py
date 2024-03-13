import io
import os
from setuptools import find_packages, setup

# Project metadata
project_name = "thesis_backend"
author = "Your Name"
# email="your@email.com"
description = f"Awesome project '{project_name}' created by {author}"


def read(*paths, **kwargs):
    """Read the contents of a text file safely
    """

    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name=project_name,
    version=read("VERSION"),
    description=description,
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author=author,
    # author_email=email,
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": [f"{project_name} = src.__main__:main"]
    },
    extras_require={"test": read_requirements("requirements-test.txt")},
)
