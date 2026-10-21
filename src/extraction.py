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
    raise NotImplementedError


def lire_scan(rapport: dict, numero: int, env: str = "production") -> Signal:
    raise NotImplementedError


def lire_build(rapport: dict, numero: int, env: str = "production") -> Signal:
    raise NotImplementedError
