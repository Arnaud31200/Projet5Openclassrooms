from __future__ import print_function
from mysql.connector import (connection)
from mysql.connector import errorcode
import mysql.connector


cnx = connection.MySQLConnection(user='root', password='Arnaud31',
                                 host='127.0.0.1',
                                 database='purbeurre')

print(cnx)

DB_NAME = 'purbeurre'

TABLES = {}
TABLES['storage'] = (
    "CREATE TABLE IF NOT EXISTS `storage` ("
    "`start_food` INT NOT NULL,"
    "`substitute_food` INT NOT NULL,"
    "INDEX `id_start` (`start_food` ASC) VISIBLE,"
    "INDEX `id_substitute` (`substitute_food` ASC) VISIBLE"
    ") ENGINE = InnoDB;")

TABLES['food_datas'] = (
    "CREATE TABLE IF NOT EXISTS `food_datas` ("
    "`id` INT NOT NULL,"
    "`name` VARCHAR(45) NOT NULL,"
    "`brand` VARCHAR(45) NOT NULL,"
    "`nutriscore` CHAR(1) NOT NULL,"
    "`store` VARCHAR(45) NOT NULL,"
    "`URL` VARCHAR(45) NOT NULL,"
    "PRIMARY KEY (`id`),"
    "UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,"
    "INDEX `nutriscore` (`nutriscore` ASC) VISIBLE,"
    "CONSTRAINT `key_start` FOREIGN KEY (`id`)"
        "REFERENCES `purbeurre`.`storage` (`start_food`),"
    "CONSTRAINT `key_substitute`FOREIGN KEY (`id`)"
        "REFERENCES `purbeurre`.`storage` (`substitute_food`)"
    ") ENGINE = InnoDB;")

TABLES['categories'] = (
    "CREATE TABLE IF NOT EXISTS `categories` ("
    "`category_id` INT NOT NULL,"
    "`category` VARCHAR(45) NOT NULL,"
    "PRIMARY KEY (`category_id`, `category`),"
    "UNIQUE INDEX `category` (`category` ASC) VISIBLE,"
    "CONSTRAINT `Key_food`"
        "FOREIGN KEY (`category_id`)"
        "REFERENCES `purbeurre`.`food_datas` (`id`)"
    ") ENGINE = InnoDB;")

cnx = mysql.connector.connect(user='root', password='Arnaud31',
                                 host='127.0.0.1',
                                 database='purbeurre')
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(purbeurre))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format('purbeurre'))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format('purbeurre'))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format('purbeurre'))
        cnx.database = 'purbeurre'
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()