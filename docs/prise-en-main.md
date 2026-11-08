# Comprendre la version R1

## Ce qui fonctionne

Cette version prépare une partie locale : elle demande les joueurs, charge un
backlog JSON et présente sa première fonctionnalité. Le vote viendra ensuite.

Le backlog du programme est une liste de fonctionnalités à estimer. Le fichier
`exemples/backlog.json` contient par exemple des besoins d'une bibliothèque.
Les US de R0 décrivent, elles, le développement de l'application de Planning Poker.

## Essayer le programme

Depuis la racine du projet :

```sh
python3 -m planning_poker exemples/backlog.json
```

Saisir une réponse par ligne :

```text
2
A
B
1
```

Cela configure deux joueurs, A et B, avec la règle stricte. Le programme affiche
le projet « Bibliothèque en ligne » et sa première fonctionnalité :
« F1 : Rechercher un livre par titre ».

Pour essayer la gestion des erreurs, relancer le programme avec un fichier absent :

```sh
python3 -m planning_poker exemples/inexistant.json
```

Après la configuration, le programme signale l'erreur et demande un nouveau chemin.
Saisir `exemples/backlog.json` pour poursuivre.

On peut aussi saisir un nombre de joueurs invalide, un pseudo vide ou deux pseudos
identiques. Le programme demande de corriger la saisie.

## Le chemin suivi dans le code

1. `__main__.py` appelle la fonction `main()` de `console.py`.
2. `console.py` récupère le nombre de joueurs, leurs pseudos et la règle.
3. `ConfigurationPartie` vérifie que la configuration est valide.
4. `charger_backlog()` lit le fichier et vérifie les champs du JSON.
5. Une `Partie` regroupe la configuration et le backlog.
6. La console affiche la première fonctionnalité, puis le programme se termine.

La version actuelle ne conserve pas la partie après la fermeture du programme.

## Les constructions Python utilisées

| Construction | Utilité dans ce programme |
|---|---|
| `dataclass` | Déclarer des objets qui regroupent des données, comme une fonctionnalité avec son identifiant et son titre |
| `frozen=True` | Empêcher la modification directe des champs après la création d'un objet |
| `Enum` | Donner un nom aux deux règles autorisées et éviter les chaînes de caractères arbitraires |
| `__post_init__` | Vérifier les données juste après la création d'une configuration |
| `tuple` | Conserver une suite de valeurs qui ne sera pas modifiée sur place |
| `set` | Repérer les pseudos ou les identifiants déjà rencontrés |
| `strip()` | Retirer les espaces au début et à la fin d'un texte |
| `casefold()` | Comparer les pseudos sans tenir compte des majuscules |
| `try` / `except` | Traiter une erreur et afficher un message au lieu d'arrêter brutalement le programme |
| `@property` | Accéder à la première fonctionnalité avec `partie.fonctionnalite_courante` |

Dans `ConfigurationPartie`, `object.__setattr__` sert seulement à retirer les espaces
des pseudos pendant l'initialisation, malgré `frozen=True`. Les champs restent ensuite
protégés contre les affectations directes.

La console contrôle les saisies pour donner un retour immédiat à l'utilisateur.
`ConfigurationPartie` les vérifie aussi pour que ses données restent valides lorsqu'elle
est utilisée directement, par exemple par un test ou une future interface web.

## La vérification du JSON

Le chargeur vérifie successivement :

1. Que le fichier peut être ouvert et lu comme du JSON.
2. Que sa racine est un objet avec un nom de projet non vide.
3. Que `fonctionnalites` est une liste non vide.
4. Que chaque élément contient un identifiant et un titre non vides.
5. Que chaque identifiant n'apparaît qu'une fois.

Les fonctionnalités gardent l'ordre du fichier. La première se trouve donc à
l'indice `0`. Un JSON vide ou incorrect est refusé avant la création de la partie.

## Les trois critères décrits dans R1

Les critères de R1 décrivent le résultat attendu du futur moteur de règles.
Ils ne sont pas encore exécutés par le programme.

| Votes de trois joueurs | Situation | Résultat attendu |
|---|---|---|
| 5, 5, 8 | Règle stricte, deuxième tour | Nouveau vote, car il n'y a pas unanimité |
| 5, 5, 8 | Majorité absolue, deuxième tour | Validation à 5, car deux joueurs sur trois ont choisi 5 |
| 5, 5, 8 | Majorité absolue, premier tour | Nouveau vote, car le premier tour exige l'unanimité |

La majorité absolue signifie strictement plus de la moitié des joueurs.
Avec quatre joueurs, deux votes identiques ne suffisent donc pas : il en faut trois.
Avec deux joueurs, les règles stricte et majorité absolue demandent toutes les deux
deux votes identiques ; trois joueurs permettent de mieux voir leur différence.

## Compléter le PV de R1

Les votes du PV portent sur la difficulté de développer US-01, US-02 et US-03.
Ils sont indépendants des valeurs 5, 5 et 8 utilisées dans les critères d'acceptation.

Pour chaque US :

1. Lire le besoin et le comparer à l'US de référence.
2. Choisir chacun une carte, sans se consulter.
3. Révéler les cartes et noter les deux valeurs dans le PV.
4. En cas de désaccord, noter une phrase de chaque membre et revoter.
5. Reporter la valeur commune dans le backlog.

La référence proposée est US-04 à 3 points, à confirmer en binôme.
Les points comparent la difficulté ; ils ne donnent pas une durée en heures.

## Vérifier les tests

```sh
python3 -m unittest discover -s tests -v
```

Les neuf tests couvrent le chargement, l'ordre des fonctionnalités, les erreurs de
fichier et de structure, les identifiants en double et la configuration des joueurs.
Le moteur de vote et de validation n'est pas encore couvert.

## Ce qui reste pour terminer R1

- Compléter les votes, les estimations et les deux lignes de retour réflexif.
- Lire et adopter la définition de « terminé » en binôme.
- Essayer le programme sur les deux machines.
- Créer le tableau de suivi et relier l'issue US-04 à sa PR.
- Faire relire puis fusionner la PR et déposer le lien du commit sur Moodle.
