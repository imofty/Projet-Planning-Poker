
from dataclasses import dataclass
from typing import Sequence

from .partie import RegleValidation


@dataclass(frozen=True)
class ResultatVote:
    valide: bool
    estimation: int | None
    raison: str


def evaluer_vote(
    regle: RegleValidation,
    numero_tour: int,
    votes: Sequence[int],
) -> ResultatVote:
    """Évalue les votes selon la règle choisie."""
    if not votes:
        raise ValueError("La liste des votes ne peut pas être vide.")

    raise NotImplementedError