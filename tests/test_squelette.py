"""Vérifications du démarrage et du chargement d'US-04, sans moteur de règles."""

import json
from pathlib import Path
import tempfile
import unittest

from planning_poker.backlog import ErreurBacklog, charger_backlog
from planning_poker.partie import ConfigurationPartie, Partie, RegleValidation


class ChargementBacklogTests(unittest.TestCase):
    def setUp(self):
        self.dossier = tempfile.TemporaryDirectory()
        self.addCleanup(self.dossier.cleanup)
        self.chemin = Path(self.dossier.name) / "backlog.json"

    def ecrire(self, contenu):
        self.chemin.write_text(json.dumps(contenu), encoding="utf-8")

    def test_US_04_preserve_ordre_et_affiche_premiere_fonctionnalite(self):
        self.ecrire({"projet": "Bibliothèque", "fonctionnalites": [
            {"id": "F2", "titre": "Emprunter"}, {"id": "F1", "titre": "Chercher"}
        ]})
        backlog = charger_backlog(self.chemin)
        partie = Partie(ConfigurationPartie(("A", "B"), RegleValidation.STRICTE), backlog)
        self.assertEqual(backlog.projet, "Bibliothèque")
        self.assertEqual([f.identifiant for f in backlog.fonctionnalites], ["F2", "F1"])
        self.assertEqual(partie.fonctionnalite_courante.titre, "Emprunter")

    def test_US_04_fichier_absent(self):
        with self.assertRaises(ErreurBacklog):
            charger_backlog(self.chemin)

    def test_US_04_json_malforme(self):
        self.chemin.write_text('{"projet":', encoding="utf-8")
        with self.assertRaises(ErreurBacklog):
            charger_backlog(self.chemin)

    def test_US_04_encodage_invalide(self):
        self.chemin.write_bytes(b"\xff\xfe\x00")
        with self.assertRaises(ErreurBacklog):
            charger_backlog(self.chemin)

    def test_US_04_structure_et_champs_invalides(self):
        cas = [
            [], {}, {"projet": "  ", "fonctionnalites": []},
            {"projet": "P", "fonctionnalites": []},
            {"projet": "P", "fonctionnalites": "incorrect"},
            {"projet": "P", "fonctionnalites": ["incorrect"]},
            {"projet": "P", "fonctionnalites": [{"id": "F1"}]},
            {"projet": "P", "fonctionnalites": [{"id": 1, "titre": "T"}]},
            {"projet": "P", "fonctionnalites": [{"id": "F1", "titre": " "}]},
        ]
        for contenu in cas:
            with self.subTest(contenu=contenu):
                self.ecrire(contenu)
                with self.assertRaises(ErreurBacklog):
                    charger_backlog(self.chemin)

    def test_US_04_identifiants_dupliques(self):
        self.ecrire({"projet": "P", "fonctionnalites": [
            {"id": "F1", "titre": "A"}, {"id": " F1 ", "titre": "B"}
        ]})
        with self.assertRaises(ErreurBacklog):
            charger_backlog(self.chemin)


class ConfigurationPartieTests(unittest.TestCase):
    def test_US_04_configuration_et_normalisation(self):
        configuration = ConfigurationPartie((" A ", "B"), RegleValidation.MAJORITE_ABSOLUE)
        self.assertEqual(configuration.pseudos, ("A", "B"))
        self.assertEqual(configuration.regle.value, "majorite_absolue")

    def test_US_04_joueurs_invalides(self):
        for pseudos in [(), (" ",), ("A", "a"), (" A ", "A"), (1,)]:
            with self.subTest(pseudos=pseudos):
                with self.assertRaises(ValueError):
                    ConfigurationPartie(pseudos, RegleValidation.STRICTE)

    def test_US_04_regle_inconnue(self):
        with self.assertRaises(ValueError):
            ConfigurationPartie(("A",), "inconnue")


if __name__ == "__main__":
    unittest.main()
