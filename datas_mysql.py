"""Import Modules"""
from __future__ import print_function
from mysql.connector import errorcode
import mysql.connector
import json
import urllib.request

def validate_string(val) :
    """ Validate string function"""
    if val is not None :
        if type(val) is int :
            return str(val).encode('utf-8')
        else :
            if val == str("") :
                return None
            else:
                return val.replace("'", "_")


class Database_coordinates :
    """ Set database creation"""
    def __init__(self) :
        self.user = 'root'
        self.password = 'Arnaud31'
        self.host = '127.0.0.1'
        self.database = 'purbeurre'

    def create_database(self, cursor) :
        """ Creating database function"""
        try :
            cursor.execute("CREATE DATABASE {} "
                "DEFAULT CHARACTER SET `utf8`".format(self.database))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    def use_database(self, cursor) :
        """Using database function"""
        try :
            cursor.execute("USE {}".format(self.database))
        except mysql.connector.Error as err :
            print("Database {} does not exists.".format(self.database))
            if err.errno == errorcode.ER_BAD_DB_ERROR :
                self.create_database(cursor)
                print("Database {} created successfully."
                    .format(self.database))
            else:
                print(err)
                exit(1)


class Tables_description :
    """Set tables creation"""
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
            "`category` VARCHAR(50) NOT NULL,"
            "PRIMARY KEY (`category_id`),"
            "UNIQUE INDEX `category` (`category_id` ASC) VISIBLE"
            ") ENGINE = InnoDB;")
        self.TABLES['food_datas'] = (
            "CREATE TABLE IF NOT EXISTS `food_datas` ("
            "`id` INT NOT NULL AUTO_INCREMENT,"
            "`id_category` INT NOT NULL,"
            "`product_name` VARCHAR(100) NOT NULL,"
            "`brands` VARCHAR(100) NOT NULL,"
            "`nutrition_grade_fr` VARCHAR(4) NOT NULL,"
            "`stores` VARCHAR(100),"
            "`image_url` VARCHAR(100) NOT NULL,"
            "PRIMARY KEY (`id`),"
            "CONSTRAINT `key_category`"
                "FOREIGN KEY (`id_category`)"
                "REFERENCES `purbeurre`.`categories` (`category_id`))"
            "ENGINE = InnoDB;")

    def create_tables(self, cursor) :
        """ Creating tables function"""
        for table_name in self.TABLES :
            table_description = self.TABLES[table_name]
            try :
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err :
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR :
                    print("Table already exists.")
                else :
                    print(err.msg)
            else :
                print("OK")

class Create_API :
    """Set API creation"""
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
    """Set categories in database"""
    def __init__(self, API) :
        self.API = API
        self.check_categories = "SELECT category FROM categories"
        self.categories_list = []

    def insertion_funct(self, cursor, key) :
        """Initialize categories insertion"""
        exec_cat = ("INSERT INTO categories (category) "
            f"VALUES ('{key}')")
        cursor.execute(exec_cat)
        print("Category added")


    def insert_into_categories(self, cursor) :
        """Execute categories insertion"""
        cursor.execute(self.check_categories)
        categories_database = cursor.fetchall()
        for tuples in categories_database :
            for i in tuples :
                self.categories_list.append(i)
        row = cursor.rowcount
        if row <= 0 :
            for key in self.API :
                self.insertion_funct(cursor, key)
        elif row > 0 :
            for key in self.API :
                if key not in self.categories_list :
                    self.insertion_funct(cursor, key)
                else :
                    print("Category already exists")

class Datas_description :
    """ Set datas insertion"""
    def __init__(self, API, categories) :
        self.API = API
        self.categories = categories
        self.check_datas = "SELECT * FROM food_datas"

    def insertion_funct(self, cursor, key, values) :
        """Initialize datas insertion"""
        req_id_cat = ("SELECT category_id "
        f"FROM categories WHERE category = '{key}' LIMIT 1")
        cursor.execute(req_id_cat)
        id_cat = cursor.fetchone()[0]
        json_obj = [json.loads(
        (urllib.request.urlopen(values)).read())][0]['products']
        for i, item in enumerate(json_obj) :
            product_name = validate_string(item.get(
                "product_name", None))
            brands = validate_string(item.get(
                "brands", None))
            nutrition_grade_fr = validate_string(item.get(
                "nutrition_grade_fr", None))
            stores = validate_string(item.get(
                "stores", None))
            image_url = validate_string(item.get(
                "image_url", None))
            execute = ("INSERT INTO food_datas "
                "(id_category, "
                "product_name, "
                "brands, "
                "nutrition_grade_fr, "
                "stores, "
                "image_url) "
                f"VALUES ({id_cat}, "
                f"'{product_name}', "
                f"'{brands}', "
                f"'{nutrition_grade_fr}', "
                f"'{stores}', "
                f"'{image_url}')")
            delete_none_entry = ("DELETE FROM food_datas "
            "WHERE product_name = 'None' "
            "OR nutrition_grade_fr = 'None'")
            cursor.execute(execute)
            print(execute)
            cursor.execute(delete_none_entry)
            print(delete_none_entry)
            


    def insert_into_food_datas(self, cursor) :
        """Execute datas insertion"""
        exec_check = cursor.execute(self.check_datas)
        cursor.fetchall()
        row = cursor.rowcount
        if row <= 0 :
            for key, values in self.API.items() :
                self.insertion_funct(cursor, key, values)
        elif row > 0 :
            for key, values in self.API.items() :
                if key not in self.categories :
                    self.insertion_funct(cursor, key, values)
                else :
                    print("Datas already exists")
