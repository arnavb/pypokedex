import os
import re

from setuptools import setup, find_packages

this_directory = os.path.abspath(os.path.dirname(__file__))

# Get long description from README.md
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as readme_file:
    long_description = readme_file.read()

# Get package version from pypokedex/__init__.py
with open(os.path.join(this_directory, "pypokedex", "__init__.py")) as version_file:
    version = re.search(
        r'^__version__ = [\'"]([^\'"]*)[\'"]', version_file.read(), re.M
    ).group(1)

setup(
    name="pypokedex",
    version=version,
    description="A minimal pokedex library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arnavb/pypokedex",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries",
    ],
    author="Arnav Borborah",
    author_email="arnavborborah11@gmail.com",
    license="MIT",
    packages=find_packages(exclude=["tests", "docs"]),
    install_requires=["requests>=2.21.0"],
    python_requires=">=3.6",
)
