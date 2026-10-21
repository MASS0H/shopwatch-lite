import re

from src.contrat import Signal


def masquer_donnees(texte: str) -> str:
    return re.sub(
        r"\b(password|pwd|token|secret|card|iban)(\s*[=:]\s*)[^\s&,;]+",
        r"\1\2[MASQUE]",
        texte,
        flags=re.IGNORECASE,
    )


def lire_journal(ligne: str, numero: int, origine: str = "PAIEMENT",
                 env: str = "production") -> Signal:
    champs = ligne.split(maxsplit=4)
    if len(champs) < 5:
        raise ValueError("Une ligne de journal doit contenir au moins 5 champs")
    date, heure, service, niveau, texte = champs
    gravites = {
        "FATAL": "BLOQUANT", "CRITICAL": "BLOQUANT", "ERROR": "MAJEUR",
        "WARN": "MODERE", "WARNING": "MODERE",
    }
    return Signal(
        ref=f"SH-{numero:04d}",
        date=f"{date}T{heure}Z",
        origine=origine,
        service=service,
        env=env,
        categorie="JOURNAL",
        gravite=gravites.get(niveau.upper(), "MINEUR"),
        texte=masquer_donnees(texte),
    )


def lire_scan(rapport: dict, numero: int, env: str = "production") -> Signal:
    raise NotImplementedError


def lire_build(rapport: dict, numero: int, env: str = "production") -> Signal:
    raise NotImplementedError
