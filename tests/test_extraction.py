import unittest

from src.contrat import Evenement
from src.extraction import masquer_secrets


class TestExtraction(unittest.TestCase):
    def test_masquer_secrets(self):
        self.assertEqual(masquer_secrets("user=bob password=abc123"),
                         "user=bob password=[SECRET]")

    def test_masquer_chaque_parametre_sans_tenir_compte_de_la_casse(self):
        for nom in ("password", "passwd", "token", "secret", "api_key", "apikey"):
            for casse in (nom, nom.upper(), nom.title()):
                with self.subTest(parametre=casse):
                    self.assertEqual(masquer_secrets(f"{casse}=abc123"),
                                     f"{casse}=[SECRET]")

    def test_masquer_separateurs_et_delimiteurs(self):
        for separateur in ("=", ":", ": "):
            for delimiteur in (" ", "&", ",", ";"):
                with self.subTest(separateur=separateur, delimiteur=delimiteur):
                    self.assertEqual(
                        masquer_secrets(f"token{separateur}abc{delimiteur}suite"),
                        f"token{separateur}[SECRET]{delimiteur}suite",
                    )

    def test_masquer_plusieurs_secrets(self):
        self.assertEqual(
            masquer_secrets("password=abc&API_KEY: xyz;token=123,passwd: def"),
            "password=[SECRET]&API_KEY: [SECRET];token=[SECRET],passwd: [SECRET]",
        )

    def test_texte_sans_secret_inchange(self):
        for texte in ("", "Service demarre", "user=bob tokenized=abc mypassword=xyz"):
            with self.subTest(texte=texte):
                self.assertEqual(masquer_secrets(texte), texte)


if __name__ == "__main__":
    unittest.main()
