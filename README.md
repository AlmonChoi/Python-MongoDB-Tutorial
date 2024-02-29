
# "Python-MongoDB-Tutorial"

[![PyPI version](https://badge.fury.io/py/google-api-python-client.svg)](https://badge.fury.io/py/google-api-python-client)

## Description

Simple Python program support Mongo database creation using direct access or via object Class 


## Built With

| Syntax | Description |
| --- | ----------- |
| ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) | Implementation of the API using FastAPI |
| ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white) | Data storage of the entities created through the API |
| ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) | Provide the required local environment in a container |


## Installation

Install Python virtual enviornment and required modules:

```bash
apt install -y python3.10-venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt     # include PyMongo
deactivate
```

## Run with Python virtual environment
```bash
docker-compose up -d
source .venv/bin/activate
python initdb.py                    # create user database
python test.py                      # test database operation
deactivate
docker-compose down
```

## Environment variable or configuration file
    export APP_CONFIG_MONGODB_URL="mongodb://username:password@localhost:27017/" 
    export APP_CONFIG_MONGODB_URL="mongodb://localhost:27017/" 
    export APP_CONFIG_MONGODB_NAME="database"

    "APP_CONFIG_MONGODB_URL" : "mongodb://localhost:27017/"
    "APP_CONFIG_MONGODB_URL" : "mongodb://username:password@localhost:27017/"
    "APP_CONFIG_MONGODB_NAME" : "database"


## / root folder
    - initdb.py     : To load initalize data from file ./init_data/data.json
    - test.py       : To test the function of Class

## ./init_data folder
    - data.json     : initalize user data to setup the database. 

## ./config
    - setting.json  : configuration file

## /lib
    - __init__.py   : python module folder
    - db.py         : Class Datasource
    - user.py       : Class User

