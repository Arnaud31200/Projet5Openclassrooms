class Program_execute :
    """Set program execution"""
    def __init__(self, cursor) :
        self.cursor = cursor
        self.categories_list = []
        self.foods_list = []
        self.food_selected = []
        self.food_substituted = []

    def select_categories(self):
        """Set categories selection"""
        execute = ("SELECT product_name, nutrition_grade_fr "
            "FROM purbeurre.food_datas WHERE id "
            "IN (SELECT substitute_food FROM purbeurre.storage)")
        self.cursor.execute(execute)
        food_already_substituted = self.cursor.fetchall()
        print("Liste des aliments déjà substitués :"
            , food_already_substituted)
        execute = "SELECT category FROM categories"
        self.cursor.execute(execute)
        categories = self.cursor.fetchall()
        for tuples in categories :
            for i in tuples :
                self.categories_list.append(i)
        print(self.categories_list)

    def generate_foods_list(self, answer) :
        """Generate foods list""" 
        execute = ("SELECT category FROM categories "
            f"WHERE category = '{answer}'")
        self.cursor.execute(execute)
        execute = ("SELECT product_name "
            "FROM purbeurre.food_datas "
            "WHERE id_category = (SELECT category_id FROM purbeurre.categories "
            f"WHERE category = '{answer}')")
        self.cursor.execute(execute)
        foods = self.cursor.fetchall()
        for tuples in foods : 
            for i in tuples :
                self.foods_list.append(i)
        print(self.foods_list)

    def select_food(self, answer) :
        """Set food selection"""
        execute = ("SELECT product_name, nutrition_grade_fr "
            f"FROM purbeurre.food_datas WHERE product_name='{answer}'")
        self.cursor.execute(execute)
        self.food_selected = self.cursor.fetchone()
        print("nom : ", self.food_selected[0], ", nutriscore : "
            , self.food_selected[1])

    def searching_better_food(self, answer) :
        """Set searching better food"""
        execute = ("SELECT product_name, nutrition_grade_fr "
            "FROM purbeurre.food_datas WHERE id_category = "
            "(SELECT category_id FROM purbeurre.categories "
            f"WHERE category = '{answer}') AND product_name <> 'None' "
            "AND nutrition_grade_fr = (SELECT MIN(nutrition_grade_fr) "
            "FROM purbeurre.food_datas "
            "WHERE id_category = (SELECT category_id "
            "FROM purbeurre.categories "
            f"WHERE category = '{answer}'))")
        self.cursor.execute(execute)
        self.food_selected = self.cursor.fetchone()
        print("Nous avons trouvé : ", self.food_selected)

    def id_food_storage(self, answer) :
        """Set chosen food storage"""
        self.food_substituted.append(self.food_selected[0])
        execute_start_food = ("SELECT id FROM purbeurre.food_datas "
            f"WHERE product_name='{answer}'")
        self.cursor.execute(execute_start_food)
        id_start_food = self.cursor.fetchone()
        execute_substitute_food = ("SELECT id FROM purbeurre.food_datas "
        f"WHERE product_name='{self.food_selected[0]}'")
        self.cursor.execute(execute_substitute_food)
        id_substitute_food = self.cursor.fetchone()
        execute_insertion_storage = ("INSERT INTO purbeurre.storage "
            f"(start_food, substitute_food) VALUES ('{id_start_food[0]}', "
            f"'{id_substitute_food[0]}')")
        self.cursor.execute(execute_insertion_storage)
        print(execute_insertion_storage)
        print("Aliment ajouté avec succés !")
        print("Liste des aliments substitués : ", self.food_substituted)
        print("Recherche terminée")
