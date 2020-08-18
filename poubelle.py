    "CONSTRAINT `key_start` FOREIGN KEY (`id`)"
        "REFERENCES `purbeurre`.`storage` (`start_food`),"
    "CONSTRAINT `key_substitute`FOREIGN KEY (`id`)"
        "REFERENCES `purbeurre`.`storage` (`substitute_food`)"

        , 'https://fr.openfoodfacts.org/categorie/popcorn/1.json'

        , "popcorn"

        url = urllib.request.urlopen(url_list[categories.index(name)])