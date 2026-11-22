
import unittest

from planning_poker.moteur_regles import evaluer_vote
from planning_poker.partie import RegleValidation


class MoteurReglesTests(unittest.TestCase):

    def test_stricte_unanimite_premier_tour(self):
        resultat = evaluer_vote(
            RegleValidation.STRICTE, 1, [5, 5, 5]
        )
        self.assertTrue(resultat.valide)
        self.assertEqual(resultat.estimation, 5)

    def test_stricte_sans_unanimite(self):
        resultat = evaluer_vote(
            RegleValidation.STRICTE, 2, [5, 5, 8]
        )
        self.assertFalse(resultat.valide)
        self.assertIsNone(resultat.estimation)

    def test_majorite_premier_tour_exige_unanimite(self):
        resultat = evaluer_vote(
            RegleValidation.MAJORITE_ABSOLUE, 1, [5, 5, 8]
        )
        self.assertFalse(resultat.valide)

    def test_majorite_absolue_deuxieme_tour(self):
        resultat = evaluer_vote(
            RegleValidation.MAJORITE_ABSOLUE, 2, [5, 5, 8]
        )
        self.assertTrue(resultat.valide)
        self.assertEqual(resultat.estimation, 5)

    def test_majorite_absolue_egalite(self):
        resultat = evaluer_vote(
            RegleValidation.MAJORITE_ABSOLUE, 2, [5, 5, 8, 8]
        )
        self.assertFalse(resultat.valide)
        self.assertIsNone(resultat.estimation)

    def test_liste_de_votes_vide(self):
        with self.assertRaises(ValueError):
            evaluer_vote(
                RegleValidation.STRICTE, 1, []
            )


if __name__ == "__main__":
    unittest.main()
