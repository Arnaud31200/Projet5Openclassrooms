from __future__ import print_function
from mysql.connector import errorcode
import mysql.connector
import json
import urllib.request


class database_coordinates:
    def __init__(self):
        self.user = 'root'
        self.password = 'Arnaud31'
        self.host = '127.0.0.1'
        self.database = 'purbeurre'

    def create_database(self, cursor):
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET `utf8`"
                .format(self.database))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    def use_database(self, cursor):
        try:
            cursor.execute("USE {}".format(self.database))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(self.database))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(cursor)
                print("Database {} created successfully."
                .format(self.database))
                cnx.database = self.database
            else:
                print(err)
                exit(1)


class tables_description:
    def __init__(self):
        self.TABLES = {}
        self.TABLES['storage'] = (
            "CREATE TABLE IF NOT EXISTS `storage` ("
            "`start_food` INT NOT NULL,"
            "`substitute_food` INT NOT NULL,"
            "INDEX `id_start` (`start_food` ASC) VISIBLE,"
            "INDEX `id_substitute` (`substitute_food` ASC) VISIBLE"
            ") ENGINE = InnoDB;")
        self.TABLES['categories'] = (
            "CREATE TABLE IF NOT EXISTS `categories` ("
            "`category_id` INT NOT NULL AUTO_INCREMENT,"
            "`category` VARCHAR(100) NOT NULL,"
            "PRIMARY KEY (`category_id`),"
            "UNIQUE INDEX `category` (`category_id` ASC) VISIBLE"
            ") ENGINE = InnoDB;")
        self.TABLES['food_datas'] = (
            "CREATE TABLE IF NOT EXISTS `food_datas` ("
            "`id` INT NOT NULL AUTO_INCREMENT,"
            "`id_category` INT NOT NULL,"
            "`product_name` VARCHAR(70) NOT NULL,"
            "`brands` VARCHAR(70) NOT NULL,"
            "`nutrition_grade_fr` VARCHAR(70) NOT NULL,"
            "`stores` VARCHAR(70),"
            "`image_url` VARCHAR(100) NOT NULL,"
            "PRIMARY KEY (`id`),"
            "CONSTRAINT `key_category`"
                "FOREIGN KEY (`id_category`)"
                "REFERENCES `purbeurre`.`categories` (`category_id`))" 
            "ENGINE = InnoDB;")

    def creating_tables(self, cursor):
        for table_name in self.TABLES:
            table_description = self.TABLES[table_name]
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

class categories_description:
    def __init__(self):
        self.categories = ["pates-a-tartiner", "popcorn", "brioches"]
        self.check_categories = "SELECT * FROM categories"
        self.check_datas = "SELECT * FROM food_datas"

    def validate_string(self, val):
        if val != None:
                if type(val) is int:
                    return str(val).encode('utf-8')
                else:
                    if val == str(""):
                        return None
                    else:
                        return val.replace("'","_")
 
    def insert_into_categories(self, cursor):
        exec_check = cursor.execute(self.check_categories)
        cursor.fetchall()
        row = cursor.rowcount
        if row <= 0:
            for categories in self.categories :
                exec_cat = f"INSERT INTO categories (category) VALUES ('{categories}')"
                cursor.execute(exec_cat)
        else :
            print("already exist")

class API:
    def __init__(self):
        self.categories_description = categories_description()
        self.API = {self.categories_description.categories[0] : 'https://fr.openfoodfacts.org/categorie/pates-a-tartiner/1.json', self.categories_description.categories[1] : 'https://fr.openfoodfacts.org/categorie/popcorn/1.json', self.categories_description.categories[2]: 'https://fr.openfoodfacts.org/categorie/brioches/1.json'}
        self.urllib = urllib.request.urlopen(self.API.values)
        self.json_obj = [json.loads((self.urllib).read())][0]['products']

class datas_description:
    def __init__(self, product_name, brands, nutrition_grade_fr, stores, image_url):
        self.product_name = categories_description.validate_string(API.json_obj.item.get(product_name, None))
        self.brands = categories_description.validate_string(API.json_obj.item.get(brands, None))
        self.nutrition_grade_fr = nutrition_grade_fr = categories_description.validate_string(API.json_obj.item.get(nutrition_grade_fr, None))
        self.stores = categories_description.validate_string(API.json_obj.item.get(stores, None))
        self.image_url = categories_description.validate_string(API.json_obj.item.get(image_url, None))
        self.check_datas = "SELECT * FROM food_datas"
    
    def insert_into_food_datas(self, cursor):
        exec_check = cursor.execute(self.check_datas)
        cursor.fetchall()
        row = cursor.rowcount
        if row <= 0:
            for key, values in API.API.items():
                    req_id_cat = (f"SELECT category_id FROM categories WHERE category = '{key}' LIMIT 1")
                    exec_id_cat = cursor.execute(req_id_cat)
                    id_cat = cursor.fetchone()[0]
                    for i, item in enumerate(API.json_obj) :
                        execute = f"INSERT INTO food_datas (id_category, product_name, brands, nutrition_grade_fr, stores, image_url) VALUES ({id_cat}, '{self.product_name}', '{self.brands}', '{self.nutrition_grade_fr}', '{self.stores}', '{self.image_url}')"
                        cursor.execute(execute)
                        print(execute)
        else :
            print("already exist")