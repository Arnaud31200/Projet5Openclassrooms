from datas_mysql import database_coordinates
from datas_mysql import tables_description
from datas_mysql import datas_description
from mysql.connector import (connection)
from random import choice

coordinates = database_coordinates()
table = tables_description()
datas = datas_description()

cnx = connection.MySQLConnection(user = coordinates.user, password = coordinates.password, host = coordinates.host, database = coordinates.database)
cursor = cnx.cursor(buffered=True)

coordinates.use_database(cursor)
table.creating_tables(cursor)

cnx.commit()

datas.insert_into_categories(cursor)
datas.insert_into_food_datas(cursor)

execute = f"SELECT category FROM categories"
cursor.execute(execute)
categories = cursor.fetchall()
categories_list = []
for tuples in categories: 
    for i in tuples:
        categories_list.append(i)
print(categories_list)

ANSWER1 = str(input("Choisissez une catégorie : "))
while ANSWER1 != [f'{choice(categories_list)}'] :
    if ANSWER1 in categories_list :
        execute = f"SELECT category FROM categories WHERE category = '{ANSWER1}'"
        cursor.execute(execute)
        execute = f"SELECT product_name FROM purbeurre.food_datas INNER JOIN purbeurre.categories ON id_category = category_id WHERE category = '{ANSWER1}'"
        cursor.execute(execute)
        foods = cursor.fetchall()
        foods_list = []
        for tuples in foods: 
            for i in tuples:
                foods_list.append(i)
        print(foods_list)

        ANSWER2 = str(input("Choisissez un aliment : "))
        while ANSWER2 != [f'{choice(foods_list)}'] :
            if ANSWER2 in foods_list :
                execute = f"SELECT product_name, nutrition_grade_fr FROM purbeurre.food_datas WHERE product_name='{ANSWER2}'"
                cursor.execute(execute)
                food_selected = cursor.fetchone()
                print("nom : ", food_selected[0], ", nutriscore : ", food_selected[1])

                ANSWER3 = str(input("Rechercher un aliment plus équilibré ?"))
                while ANSWER3 != ["Oui","Non"] :
                    if ANSWER3 == "Oui":
                        execute = f"SELECT product_name, nutrition_grade_fr FROM purbeurre.food_datas  WHERE id_category = (SELECT category_id FROM purbeurre.categories WHERE category = '{ANSWER1}') AND nutrition_grade_fr = (SELECT MIN(nutrition_grade_fr) FROM purbeurre.food_datas)"
                        cursor.execute(execute)
                        food_selected = cursor.fetchone()
                        print("Nous avons trouvé : ", food_selected) 
                        ANSWER4 = str(input("Stocker l'aliment sélectionné ? "))
    
                        while ANSWER4 != ["Oui","Non"] :
                            if ANSWER4 == "Oui":
                                food_substituted = []
                                food_substituted.append(food_selected[0])
                                execute_start_food = f"SELECT id FROM purbeurre.food_datas WHERE product_name='{ANSWER2}'"
                                cursor.execute(execute_start_food)
                                id_start_food = cursor.fetchone()
                                execute_substitute_food = f"SELECT id FROM purbeurre.food_datas WHERE product_name='{food_selected[0]}'"
                                cursor.execute(execute_substitute_food)
                                id_substitute_food = cursor.fetchone()
                                execute_insertion_storage = f"INSERT INTO purbeurre.storage (start_food, substitute_food) VALUES ('{id_start_food[0]}', '{id_substitute_food[0]}')"
                                cursor.execute(execute_insertion_storage)
                                print(execute_insertion_storage)
                                print("Aliments ajoutés avec succés !")
                                print("Liste des aliments substitués : ", food_substituted)
                                cnx.commit()
                                cursor.close()
                                cnx.close()
                                break

                            elif ANSWER4 == "Non":
                                print("Recherche terminée")
                                cnx.commit()
                                cursor.close()
                                cnx.close()
                                break
                            
                            else:
                                print("Réponse incorrecte ! Réessayez !")
                            ANSWER4 = str(input("Stocker l'aliment sélectionné ? "))

                    elif ANSWER3 == "Non":
                        print("Recherche terminée")
                        break
                        cnx.commit()
                        cursor.close()
                        cnx.close()

                    else : 
                        print("Réponse incorrecte ! Réessayez !")
                    ANSWER3 = str(input("Rechercher un aliment plus équilibré ?"))
            else : 
                print("Aliment inexistant ! Réessayez !")
            ANSWER2 = str(input("Choisissez un aliment : "))
    else :
        print("catégorie inexistante ! Réessayez !")
    ANSWER1 = str(input("Choisissez une catégorie : "))