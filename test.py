#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from urllib.parse import uses_relative
from lib.db import DataSource 
from lib.user import User


def show_object():
    db = DataSource()
    print(db)

    usr = User("user1@test.com")
    print(usr)
    usr.auth('test')
    print(usr)
    del usr

    usr = User("user2@test.com")
    print(usr)
    del usr

def test_insert():
    db = DataSource()

    if db.connect is None:
        print("ERROR : Unable to connect, please check connection string or database service") 
        os._exit(1)
    else:
        data = {"usersName": "User3",
            "userEmail": "user3@test.com",
            "userPassword": "$2a$10$7jQx/hQOWrRni531b/dHRuH8o1ZP8Yo8g..GpTOF4M7RrEH/pzTMy",
            "isAdmin": False,
            "isOwner": False }

        db.insert_one("users", data )

def test_delete():
    db = DataSource()

    if db.connect is None:
        print("ERROR : Unable to connect, please check connection string or database service") 
        os._exit(1)
    else:
        res = db.delete("users", [{"userEmail":"user3@test.com"}])
        print(res)

def test_query():
    db = DataSource()

    if db.connect is None:
        print("ERROR : Unable to connect, please check connection string or database service") 
        os._exit(1)
    else:
        res = db.query("users", [{"userEmail":"user1@test.com"}])
        print(res)
        res = db.query_count("users", {"userEmail":"user1@test.com"})
        print(res)

def test_updatey():
    db = DataSource()

    if db.connect is None:
        print("ERROR : Unable to connect, please check connection string or database service") 
        os._exit(1)
    else:
        res = db.update_one("users", {"userEmail":"user1@test.com"}, {'isAdmin':False})
        print(res)
        condition =  {"userEmail":"user1@test.com"}
        new_value = {'isAdmin': False, 'isOwner': False}
        res = db.update_one("users", condition, new_value)
        print(res)

def test_user():
    usr = User()
    print("Email {}, Name '{}', isAdmin : {}, isOnwe : {}".format(usr.userEmail, usr.usersName, usr.isAdmin, usr.isOwner))
    
    usr = User("user1@test.com")
    print("Email {}, Name '{}', isAdmin : {}, isOnwe : {}".format(usr.userEmail, usr.usersName, usr.isAdmin, usr.isOwner))


def test_auth():
    usr = User("user1@test.com")
    print(usr.auth())
    print(usr.auth("admin"))
    print(usr.auth("test"))


def test_chg_pwd():
    usr = User("user1@test.com")
    password = "test"
    new_pass = "test"
    print(usr.change_pwd(password, new_pass))

if __name__ == '__main__':
    show_object()
    test_insert()
    test_delete()
    test_query()
    test_updatey()
    test_user()
    test_auth()
    test_chg_pwd()
    print('INFO : End of test')
