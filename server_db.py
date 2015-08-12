#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
import MySQLdb.cursors
import logging
import logging.config
import chardet
from conf import *

class db(object):
        db_link = None
        cursor = None

        @staticmethod
        def get_db(force=False):
                if db.db_link is None or force:
                        db.db_link = MySQLdb.connect(user=db_user, passwd=db_password, db=db_base, cursorclass=MySQLdb.cursors.DictCursor)
                else:
                        db.db_link.ping()
                return db.db_link

        @staticmethod
        def get_cursor(force=False):
                if db.cursor is None or force:
                        db.cursor = db.get_db(force).cursor()
                        db.cursor.connection.autocommit(True)
                return db.cursor

        @staticmethod
        def query(sql, values=()):
                cursor = db.get_cursor()
                cursor.execute(sql, values)
                return cursor

        @staticmethod
        def query_many(sql, values=()):
                cursor = db.get_cursor()
                cursor.executemany(sql, values)
                return cursor

        @staticmethod
        def select(sql, values=(), **kwargs):
                cursor = db.query(sql, values)
                if kwargs.get('one') is not None:
                        return cursor.fetchone()
                return cursor.fetchall()

        @staticmethod
        def insert(sql, values=()):
            try:
                cursor = db.query(sql, values)
                return cursor.lastrowid
            except Exception as e:
                return False

        @staticmethod
        def insert_many(sql, values=()):
            try:
                cursor = db.query_many(sql, values)
                #return cursor.lastrowid
            except Exception as e:
                print e
                return False


        @staticmethod
        def commit():
                db.db_link.commit()

def reconnect():
        db.get_cursor(True)

def get_regions_for_search(text):
    try:        
        return db.select('select * from regions where NormalizedName like %s limit 0,10', ('%'+text+'%',))
    except Exception as e:
        print e
        return False

def get_type_shorts():
    try:        
        return db.select('select * from socrtypes')
    except Exception as e:
        print e
        return False

def get_records_for_search(text, parent, table):
    try:
	print table, parent, text
        return db.select('select * from '+table+' where NormalizedName like %s and code like %s limit 0,10', ('%'+text+'%', parent+'%',))
    except Exception as e:
        print e
        return False
