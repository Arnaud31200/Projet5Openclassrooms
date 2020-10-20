from datas_mysql import Database_coordinates
from datas_mysql import Tables_description
from datas_mysql import Categories_description
from datas_mysql import Datas_description
from datas_mysql import Create_API
from program_mysql import Program_execute
from mysql.connector import (connection)
from random import choice

def main():
    """Enable main function"""
    if __name__ == "__main__" :
        print("Script directly executed")

        coordinates = Database_coordinates()
        table = Tables_description()
        ressources = Create_API()
        categories = Categories_description(ressources.API_dict)
        datas = Datas_description(ressources.API_dict, categories.categories_list)

        cnx = connection.MySQLConnection(user = coordinates.user,
            password = coordinates.password,
            host = coordinates.host,
            database = coordinates.database)

        cursor = cnx.cursor(buffered=True)

        coordinates.use_database(cursor)
        table.create_tables(cursor)
        cnx.commit()

        categories.insert_into_categories(cursor)
        datas.insert_into_food_datas(cursor)
        cnx.commit()

        program = Program_execute(cursor)
        program.select_categories()
        good_answer = [f"{choice(program.categories_list)}"]
        user_input = ""

        while user_input not in good_answer :
            answer1 = str(input("Choisissez une catégorie : "))
            if answer1 in program.categories_list :
                program.generate_foods_list(answer1)
                break
            elif answer1 not in program.categories_list :
                print("Catégorie inexistante ! Réessayez !")

        good_answer = [f'{choice(program.foods_list)}']
        while user_input not in good_answer :
            answer2 = str(input("Choisissez un aliment : "))
            if answer2 in program.foods_list :
                program.select_food(answer2)
                break
            elif answer2 not in program.foods_list :
                print("Aliment inexistant ! Réessayez !")

        good_answer = ["Oui", "Non"]
        while user_input not in good_answer :
            answer3 = str(input("Voulez-vous rechercher un aliment plus équilibré ? Oui/Non "))
            if answer3 == "Oui" :
                program.searching_better_food(answer1)
                break
            elif answer3 == "Non" :
                print("Recherche terminée")
                break
            else :
                print("Réponse incorrecte ! Réessayez !")

        while user_input not in good_answer and answer3 != "Non" :
            answer4 = str(input("Voulez-vous stocker l'aliment sélectionné ? Oui/Non "))
            if answer4 == "Oui" :
                program.id_food_storage(answer2)
                break
            elif answer4 == "Non" :
                print("Recherche terminée")
                break
            else :
                print("Réponse incorrecte ! Réessayez !")

        cnx.commit()
        cursor.close()
        cnx.close()

    else :
        print("Script imported")


main()
