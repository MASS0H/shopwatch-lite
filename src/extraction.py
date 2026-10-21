import re

from src.contrat import Evenement


def masquer_secrets(texte: str) -> str:
    return re.sub(
        r"\b(password|passwd|token|secret|api_key|apikey)(\s*[=:]\s*)[^\s&,;]+",
        r"\1\2[SECRET]",
        texte,
        flags=re.IGNORECASE,
    )


def normaliser_log(ligne: str, numero: int, source: str = "DOCKER",
                  environment: str = "production") -> Evenement:
    champs = ligne.split(maxsplit=4)
    if len(champs) < 5:
        raise ValueError("Une ligne de log doit contenir au moins 5 champs")
    date, heure, niveau, composant, message = champs
    gravites = {
        "CRITICAL": "CRITICAL", "FATAL": "CRITICAL", "ERROR": "HIGH",
        "WARN": "MEDIUM", "WARNING": "MEDIUM",
    }
    return Evenement(
        id=f"EVT-{numero:05d}",
        timestamp=f"{date}T{heure}Z",
        source=source,
        component=composant,
        environment=environment,
        event_type="LOG",
        severity=gravites.get(niveau.upper(), "LOW"),
        message=masquer_secrets(message),
    )


def normaliser_scan(rapport: dict, numero: int,
                   environment: str = "production") -> Evenement:
    raise NotImplementedError


def normaliser_pipeline(rapport: dict, numero: int,
                       environment: str = "production") -> Evenement:
    raise NotImplementedError
