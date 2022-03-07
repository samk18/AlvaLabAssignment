# Transaction Management REST API With Flask & SQL Alchemy

> Products API using Python Flask, SQL Alchemy and Marshmallow

## Quick Start Using Pipenv

``` bash
# Activate venv
$ pipenv shell

# Install dependencies
$ pipenv install

# Create DB
$ python
>> from app import db
>> db.create_all()
>> exit()

# Run Server (http://localhst:5000)
python app.py
```

## Endpoints

* GET     /ping
* POST    /transactions/
* GET     /transactions/
* GET     /transactions/:id
* GET     /accounts/:id
* PUT     /transaction/:id
* DELETE  /transaction/:id
