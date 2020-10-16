from __future__ import print_function
from mysql.connector import errorcode
import mysql.connector
import json
import urllib.request

def validate_string(val) :
    if val is not None :
        if type(val) is int :
            return str(val).encode('utf-8')
        else :
            if val == str("") :
                return None
            else:
                return val.replace("'", "_")


class Database_coordinates:
    def __init__(self) :
        self.user = 'root'
        self.password = 'Arnaud31'
        self.host = '127.0.0.1'
        self.database = 'purbeurre'

    def create_database(self, cursor) :
        try :
            cursor.execute("CREATE DATABASE {} "
                "DEFAULT CHARACTER SET `utf8`".format(self.database))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    def use_database(self, cursor) :
        try :
            cursor.execute("USE {}".format(self.database))
        except mysql.connector.Error as err :
            print("Database {} does not exists.".format(self.database))
            if err.errno == errorcode.ER_BAD_DB_ERROR :
                create_database(cursor)
                print("Database {} created successfully."
                    .format(self.database))
            else:
                print(err)
                exit(1)


class Tables_description :
    def __init__(self) :
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
            "`product_name` VARCHAR(100) NOT NULL,"
            "`brands` VARCHAR(100) NOT NULL,"
            "`nutrition_grade_fr` VARCHAR(100) NOT NULL,"
            "`stores` VARCHAR(100),"
            "`image_url` VARCHAR(100) NOT NULL,"
            "PRIMARY KEY (`id`),"
            "CONSTRAINT `key_category`"
                "FOREIGN KEY (`id_category`)"
                "REFERENCES `purbeurre`.`categories` (`category_id`))" 
            "ENGINE = InnoDB;")

    def creating_tables(self, cursor) :
        for table_name in self.TABLES :
            table_description = self.TABLES[table_name]
            try :
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err :
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR :
                    print("already exists.")
                else :
                    print(err.msg)
            else :
                print("OK")


class Creating_API :
    def __init__(self) :
        self.categories = []
        self.API_dict = {}
        with open("ressources.txt", "r") as ressources :
            for lines in ressources.readlines() :
                for characters in lines :
                    if characters == "\n" :
                        lines = lines.replace('\n', '')
                self.categories.append(lines)
        for cat in self.categories :
            values = f'https://fr.openfoodfacts.org/categorie/{cat}/1.json'
            self.API_dict[cat] = values

class Categories_description :
    def __init__(self, API) :
        self.API = API
        self.check_categories = "SELECT * FROM categories"
        self.check_datas = "SELECT * FROM food_datas"

    def insert_into_categories(self, cursor) :
        exec_check = cursor.execute(self.check_categories)
        cursor.fetchall()
        row = cursor.rowcount
        if row <= 0 :
            for key in self.API :
                exec_cat = ("INSERT INTO categories (category) "
                    f"VALUES ('{key}')")
                cursor.execute(exec_cat)
        else :
            print("already exist")

class Datas_description :
    def __init__(self, API) :
        self.API = API
        self.check_datas = "SELECT * FROM food_datas"
        for key, values in self.API.items() :
            self.req_id_cat = ("SELECT category_id "
                f"FROM categories WHERE category = '{key}' LIMIT 1")
            self.json_obj = [json.loads(
                (urllib.request.urlopen(values)).read())][0]['products']
            for i, item in enumerate(self.json_obj) :
                self.product_name = validate_string(item.get(
                    "product_name", None))
                self.brands = validate_string(item.get(
                    "brands", None))
                self.nutrition_grade_fr = validate_string(item.get(
                    "nutrition_grade_fr", None))
                self.stores = validate_string(item.get(
                    "stores", None))
                self.image_url = validate_string(item.get(
                    "image_url", None))

    def insert_into_food_datas(self, cursor) :
        exec_check = cursor.execute(self.check_datas)
        cursor.fetchall()
        row = cursor.rowcount
        if row <= 0 :
            for key, values in self.API.items() :
                exec_id_cat = cursor.execute(self.req_id_cat)
                id_cat = cursor.fetchone()[0]
                for i, item in enumerate(self.json_obj) :
                    execute = ("INSERT INTO food_datas "
                        "(id_category, "
                        "product_name, "
                        "brands, "
                        "nutrition_grade_fr, "
                        "stores, "
                        "image_url)"
                        f"VALUES ({id_cat}, "
                        f"'{self.product_name}', "
                        f"'{self.brands}', "
                        f"'{self.nutrition_grade_fr}', "
                        f"'{self.stores}', "
                        f"'{self.image_url}')")
                    cursor.execute(execute)
                    print(execute)
        else :
            print("already exist")

