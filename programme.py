from __future__ import print_function
from mysql.connector import (connection)
from mysql.connector import errorcode
import mysql.connector
import json
import urllib.request

cnx = connection.MySQLConnection(user='root', password='Arnaud31',
                                 host='127.0.0.1',
                                 database='purbeurre')

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
    "`id` INT NOT NULL AUTO_INCREMENT,"
    "`product_name` VARCHAR(70) NOT NULL,"
    "`brands` VARCHAR(70) NOT NULL,"
    "`nutrition_grade_fr` VARCHAR(70) NOT NULL,"
    "`stores` VARCHAR(70),"
    "`image_url` VARCHAR(100) NOT NULL,"
    "PRIMARY KEY (`id`),"
    "UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,"
    "INDEX `nutrition_grade_fr` (`nutrition_grade_fr` ASC) VISIBLE"
    ") ENGINE = InnoDB;")

TABLES['categories'] = (
  "CREATE TABLE IF NOT EXISTS `categories` ("
  "`category_id` INT NOT NULL AUTO_INCREMENT,"
  "`category` VARCHAR(100) NOT NULL,"
  "PRIMARY KEY (`category_id`),"
  "UNIQUE INDEX `category` (`category_id` ASC) VISIBLE"
  ") ENGINE = InnoDB;")

cnx = mysql.connector.connect(user='root', password='Arnaud31',
                                 host='127.0.0.1',
                                 database='purbeurre')
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET `utf8`".format(purbeurre))
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

def validate_string(val):
   if val != None:
        if type(val) is int:
            #for x in val:
            #   print(x)
            return str(val).encode('utf-8')
        else:
            if val == str(""):
                return None
            else:
                return val.replace("'","_")

categories = {"pates-a-tartiner" : 'https://fr.openfoodfacts.org/categorie/pates-a-tartiner/1.json', "popcorn" : 'https://fr.openfoodfacts.org/categorie/popcorn/1.json', "brioches" : 'https://fr.openfoodfacts.org/categorie/brioches/1.json'}

for key in categories.keys() :
    execute = f"INSERT INTO categories (category) VALUES ('{key}')"
    cursor.execute(execute)
    print(execute)

cnx.commit()

def find_key(values): 
    for k, val in categories.items(): 
        if val == values:
            return k

for values in categories.values():
    json_obj = [json.loads((urllib.request.urlopen(values)).read())][0]['products']
    for i, item in enumerate(json_obj) :
        f"SELECT categories.category_id, categories.category FROM categories WHERE categories.category = {find_key(values)}"
        product_name = validate_string(item.get("product_name", None))
        brands = validate_string(item.get("brands", None))
        nutrition_grade_fr = validate_string(item.get("nutrition_grade_fr", None))
        stores = validate_string(item.get("stores", None))
        image_url = validate_string(item.get("image_url", None))
        execute = f"INSERT INTO food_datas (product_name, brands, nutrition_grade_fr, stores, image_url) VALUES ('{product_name}', '{brands}', '{nutrition_grade_fr}', '{stores}', '{image_url}')"
        cursor.execute(execute)
        print(execute)

cnx.commit()
cursor.close()
cnx.close()