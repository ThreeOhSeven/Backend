# Backend

# Setting up Dev Environment
1. Ensure that you have python3 installed and updated
2. Clone this repo
3. Run `pip install flask flask-sqlalchemy flask-migrate flask-api mysql-python`
4. Find the `config.py` file on the `#general` channel on Slack, download it, and place the file in the app folder
5. Run `export FLASK_CONFIG=development`
6. Run `export FLASK_APP=run.py`
5. Run `flask run`

# To Add Table to Database
1. Add a new class to `models.py`
2. Run `python3 manage.py db migrate` to create the migration file
3. Run `python3 manage.py flask db upgrade` to update the database