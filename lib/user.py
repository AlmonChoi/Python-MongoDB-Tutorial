#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bcrypt
import pymongo
from lib.db import DataSource 

class User:
    '''
    Used for user operation 
    '''
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, userEmail =None):
        '''
        Check if user existed in database. If exist, get user roles
        '''
        self.userEmail = None
        self.usersName = None
        self.isAdmin = None
        self.isOwner = None
        self.logon = False

        if userEmail is not None:
            db = DataSource()
            user_found = db.query_count("users", {"userEmail":userEmail})
            if user_found:
                self.userEmail = userEmail
                res = db.query("users", {"userEmail":userEmail})
                self.usersName = res[0]["usersName"]
                self.isAdmin = res[0]["isAdmin"]
                self.isOwner = res[0]["isOwner"]

    def __repr__(self):
        return f"'{self.userEmail}', '{self.usersName}', {'isAdmin' if self.isAdmin else 'notAdmin'}', {'isOwner' if self.isOwner else 'notOwner'}', '{'Logon' if self.logon else 'Not Logon'}'"

    def change_pwd(self, old_password =None, new_password = None) -> int:
        '''
        change user passowrd
        :param old_password: old password, change if it is matched in database
        :param new_password: new password
        :return: 1 sucess, 0 failed, -1 missing input, -2 old password not match
        example: usr.change_pwd("test", "admin")
        '''
        if (old_password is not None) & (new_password is not None):
            auth = self.auth(old_password)
            if auth:
                bytes = new_password.encode('utf-8') 
                salt = bcrypt.gensalt() 
                hash = bcrypt.hashpw(bytes, salt).decode('ascii')
                print(hash)
                db = DataSource()
                res = db.update_one("users", {"userEmail": self.userEmail }, {"userPassword": hash })
                return res
            else:
                return -2
        else:
            return -1

    def auth(self, password =None) -> int:
        '''
        Check user is existed in users collection
        :param password: The password input by user
        :return: 1 sucess, 0 failed, -1 missing input
        '''
        if password is not None:
            db = DataSource()
            res = db.query("users", {"userEmail" : self.userEmail}, {"userPassword"})
            hash_pwd = res[0]["userPassword"].encode('ascii')

            password = password.encode('utf-8') 
            res = bcrypt.checkpw(password, hash_pwd)
            
            if res:
                self.logon = True
                return 1
            else:
                return 0
        else:
            return -1