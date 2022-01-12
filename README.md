# VL_Chat_App
VL is an open-source chat application built with Python and JavaScript

## Development
Please have Python 3 and SQLite3 installed on your machine.

**Create and activate a virtual environment (optional but recommended)**
```
python -m venv venv
. venv/bin/activate
```

**Install dependencies**
```
python -m pip install -r requirements.txt
```

**Start the application**
```
python main.py
```

## Testing

### Check linting
```
flake8 .
```

### Run unit tests and integration tests

Tests related to a feature should be grouped into a class (e.g. class TestUserController)

Run your tests locally with [pytest](https://docs.pytest.org/en/6.2.x/contents.html#toc):

```python -m pytest ./path/to/test/file.py``` to test the whole file

```python -m pytest ./path/to/test/file.py::TestSomethingClass``` to test a specific class in the test file

You do not need to run the full test suite (all of the tests in the project) locally, as it is done by GitHub Actions when you create a pull request.
