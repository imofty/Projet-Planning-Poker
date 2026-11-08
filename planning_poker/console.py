"""Saisie et affichage : aucune règle de vote n'est implémentée en séance 1."""

import argparse

from .backlog import ErreurBacklog, charger_backlog
from .partie import ConfigurationPartie, Partie, RegleValidation


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

    print("Règle prévue : 1 = stricte ; 2 = majorité absolue")
    choix_regles = {"1": RegleValidation.STRICTE, "2": RegleValidation.MAJORITE_ABSOLUE}
    while True:
        choix = input("Choix de la règle [1/2] : ").strip()
        if choix in choix_regles:
            return ConfigurationPartie(tuple(pseudos), choix_regles[choix])
        print("Saisissez 1 ou 2.")


def main() -> int:
    parser = argparse.ArgumentParser(description="CAPI - démarrer une partie locale de Planning Poker.")
    parser.add_argument("backlog", nargs="?", help="Chemin du backlog JSON à charger.")
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
        premiere = partie.fonctionnalite_courante
        print(f"\nProjet : {backlog.projet}")
        print(f"Joueurs ({len(configuration.pseudos)}) : {', '.join(configuration.pseudos)}")
        print(f"Règle sélectionnée : {configuration.regle.value}")
        print(f"Fonctionnalité 1/{len(backlog.fonctionnalites)} : {premiere.identifiant} : {premiere.titre}")
        print("Session préparée. Le vote et la validation ne sont pas encore implémentés.")
        return 0
    except EOFError:
        print("\nSaisie interrompue : la partie n'a pas été démarrée.")
        return 1
    except KeyboardInterrupt:
        print("\nConfiguration annulée.")
        return 130
