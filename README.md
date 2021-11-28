# VL_Chat_App
VL is a chat application built by some random students at Luther College.

Team members: Luc Vuong, Kevin Tu, Long Khuong, Bill Dang, Hudson Nguyen, Duy Nguyen, Tan Le. 

## Development
As we use Python 3.8 for testing, we expect that you use Python 3.8. Also, you should have **SQLite3** installed. For information about installing SQLite, please visit https://www.sqlite.org/draft/index.html

**Create and activate a virtual environment (recommended)**
```
$ python -m venv venv
$ . venv/bin/activate
```

**Install dependencies**
```
$ python -m pip install -r requirements.txt
```

**Configure Flask and start the application**
```
$ export FLASK_APP=message_app
$ export FLASK_ENV=development
$ flask run
```

**Populate sample database**

You can create a new database for development by using the SQL scripts from ```message-app.sql```

Step into the ```./message_app``` directory, then run the following command

```
$ sqlite3 message_app_db
```
Note: message_app_db is the name that will be used in deployment, and you can use your favorite name when developing locally.

Then, inside the sqlite shell, run

```
sqlite> .read message-app.sql
```

**A small issue between git and sqlite**



## Testing

### Check linting
```
$ flake8 .
```
 
### Run unit tests and functional tests

Tests related to a feature should be grouped into a class (e.g. class TestUserController)

Run your tests locally with [pytest](https://docs.pytest.org/en/6.2.x/contents.html#toc):

```$ python -m pytest ./path/to/test/file.py``` to test the whole file

```$ python -m pytest ./path/to/test/file.py::TestSomethingClass``` to test a specific class in the test file

You do not need to run the full test suite (all of the tests in the project) locally, as it is done by GitHub Actions when you create a pull request.
