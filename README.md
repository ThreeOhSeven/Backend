# Betcha - Backend

Betcha is a custom, social betting application that was created for CS 307 - Software Engineering at Purdue University. This is the Backend built on Flask for the corresponding Android client hosted in the accompanying [repository](https://github.com/ThreeOhSeven/Frontend). Further documentation can be found [here](https://github.com/ThreeOhSeven/Documents)

## Getting Started

### Prerequisites

You will need a set of python libraries to run this application

```
pip3 install flask flask-sqlalchemy flask-migrate flask-api mysql-python pyfcm web3 stripe
```

Additionally, an ethereum node is required to process any transactions. The blockchain can be hosted on any server as long as the IP address is placed in its correct location in the blockchain.py file.

### Setting up Dev Environment

1. Ensure that you have python3 installed and updated
2. Clone this repo
3. Run `pip3 install flask flask-sqlalchemy flask-migrate flask-api mysql-python`
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
