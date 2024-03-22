# Nom du Projet  : BookScrapePriceWatcher

# Objectif :
L'objectif principal de "BookScrapePriceWatcher" est de simplifier le processus de surveillance des prix des livres 
d'occasion sur les sites web de concurrents, en automatisant la collecte d'informations tarifaires.

# Fonctionnalités :
## Extract 
 - Le programme extrait les informations de chaque livre du site Books To Scrap.

## Transform
 - Les données extraites sont transformées pour garantir une structure uniforme (nettoyage de texte)

## Load
 - Création d'un dossier local "all_book_categories" avec une séparation logique des données.
 - Enregistrement des informations de chaque livre dans un fichier CSV dédié à la catégorie.


# Installation :
1. Ouvrez le terminal ou l'invite de commandes selon l'OS.
2. Clonez le répertoire avec la commande :
    git clone https://github.com/MouloudB-24/p2_UtilisezLesBasesDePythonPourAnalyseDeMarche
3. Accédez au répertoire avec la commande :
    cd p2_UtilisezLesBasesDePythonPourAnalyseDeMarche
4. Assurez-vous d'avoir un environnement Python configuré
5. Installez les dépendances avec la commande :
    pip install -r requirements.txt 
6. Lancez le programme avec la commande :
    python3 main.py
7. Une fois la console lancée, elle vous invite à faire un choix : soit scraper tout le site (option 1), soit une 
   catégorie de livre (option 2), soit un seul livre. Dans les deux dernières options, le programme vous invite à 
   entrer les URL des produits qui vous intéressent.


L'interface de Lancement  de programme :

 """   Welcome to the Books to scrapes price monitoring program, please select one of the following options:
        1 → Scraper data from all books
        2 → Scraper data from books in a category
        3 → Scraper data from a single book
        4 → Quit program
          
Enter your choice 👉: 1, 2, 3 OU 4
"""
