
from collections import Counter
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

    # Au premier tour, toutes les règles exigent l'unanimité.
    if numero_tour == 1 or regle == RegleValidation.STRICTE:
        if all(vote == votes[0] for vote in votes):
            return ResultatVote(
                valide=True,
                estimation=votes[0],
                raison="Unanimité obtenue."
            )

        return ResultatVote(
            valide=False,
            estimation=None,
            raison="Les votes ne sont pas unanimes."
        )

    # À partir du deuxième tour : majorité absolue.
    if regle == RegleValidation.MAJORITE_ABSOLUE:
        occurrences = Counter(votes)

        for valeur, nombre in occurrences.items():
            if nombre > len(votes) / 2:
                return ResultatVote(
                    valide=True,
                    estimation=valeur,
                    raison="Majorité absolue obtenue."
                )

        return ResultatVote(
            valide=False,
            estimation=None,
            raison="Aucune majorité absolue."
        )

    raise ValueError("Règle de validation inconnue.")
