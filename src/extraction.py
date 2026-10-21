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
    raise NotImplementedError


def normaliser_scan(rapport: dict, numero: int,
                   environment: str = "production") -> Evenement:
    raise NotImplementedError


def normaliser_pipeline(rapport: dict, numero: int,
                       environment: str = "production") -> Evenement:
    raise NotImplementedError
