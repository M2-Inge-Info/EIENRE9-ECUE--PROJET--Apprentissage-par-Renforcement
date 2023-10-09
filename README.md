# EIENRE9-ECUE-Apprentissage-par-Renforcement
Mastering the Game of Go

# Projet d'Apprentissage par Renforcement avec Atari

## Introduction
Ce projet doit être commencé pendant la première moitié de la session.

## Étape 1: Sélection d'un jeu Atari
Choisissez un jeu Atari à partir de cette liste de jeux Atari. Vous pouvez utiliser deux types d'observations différents:

- **IMAGE**: L'observation est une image RGB de l'écran, qui est un tableau de forme (210, 160, 3).
- **RAM**: L'observation est la RAM de la machine Atari, composée de 128 octets.

## Étape 2: Sélection d'un sujet
Vous pouvez choisir l'une des méthodes discutées en classe (Qlearning / Approximation de la fonction de valeur / Gradient de politique), et un sujet d'étude, tel que:

- Comparaison des stratégies pour epsilon (constant, diminution linéaire, autre fonction décroissante).
- Comparaison des valeurs pour gamma (plusieurs valeurs entre 0 et 1).
- Comparaison des valeurs pour alpha (choisir plusieurs valeurs).
- Comparaison des topologies pour le ANN (nombre de couches, nombre de neurones, dense ou convolutionnel).
- Comparaison des stratégies pour les récompenses.
- Autre sujet libre (à valider avec un instructeur).

## Étape 3: Exécution
- **v0**: Code qui vous permet de jouer et de voir les récompenses pendant le jeu (affichage sur stdout).
- **Première exécution**: Imprimez les scores pour chaque jeu. La courbe pourrait être très bruyante. Utilisez donc une moyenne mobile des récompenses cumulatives (faites attention à la taille de la moyenne mobile ou à la méthode utilisée pour calculer la moyenne).
- En fonction de votre choix de sujet, variez certains paramètres et imprimez les résultats comme pour la première exécution, puis comparez.

**Note**: Vous pouvez utiliser n'importe quel morceau de code que vous pouvez trouver sur Internet, mais il est obligatoire de citer toutes les sources dans votre rapport.

## Étape 5 (Optionnelle): Soumission de votre travail
Le travail peut être effectué en groupes de 2. Si vous le souhaitez, vous pouvez soumettre un fichier zip contenant ipynb (ou code py + rapport synthétique pdf). Si vous soumettez un ipynb, ASSUREZ-VOUS QUE TOUTES LES CELLULES SONT DÉJÀ EXÉCUTÉES. Le texte peut être rédigé en français ou en anglais en utilisant les outils disponibles pour les corrections orthographiques et grammaticales (Grammalecte, ...). Une soumission par groupe.
