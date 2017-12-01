# Betcha - Backend

This project was created for CS 307 - Software Engineering at Purdue University. This is the Backend built on Flask for the corresponding Android client hosted in the accompanying [repository](https://github.com/ThreeOhSeven/Frontend).

## Getting Started

### Setting up Dev Environment

1. Ensure that you have python3 installed and updated
2. Clone this repo
3. Run `pip install flask flask-sqlalchemy flask-migrate flask-api mysql-python`
4. Find the `config.py` file on the `#general` channel on Slack, download it, and place the file in the app folder
5. Run `export FLASK_CONFIG=development`
6. Run `export FLASK_APP=run.py`
5. Run `flask run`

### To Add Table to Database

1. Add a new class to `models.py`
2. Run `python3 manage.py db migrate` to create the migration file
3. Run `python3 manage.py db upgrade` to update the database

## Authors

* **Peter Jones** - [pickles72](https://github.com/pickles72)
* **Siddarth Shah** - [exponentialbit1024](https://github.com/exponentialbit1024)
* **Noah Smith** - [noahismith](https://github.com/noahismith)
