# Thesis Backend
This repository contains the backend for a prototype implementation for a master's thesis for the Aarhus University, Department of Computer Science.
More information in the main repository [videostrates-thesis-project/thesis-project](https://github.com/videostrates-thesis-project/thesis-project)

## Development
### Environment Variables
Required environment variables are specified in `.env.example`. Copy this file to `.env` and fill in the values.

### Running the Application
- \[Optional\] Create a virtual environment
- Install dependencies with `tools/install.sh`
- Run the application with `python .\src\app.py`

## Tools

### Dependencies

Run `tools/install.sh` to install both production and test dependencies.

### Linter

Run `tools/lint.sh` to execute linter and code formatter tools.
Some of the tools can be configured in `pyproject.toml`.

### Test

Run `tools/test.sh` to execute linter and unit tests.

### Docs

Run `tools/docs.sh` to build the documentation.
mkdocs can be configured in `mkdocs.yml`.
