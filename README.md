# Projet  : Utilisation les bases de python pour l'analyse de marché

# Objectif :
Ce programme est un système de surveillance des prix des livres du site web "_Books to Scrape_". Il est conçu pour récupérer toutes les données essentielles de chaque livre, telles que les _prix_, les _titres_, les _catégories_, etc. En suivant le processus classique du pipeline **ETL** (_Extract, Transform et Load_), ce programme assure une extraction efficace des données, leur transformation pour garantir leur qualité et leur cohérence, puis leur chargement dans un format exploitable.


# Fonctionnalités :
**Extract :** Le programme extrait les informations de chaque livre du site Books To Scrap.

**Transform :** Les données extraites sont transformées pour garantir une structure uniforme (nettoyage de texte)

**Load :** Création d'un dossier local "_all_book_categories_" avec une séparation logique des données. Enregistrement des informations de chaque livre dans un fichier _CSV_ dédié à la catégorie.


# Installation :
1. Ouvrez le terminal ou l'invite de commandes selon votre _OS_.

2. Clonez le répertoire avec la commande : `git clone https://github.com/MouloudB-24/p2_UtilisezLesBasesDePythonPourAnalyseDeMarche`

3. Accédez au répertoire avec la commande : `cd p2_UtilisezLesBasesDePythonPourAnalyseDeMarche`

4. Créer un environement virtuel avec cette commande : `python3 -m venv env`
`
5. Activez l'environnement virtuel avec cette commande : `source env/bin/activate`

5. Installez les dépendances avec la commande : `pip install -r requirements.txt`
    
5. Lancez le programme avec la commande : `python3 main.py`

6. Une fois la console lancée, elle vous invite à faire un choix : soit scraper tout le site (_option 1_), soit une 
   catégorie de livre (_option 2_). Dans la dernière option, le programme vous invite à 
   entrer l'**URL** de produit qui vous intéresse.

**Nota : Assurez-vous d'avoir un environnement Python configuré.**

L'interface de lancement  de programme :

 """   _Welcome to the Books to scrapes price monitoring program, please select one of the following options:
        1 → Scraper data from all books
        2 → Scraper data from books in a category
        3 → Quit program_
          
_Enter your choice 👉: 1, 2, OU 3_
"""
