# Python Project Template

**Note** that Git Bash should be used on Windows to execute the bash scripts.

## Tools

### Virtual Environment

Run `tools/virtualenv.sh` to create a virtual environment.

Run `tools/activate.sh` to activate the virtual environment.

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
