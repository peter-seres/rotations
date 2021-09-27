# Python-template

This is a template repository for starting a python project.
Includes the following automated testing:

- `pytest`: unit tests
- `mypy`: type hints
- `flake8`: linter
- `tox`: test multiple environments

Include / remove the packages you need for your project.

GitHub Actions are configured to run on a push or PR to the master branch.

Badge from GitHub Actions:

![Tests](https://github.com/Speterius/python-template/actions/workflows/test.yml/badge.svg)

## Environment:
 - Project dependencies: `requirements.txt`
 - Development dependencies: `requirements_dev.txt`

___
Use a virtual environment:

`python -m venv venv`

`venv/scripts/activate` (Win) or `source venv\bin\activate` (Linux)

The `test/` folder uses a general import of the packages inside `src/` so that the relative path doesn't matter.
Install the packages in `src/` using: `pip install -e .` (edit mode install)

The files `setup.cfg` and `setup.py` define how the packages will be installed.

## Pytest
Run unit tests and generate code coverage report.

Configuration: `pytest.ini`

## Mypy
Check the python code for correct type hinting.

Configuration file: `mypy.ini`


## Flake8
Python linter. Check the code formatting.

Configuration: inside `setup.cfg`


## Tox
Run the tests in multiple python environments

Configuration: `tox.ini`

## GitHub Actions
Run the tests on certain events.

Configuration: `.github/workflows/test.yml` and also `tox.ini`
