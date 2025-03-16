# Guide d'Installation et d'Exécution

## Prérequis
Avant de lancer le projet, assurez-vous d'avoir installé **Python (>=3.8)** et `pip`.

## Installation des Bibliothèques

1. Ouvrez un terminal ou un invite de commande.
2. Installez les dépendances avec `requirements.txt` :
   ```sh
   pip install -r requirements.txt
   ```

## Exécution du Code

Pour exécuter la métaheuristique MAOA sur les données réelles, lancez le fichier **maoa.py** :
```sh
python maoa.py
```

Pour exécuter la métaheuristique NSGA-II sur les données réelles, lancez le fichier **nsga.py** :
```sh
python nsga.py
```

Pour obtenir une comparaison avec NSGA-II sur les données aléatoires, lancez le fichier **compar.py** :
```sh
python compar.py
```

Les détails sur les solutions fournie par la métaheuristique sont disponible dansle fichier **demo.ipynb** :
