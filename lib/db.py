#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import json
from types import NoneType
import pymongo

class DataSource:
    '''
    Used for database table operation 
    ''' 

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        '''
        Reading connection string from Environement varaible first
        If not, found try the local config file
        Create database connector and test if any connection error
        '''
        conf_file = "./config/settings.json"
        self.current_time = datetime.datetime.now()
               
        if ('APP_CONFIG_MONGODB_URL' in os.environ) & ('APP_CONFIG_MONGODB_NAME' in os.environ):
            connection_string = os.environ.get('APP_CONFIG_MONGODB_URL')
            self.database = os.environ.get('APP_CONFIG_MONGODB_NAME')

        elif os.path.isfile(conf_file):
            setting_file = open(conf_file, "rt")
            config_value = json.loads(setting_file.read())
            connection_string = config_value["APP_CONFIG_MONGODB_URL"]
            self.database = config_value["APP_CONFIG_MONGODB_NAME"]
        
        else:
            connection_string = None
            self.database = None

        #print("{} -- {}".format(connection_string, database_name))

        if (connection_string is not None) & (self.database is not None):
            try:
                self.connect = pymongo.MongoClient(connection_string, serverSelectionTimeoutMS=3)
                # test mongodb connection using list database
                db_list = self.connect.list_database_names()        

            except :
                self.connect = None
                self.daabase = None
                            
        else:
            self.connect = None
            self.database = None
  
    def __repr__(self):
        return f"MongoDB connection '{self.connect}' --> '{self.database}' database"

    def __del__(self):
        self.connect.close

    def insert_one(self, collection: str, data=None):
        '''
        insert data in the specific collection
        :param collection: The collection to do this action
        :param data: The data to insert
        example : db.insert_one("users", {"key":"value"}])
        '''
        db_name = self.connect[self.database]
        collection = db_name[collection]
        collection.insert_one(data)

    def insert_many(self, collection: str, data=None):
        db_name = self.connect[self.database]
        collection = db_name[collection]
        collection.insert_many(data)

    def delete(self, collection: str, condition=None) -> int:
        '''
        Delete data in the specific collection
        :param collection: The collection to do this action
        :param condition: The condition to do the delete operation -> list
        :return: The count of successful delete, ignore not found, or -1 if error
        example : db.delete("users", [{"userEmail":"nonowner@test.com"}])
        '''
        db_name = self.connect[self.database]
        collection = db_name[collection]
        if not condition:
            # print("ERROR : Delete criteria must be not none!")
            return -1
        count = 0
        for f in condition:
            res = collection.delete_one(f)
            # if not res or not res.deleted_count:
            #     print(f"INFO : Cannot find the matched row to delete for the criteria: {f} !")
            count += res.deleted_count
        return count

    def drop(self, collection:str):
        db_name = self.connect[self.database]
        collection = db_name[collection]
        collection.drop()

    def update_manay(self, collection: str, mod_dict=None) -> int:
        '''
        Update the data in the specific collection
        :param collection: The collection do do this action
        :param mod_dict: The condition to update collection,
            e.g. {"{'d':4}":{"$set": {'e': 6}}}, key is the condition, value is the new value
        :return: The count of successful update, or -1 if error
        example :  db.update("users", {"{'userEmail':'owner@test.com'}":{"$set": {'isAdmin':False}}})
        '''
        db_name = self.connect[self.database]
        collection = db_name[collection]
        if not mod_dict:
            print("ERROR : Update criteria must be not none!")
            return -1
        count = 0
        for k, v in mod_dict.items():
            criteria = eval(k)
            res = collection.update_one(criteria, v)
            # if not res or not res.matched_count:
            #     Print(f"ERROR : Cannot find the matched row to update for the criteria: {criteria} \n{v}!")
            count += res.modified_count
        return count
        
    def update_one(self, collection: str, condition =None, new_value =None) -> int:
        '''
        Update the data in the specific collection
        :param collection: The collection do do this action
        :param query: The condition to update collection,
        :param value: The value to update
        :return: The count of successful update, or -1 if error
        example :  db.update_one("users", {"userEmail":"owner@test.com"}, {'isAdmin':False})
        '''
        db_name = self.connect[self.database]
        collection = db_name[collection]

        if (condition is not None) & (new_value is not None):
            new_value = { "$set" : new_value }
            res = collection.update_one(condition, new_value)
            return res.matched_count 
        else:
            # print("ERROR : Update criteria and new value must be provided!")
            return -1

    def query_count(self, collection: str, condition=None) -> int:
        '''
        Check the records count according to specific condition
        :param collection: The collection do do this action
        :param condition: The condition to check
        :return: The count of the checking result, or -1 if error
        example : db.query_count("orders", {"orderEmail":"test@test.com"})
        '''
        db_name = self.connect[self.database]
        try:
            collection = db_name[collection]
            num = len(list(collection.find(condition)))
            return num
        except :
            return -1

    def query(self, collection: str, condition=None, want_fields=None) -> list:
        '''
        Select Data in the specific collection
        :param collection: The collection do do this action
        :param condition: The condition to do the select action  -> list
        :param want_fields: The condition to filter the record with the field you want -> dict, e.g. {'a': 1}
        :return: The list contains the dicts of every account record
        example : db.query("users"), return all rows and data in collection
        example : db.query("users", {"userEmail":"owner@test.com"}), return row matched the condition
        example : db.query("users", {"userEmail":"owner@test.com"}, {"isAdmin", "isOwner"}), return required fields
        example : db.query("users", {}, {"userEmail"})), return required fields in all rows
        ''' 
        db_name = self.connect[self.database]
        try:
            collection = db_name[collection]
            if not condition or isinstance(condition, dict):
                rows = collection.find(condition, want_fields)
                rows = list(rows) if rows else []
            else:
                rows = []
                for f in condition:
                    row = collection.find_one(f, want_fields)
                    if row:
                        rows.append(row)
            return rows
        except :
            return None
