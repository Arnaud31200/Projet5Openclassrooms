categories = ["pates-a-tartiner", "popcorn", "brioches", "pains", "viandes", "boissons"]
API_dict = {}

for cat in categories:
    values = f'https://fr.openfoodfacts.org/categorie/{cat}/1.json'
    API_dict[cat] = values
    
print(API_dict)