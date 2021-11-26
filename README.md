# VL_Chat_App
VL is a chat application built by some random students at Luther College.

Team members: Luc Vuong, Kevin Tu, Long Khuong, Bill Dang, Hudson Nguyen, Duy Nguyen, Tan Le. 

## Development
As we use Python 3.8 for testing, we expect that you have Python 3.8 on your machine

**Create and activate a virtual environment (recommended)**
```
python -m venv venv
. venv/bin/activate
```

**Install dependencies**
```
python -m pip install -r requirements.txt
```

**Configure Flask and start the application**
```
export FLASK_APP=message_app
export FLASK_ENV=development
flask init-db
flask run
```

## Testing

### Linting
```
flake8 .
```
 
### Unit testing

Tests related to a feature should be grouped into a class (e.g. class TestUserController)

Run your unit tests locally with [pytest](https://docs.pytest.org/en/6.2.x/contents.html#toc):

```python -m pytest ./path/to/test/file.py``` to test the whole file

```python -m pytest ./path/to/test/file.py::TestSomethingClass``` to test a specific class in the test file

You do not need to run the full test suite locally, as it is done by GitHub Actions when you create a pull request.
