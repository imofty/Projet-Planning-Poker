# Projet CAPI - Planning Poker

Binôme **B3-5**, membres **A** et **B**.

## Version actuelle - US-04

Le programme fonctionne dans un terminal. Il permet de :

- saisir le nombre de joueurs et leurs pseudos ;
- choisir la règle stricte ou la majorité absolue ;
- charger un backlog JSON ;
- afficher la première fonctionnalité à estimer.

Il faut au moins un joueur. Les pseudos doivent être non vides et différents :
`Alice` et `alice` sont considérés comme le même pseudo.

Pour l'instant, la règle choisie est conservée dans la configuration.
Le vote, le calcul des estimations, l'export et la sauvegarde/reprise restent à développer.

## Lancement

Prérequis : **Python 3.10 ou plus récent**. Aucune dépendance à installer.

```sh
git clone https://github.com/imofty/Projet-Planning-Poker.git
cd Projet-Planning-Poker
python3 -m planning_poker exemples/backlog.json
```

Sous Windows, utilisez `py -3` à la place de `python3` si nécessaire.
Depuis la racine du dépôt, on peut aussi lancer `python3 -m planning_poker`
et saisir le chemin du fichier pendant la configuration.

Exemple de saisies : `2`, `A`, `B`, `1` (une valeur par ligne).
L'application affiche ensuite le projet « Bibliothèque en ligne » et
`F1 : Rechercher un livre par titre`.

Si le fichier est absent, illisible, invalide ou vide, un message explique
l'erreur et un nouveau chemin est demandé. `Ctrl+C` annule la configuration.

## Vérification

Depuis la racine du dépôt :

```sh
python3 -m unittest discover -s tests -v
```

Les tests vérifient la configuration des joueurs et le chargement du JSON.
Ils couvrent notamment les pseudos en double, un fichier absent, un JSON incorrect
et un backlog vide. Les trois critères de R1 concernent les règles de vote :
ils seront implémentés en séance 2.

## Format du backlog

Le fichier doit être un JSON en UTF-8. Exemple :

```json
{
  "projet": "Bibliothèque en ligne",
  "fonctionnalites": [
    { "id": "F1", "titre": "Rechercher un livre par titre" },
    { "id": "F2", "titre": "Emprunter un livre disponible" }
  ]
}
```

- La racine est un objet avec `projet`, texte non vide, et `fonctionnalites`,
  liste non vide.
- Chaque fonctionnalité possède un `id` et un `titre`, tous deux des textes
  non vides. Les identifiants sont uniques après retrait des espaces de bord.
- L'ordre du fichier détermine l'ordre des fonctionnalités à estimer.
- Les champs supplémentaires sont ignorés lors du chargement.
- Un marqueur BOM en début de fichier est accepté.
- Ce format décrit un backlog initial ; il ne constitue pas encore un format
  de sauvegarde ou d'export de partie.

Un exemple complet est disponible dans `exemples/backlog.json`.

## Repères dans le code

```text
planning_poker/
  __main__.py    point d'entrée
  console.py     saisies et affichages
  partie.py      données de configuration, backlog et partie
  backlog.py     lecture et validation du JSON
tests/          vérifications d'US-04
exemples/       backlog JSON
rendus/         documents R0 et R1
```

Les saisies et les affichages sont dans `console.py`. Les autres modules peuvent
être utilisés sans lancer le terminal, notamment dans les tests.

Le déroulement du programme et les notions utiles sont expliqués dans
[`docs/prise-en-main.md`](docs/prise-en-main.md).
