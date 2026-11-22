
"""Configuration, votes et affichage de la partie locale."""

import argparse

from .backlog import ErreurBacklog, charger_backlog
from .moteur_regles import evaluer_vote
from .partie import ConfigurationPartie, Partie, RegleValidation


CARTES = (0, 1, 2, 3, 5, 8, 13, 20, 40, 100)


def _saisir_configuration() -> ConfigurationPartie:
    while True:
        try:
            nombre = int(input("Nombre de joueurs : "))
            if nombre >= 1:
                break
        except ValueError:
            pass
        print("Saisissez un entier supérieur ou égal à 1.")

    pseudos: list[str] = []
    while len(pseudos) < nombre:
        pseudo = input(f"Pseudo du joueur {len(pseudos) + 1} : ").strip()
        if not pseudo:
            print("Le pseudo ne peut pas être vide.")
        elif pseudo.casefold() in {nom.casefold() for nom in pseudos}:
            print("Ce pseudo est déjà utilisé.")
        else:
            pseudos.append(pseudo)

    print("Règle : 1 = stricte ; 2 = majorité absolue")
    choix_regles = {
        "1": RegleValidation.STRICTE,
        "2": RegleValidation.MAJORITE_ABSOLUE,
    }

    while True:
        choix = input("Choix de la règle [1/2] : ").strip()
        if choix in choix_regles:
            return ConfigurationPartie(tuple(pseudos), choix_regles[choix])
        print("Saisissez 1 ou 2.")


def _saisir_votes(pseudos: tuple[str, ...]) -> list[int]:
    votes = []

    print("\nCartes disponibles :", ", ".join(map(str, CARTES)))

    for pseudo in pseudos:
        while True:
            try:
                vote = int(input(f"{pseudo}, choisissez votre carte : "))
                if vote in CARTES:
                    votes.append(vote)
                    break
            except ValueError:
                pass

            print("Carte invalide. Choisissez une carte disponible.")

    return votes


def _jouer_fonctionnalite(
    identifiant: str,
    titre: str,
    configuration: ConfigurationPartie,
) -> None:
    numero_tour = 1

    print(f"\nFonctionnalité : {identifiant} - {titre}")

    while True:
        print(f"\n--- Tour {numero_tour} ---")
        votes = _saisir_votes(configuration.pseudos)

        print("\nRévélation des votes :")
        for pseudo, vote in zip(configuration.pseudos, votes):
            print(f"{pseudo} : {vote}")

        resultat = evaluer_vote(
            configuration.regle,
            numero_tour,
            votes,
        )

        print(f"\nRésultat : {resultat.raison}")

        if resultat.valide:
            print(f"Fonctionnalité validée avec l'estimation : {resultat.estimation}")
            return

        print("Discussion nécessaire : un nouveau tour commence.")
        numero_tour += 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="CAPI - démarrer une partie locale de Planning Poker."
    )
    parser.add_argument("backlog", nargs="?", help="Chemin du backlog JSON.")
    arguments = parser.parse_args()

    try:
        print("=== Planning Poker - configuration ===")
        configuration = _saisir_configuration()
        chemin = arguments.backlog

        while True:
            if chemin is None:
                chemin = input("Chemin du backlog JSON : ").strip()
                if not chemin:
                    print("Indiquez le chemin d'un fichier JSON.")
                    continue

            try:
                backlog = charger_backlog(chemin)
                break
            except ErreurBacklog as erreur:
                print(f"Erreur : {erreur}")
                chemin = None

        partie = Partie(configuration, backlog)

        print(f"\nProjet : {backlog.projet}")
        print(f"Joueurs ({len(configuration.pseudos)}) : "
              f"{', '.join(configuration.pseudos)}")
        print(f"Règle sélectionnée : {configuration.regle.value}")

        for fonctionnalite in backlog.fonctionnalites:
            _jouer_fonctionnalite(
                fonctionnalite.identifiant,
                fonctionnalite.titre,
                configuration,
            )

        print("\nToutes les fonctionnalités ont été estimées.")
        return 0

    except EOFError:
        print("\nSaisie interrompue.")
        return 1
    except KeyboardInterrupt:
        print("\nPartie interrompue.")
        return 130
