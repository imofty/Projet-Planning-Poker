"""Chargement et vérification du format JSON documenté dans le README."""

import json
from pathlib import Path

from .partie import Backlog, Fonctionnalite


class ErreurBacklog(ValueError):
    """Un fichier de backlog ne peut pas être utilisé pour commencer la partie."""


def _texte_non_vide(valeur: object, champ: str) -> str:
    if not isinstance(valeur, str) or not valeur.strip():
        raise ErreurBacklog(f"Le champ {champ} doit être un texte non vide.")
    return valeur.strip()


def charger_backlog(chemin: str | Path) -> Backlog:
    try:
        with Path(chemin).open(encoding="utf-8-sig") as fichier:
            contenu = json.load(fichier)
    except (OSError, ValueError) as erreur:
        raise ErreurBacklog(f"Impossible de charger le backlog : {erreur}") from erreur

    if not isinstance(contenu, dict):
        raise ErreurBacklog("Le backlog doit être un objet JSON.")
    projet = _texte_non_vide(contenu.get("projet"), "projet")
    elements = contenu.get("fonctionnalites")
    if not isinstance(elements, list) or not elements:
        raise ErreurBacklog("Le champ fonctionnalites doit être une liste non vide.")

    fonctionnalites = []
    identifiants = set()
    for position, element in enumerate(elements, start=1):
        if not isinstance(element, dict):
            raise ErreurBacklog(f"La fonctionnalité n°{position} doit être un objet JSON.")
        identifiant = _texte_non_vide(element.get("id"), f"fonctionnalité n°{position}.id")
        titre = _texte_non_vide(element.get("titre"), f"fonctionnalité n°{position}.titre")
        if identifiant in identifiants:
            raise ErreurBacklog(f"L'identifiant {identifiant!r} apparaît plusieurs fois.")
        identifiants.add(identifiant)
        fonctionnalites.append(Fonctionnalite(identifiant, titre))

    return Backlog(projet, tuple(fonctionnalites))
