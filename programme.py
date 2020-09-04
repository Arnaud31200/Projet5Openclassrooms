from datas_mysql import database_coordinates
from datas_mysql import tables_description
from datas_mysql import datas_description
from mysql.connector import (connection)

coordinates = database_coordinates()
table = tables_description()
datas = datas_description()

cnx = connection.MySQLConnection(user = coordinates.user, password = coordinates.password, host = coordinates.host, database = coordinates.database)
cursor = cnx.cursor()

coordinates.use_database(cursor)
table.creating_tables(cursor)

cnx.commit()

datas.insert_into_categories(cursor)
datas.insert_into_food_datas(cursor)

cnx.commit()
cursor.close()
cnx.close()