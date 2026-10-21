import unittest

from src.contrat import Signal
from src.extraction import lire_journal, masquer_donnees

LIGNE = "2026-11-27 17:02:11 paiement ERROR timeout passerelle apres 30s card=4970123412341234"


class TestExtraction(unittest.TestCase):
    def test_masquer_donnees(self):
        self.assertEqual(masquer_donnees("client=bob pwd=abc123"),
                         "client=bob pwd=[MASQUE]")

    def test_masquer_chaque_parametre_sans_tenir_compte_de_la_casse(self):
        for nom in ("password", "pwd", "token", "secret", "card", "iban"):
            for casse in (nom, nom.upper(), nom.title()):
                with self.subTest(parametre=casse):
                    self.assertEqual(masquer_donnees(f"{casse}=abc123"),
                                     f"{casse}=[MASQUE]")

    def test_masquer_separateurs_et_delimiteurs(self):
        for separateur in ("=", ":", ": "):
            for delimiteur in (" ", "&", ",", ";"):
                with self.subTest(separateur=separateur, delimiteur=delimiteur):
                    self.assertEqual(
                        masquer_donnees(f"card{separateur}4970123412341234{delimiteur}suite"),
                        f"card{separateur}[MASQUE]{delimiteur}suite",
                    )

    def test_masquer_plusieurs_donnees(self):
        self.assertEqual(
            masquer_donnees("pwd=abc&IBAN: MA123;token=123,card: 4970123412341234"),
            "pwd=[MASQUE]&IBAN: [MASQUE];token=[MASQUE],card: [MASQUE]",
        )

    def test_texte_sans_donnee_sensible_inchange(self):
        for texte in ("", "Service demarre", "client=bob cardholder=Alice mypassword=xyz"):
            with self.subTest(texte=texte):
                self.assertEqual(masquer_donnees(texte), texte)

    def test_lire_journal(self):
        sig = lire_journal(LIGNE, 42)
        self.assertIsInstance(sig, Signal)
        self.assertEqual(sig, Signal(
            "SH-0042", "2026-11-27T17:02:11Z", "PAIEMENT", "paiement",
            "production", "JOURNAL", "MAJEUR", "timeout passerelle apres 30s card=[MASQUE]",
        ))
        self.assertEqual(sig.etat, "RECU")
        self.assertNotIn("4970123412341234", sig.texte)

    def test_gravites_journal(self):
        for niveau, attendu in (
            ("FATAL", "BLOQUANT"), ("critical", "BLOQUANT"), ("error", "MAJEUR"),
            ("warn", "MODERE"), ("WaRnInG", "MODERE"), ("INFO", "MINEUR"),
            ("DEBUG", "MINEUR"), ("INCONNU", "MINEUR"),
        ):
            with self.subTest(niveau=niveau):
                sig = lire_journal(f"2026-11-27 17:02:11 paiement {niveau} message", 1)
                self.assertEqual(sig.gravite, attendu)

    def test_journal_origine_et_environnement_personnalises(self):
        sig = lire_journal(LIGNE, 7, origine="PANIER", env="test")
        self.assertEqual(sig.ref, "SH-0007")
        self.assertEqual(sig.origine, "PANIER")
        self.assertEqual(sig.env, "test")

    def test_journal_conserve_le_reste_du_texte(self):
        sig = lire_journal("2026-11-27 17:02:11 paiement INFO Service  demarre", 1)
        self.assertEqual(sig.texte, "Service  demarre")

    def test_journal_incomplet(self):
        for ligne in ("", "2026-11-27", "2026-11-27 17:02:11",
                      "2026-11-27 17:02:11 paiement", "2026-11-27 17:02:11 paiement INFO"):
            with self.subTest(ligne=ligne):
                with self.assertRaises(ValueError):
                    lire_journal(ligne, 1)


if __name__ == "__main__":
    unittest.main()
