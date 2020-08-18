from __future__ import print_function
from mysql.connector import (connection)
from mysql.connector import errorcode
import mysql.connector
import json
import urllib.request

url = urllib.request.urlopen('https://fr.openfoodfacts.org/categorie/pates-a-tartiner/1.json')
json_data= url.read()
json_obj = [json.loads(json_data)[0]['products']]
products = json_obj[0]['products']
print(products)