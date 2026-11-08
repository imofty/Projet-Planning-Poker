"""Données et validation d'une partie, indépendantes de la console."""

from dataclasses import dataclass
from enum import Enum


class RegleValidation(str, Enum):
    STRICTE = "strict"
    MAJORITE_ABSOLUE = "majorite_absolue"


@dataclass(frozen=True)
class ConfigurationPartie:
    pseudos: tuple[str, ...]
    regle: RegleValidation

    def __post_init__(self) -> None:
        if not self.pseudos:
            raise ValueError("La partie doit comporter au moins un joueur.")
        if any(not isinstance(pseudo, str) or not pseudo.strip() for pseudo in self.pseudos):
            raise ValueError("Chaque joueur doit avoir un pseudo non vide.")
        pseudos = tuple(pseudo.strip() for pseudo in self.pseudos)
        if len({pseudo.casefold() for pseudo in pseudos}) != len(pseudos):
            raise ValueError("Les pseudos doivent être distincts, même sans tenir compte des majuscules.")
        if not isinstance(self.regle, RegleValidation):
            raise ValueError("La règle de validation est inconnue.")
        object.__setattr__(self, "pseudos", pseudos)


@dataclass(frozen=True)
class Fonctionnalite:
    identifiant: str
    titre: str


@dataclass(frozen=True)
class Backlog:
    projet: str
    fonctionnalites: tuple[Fonctionnalite, ...]


@dataclass(frozen=True)
class Partie:
    configuration: ConfigurationPartie
    backlog: Backlog

    @property
    def fonctionnalite_courante(self) -> Fonctionnalite:
        return self.backlog.fonctionnalites[0]
