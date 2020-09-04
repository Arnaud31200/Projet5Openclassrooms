
from __future__ import print_function
from mysql.connector import (connection)
from mysql.connector import errorcode
import mysql.connector

cnx = connection.MySQLConnection(user='root', password='Arnaud31',
                                 host='127.0.0.1',
                                 database='purbeurre')

class connection:
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
    
    def connect(self):
        cnx = connection.MySQLConnection(user = self.user, password = self.password, host = self.host, database = self.database)