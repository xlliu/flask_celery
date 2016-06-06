# -*- coding: utf-8 -*-
import pymongo


class mongodb_conn():
    conn = None

    def __init__(self, host, port, collection, flag=0):
        self.db_host = host
        self.db_port = port
        self.db_collection = collection
        self.db_flag = flag
        self.set_conn()

    def get_db(self):
        db = self.get_conn()
        collection = db[self.db_collection]
        if self.db_flag:
            a = collection.authenticate("surpro", "Gmtinter89")
        return collection

    def set_conn(self):
        self.conn = pymongo.MongoClient(self.db_host, self.db_port,)

    def get_conn(self):
        return self.conn
