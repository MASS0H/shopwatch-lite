import unittest

from src.extraction import masquer_donnees


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


if __name__ == "__main__":
    unittest.main()
