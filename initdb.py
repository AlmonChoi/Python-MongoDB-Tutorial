#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Reading configuration settings from i) environment variable or ii) ./config/settings.json
# Remove old datbase if existed
# import collection fronm ./init_data/data.json

import os
import sys
import pymongo
import json
from datetime import datetime
from datetime import timedelta 

from lib.db import DataSource 
# sys.tracebacklimit=0

conf_file = "./config/settings.json"
init_data = "./init_data/data.json"

def init_main1():
    # loading initalial data to mongoDB using method 1 - directly using pymongo module 
    # MongoDB module pymongo used
    
    setting_file = open(conf_file, "rt")
    config_value = json.loads(setting_file.read())

    db_connection = pymongo.MongoClient(config_value["APP_CONFIG_MONGODB_URL"])
    db_name = config_value["APP_CONFIG_MONGODB_NAME"]

    db_list = db_connection.list_database_names()

    if db_name in db_list:
        print("INFO : Database {} existed and will be dropped".format(db_name))
        db_connection.drop_database(db_name)

    data_file = open(init_data, "rt")
    test_data = json.loads(data_file.read())

    db_name = db_connection[db_name]

    for key in test_data.keys():
        print("INFO: Import collection : ", key)
        collection_name = db_name[key] 
        if str(type(test_data[key])) in ["<class 'dict'>"]:
            collection_name.insert_one(test_data[key])
        else:
            collection_name.insert_many(test_data[key])

def init_main2():
    # loading initalial data to mongoDB using method 2 - inddirectly using pymongo module via Class 
    db = DataSource()

    if db.connect is None:
        print("ERROR : Unable to connect, please check connection string or database service") 
        os._exit(1)
    else:
        database_list = db.connect.list_database_names()
        print ("INFO : Database connected. Existed database are", database_list)

    if (db.database in database_list):
        print("INFO : Database {} existed and will be dropped".format(db.database))
        db.connect.drop_database(db.database)

    data_file = open(init_data, "rt")
    test_data = json.loads(data_file.read())
    data_file.close()

    for key in test_data.keys():
        print("INFO : Import collection - ", key, sep="")
        if str(type(test_data[key])) in ["<class 'dict'>"]:
            db.insert_one(key, test_data[key])
        else:
            db.insert_many(key, test_data[key])

    for key in test_data.keys():
        if (test_data[key] == db.query(key)):
            print("INFO : Collection {} matched database ".format(key))
        else:
            print("ERROR : Collection {} not matched database ".format(key))

if __name__ == '__main__':
    init_main2()
