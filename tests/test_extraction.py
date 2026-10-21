import unittest

from src.contrat import Evenement
from src.extraction import masquer_secrets, normaliser_log, normaliser_scan

LIGNE = "2026-10-05 10:02:11 ERROR backend OOMKilled restarts=14 password=abc123"


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

    def test_normaliser_log(self):
        evt = normaliser_log(LIGNE, 42)
        self.assertIsInstance(evt, Evenement)
        self.assertEqual(evt, Evenement(
            "EVT-00042", "2026-10-05T10:02:11Z", "DOCKER", "backend",
            "production", "LOG", "HIGH", "OOMKilled restarts=14 password=[SECRET]",
        ))
        self.assertEqual(evt.status, "NEW")
        self.assertNotIn("abc123", evt.message)

    def test_niveaux_log(self):
        for niveau, attendu in (
            ("CRITICAL", "CRITICAL"), ("fatal", "CRITICAL"), ("error", "HIGH"),
            ("warn", "MEDIUM"), ("WaRnInG", "MEDIUM"), ("INFO", "LOW"),
            ("debug", "LOW"), ("INCONNU", "LOW"),
        ):
            with self.subTest(niveau=niveau):
                evt = normaliser_log(f"2026-10-05 10:02:11 {niveau} backend message", 1)
                self.assertEqual(evt.severity, attendu)

    def test_log_source_et_environnement_personnalises(self):
        evt = normaliser_log(LIGNE, 7, source="KUBERNETES", environment="test")
        self.assertEqual(evt.id, "EVT-00007")
        self.assertEqual(evt.source, "KUBERNETES")
        self.assertEqual(evt.environment, "test")

    def test_log_conserve_le_reste_du_message(self):
        evt = normaliser_log("2026-10-05 10:02:11 INFO backend Service  demarre", 1)
        self.assertEqual(evt.message, "Service  demarre")

    def test_log_incomplet(self):
        for ligne in ("", "2026-10-05", "2026-10-05 10:02:11",
                      "2026-10-05 10:02:11 INFO", "2026-10-05 10:02:11 INFO backend"):
            with self.subTest(ligne=ligne):
                with self.assertRaises(ValueError):
                    normaliser_log(ligne, 1)

    def test_normaliser_scan(self):
        rapport = {"cve": "CVE-2026-1234", "package": "lib-xyz", "severity": "critical",
                   "date": "2026-10-05T10:07:00Z"}
        evt = normaliser_scan(rapport, 42)
        self.assertEqual(evt, Evenement(
            "EVT-00042", rapport["date"], "TRIVY", "lib-xyz", "production",
            "VULNERABILITY", "CRITICAL", "Vulnerabilite CVE-2026-1234 dans lib-xyz",
        ))
        self.assertEqual(evt.status, "NEW")

    def test_niveaux_scan(self):
        for niveau, attendu in (("critical", "CRITICAL"), ("High", "HIGH"),
                                ("medium", "MEDIUM"), ("low", "LOW"),
                                ("UNKNOWN", "LOW"), ("", "LOW")):
            with self.subTest(niveau=niveau):
                rapport = {"cve": "CVE-1", "package": "lib", "severity": niveau,
                           "date": "2026-10-05T10:07:00Z"}
                self.assertEqual(normaliser_scan(rapport, 1).severity, attendu)

    def test_scan_environnement_personnalise(self):
        rapport = {"cve": "CVE-1", "package": "lib", "severity": "high", "date": "date"}
        evt = normaliser_scan(rapport, 1, environment="dev")
        self.assertEqual(evt.environment, "dev")
        self.assertEqual(evt.timestamp, "date")

    def test_scan_cle_manquante(self):
        rapport = {"cve": "CVE-1", "package": "lib", "severity": "high", "date": "date"}
        for cle in rapport:
            with self.subTest(cle=cle):
                incomplet = {k: v for k, v in rapport.items() if k != cle}
                with self.assertRaises(ValueError):
                    normaliser_scan(incomplet, 1)


if __name__ == "__main__":
    unittest.main()
