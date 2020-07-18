Objectif : Créer un programme qui interagirait avec la base Open Food Facts pour en récupérer les aliments, les comparer et proposer à l'utilisateur un substitut plus sain à l'aliment qui lui fait envie.

Description du parcours utilisateur
1 - Quel aliment souhaitez-vous remplacer ? 
2 - Retrouver mes aliments substitués.
Sélectionnez la catégorie. [Plusieurs propositions associées à un chiffre. L'utilisateur entre le chiffre correspondant et appuie sur entrée]
Sélectionnez l'aliment. [Plusieurs propositions associées à un chiffre. L'utilisateur entre le chiffre correspondant à l'aliment choisi et appuie sur entrée]
Le programme propose un substitut, sa description, un magasin ou l'acheter (le cas échéant) et un lien vers la page d'Open Food Facts concernant cet aliment.
L'utilisateur a alors la possibilité d'enregistrer le résultat dans la base de données.

Fonctionnalités :
Recherche d'aliments dans la base Open Food Facts.
L'utilisateur interagit avec le programme dans le terminal, mais si vous souhaitez développer une interface graphique vous pouvez,
Si l'utilisateur entre un caractère qui n'est pas un chiffre, le programme doit lui répéter la question,
La recherche doit s'effectuer sur une base MySql.

Que souhaitez-vous que votre programme fasse ?
- Le programme doit comporter une base de données en relation avec l'API OpenFoodFacts.
- Le programme doit ensuite sélectionner l'aliment à remplacer.
- Le programme doit enfin proposer des subsituts à cet aliment :
  - Les Données de l'aliment.
    - Le lien OpenFoodFacts.
- Le programme doit enregistrer le résultat dans la base de données.

Comment le développeur comprendra le code ?
- Une partie base de données MySQL :
    - Base de données.
    - Relation avec l'API qui importera les élements nécessaires en JSON.
- Une partie programme en Python :
    - Le programme Sélectionnera l'aliment choisi dans la base de données.
    - Le programme proposera un subsistut.
    - Le programme enregistrera le résultat sur la base de données