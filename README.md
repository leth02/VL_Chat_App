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

<<<<<<< HEAD
Step into the ```./message_app/db``` directory, then run the following command
=======
Step into the ```./message_app``` directory, then run the following command
>>>>>>> cb91a212309579be17a75823532ed9cd904c15e7

```
$ sqlite3 message_app_db
```
Note: message_app_db is the name that will be used in deployment, and you can use your favorite name when developing locally.

Then, inside the sqlite shell, run

```
sqlite> .read message-app.sql
```

**A small issue between git and sqlite**

Even though ```*.sqlite3``` has been added to ```.gitignore```, the binary Sqlite database files are still listed when you run ```git status```. This issue is on Windows, and I am not sure if this issue is applicable to Linux/MacOS.

If you run into this issue, there are two solutions:

1) Add new/modified files to git staging area *one by one*, and skip the binary database files. If you run ```git add .```, it might add the binary database file into git staging area.

2) Delete the binary database file, then you can use ```git add .``` safely because the database file is no longer present (you can use ```git status``` to check before doing ```git add .```)

3) Temporary solution: For line 34, use "sqlite3 message_app_db.sqlite3" instead of "sqlite3 message_app_db". This will guarantee gitignore recognize the database.


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
