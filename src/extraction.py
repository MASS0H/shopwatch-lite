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
    if not {"cve", "package", "severity", "date"}.issubset(rapport):
        raise ValueError("Un rapport de scan doit contenir cve, package, severity et date")
    niveau = rapport["severity"].upper()
    return Evenement(
        id=f"EVT-{numero:05d}",
        timestamp=rapport["date"],
        source="TRIVY",
        component=rapport["package"],
        environment=environment,
        event_type="VULNERABILITY",
        severity=niveau if niveau in {"CRITICAL", "HIGH", "MEDIUM", "LOW"} else "LOW",
        message=f"Vulnerabilite {rapport['cve']} dans {rapport['package']}",
    )


def normaliser_pipeline(rapport: dict, numero: int,
                       environment: str = "production") -> Evenement:
    if not {"job", "status", "date"}.issubset(rapport):
        raise ValueError("Un rapport de pipeline doit contenir job, status et date")
    echec = rapport["status"].lower() == "failed"
    return Evenement(
        id=f"EVT-{numero:05d}",
        timestamp=rapport["date"],
        source="CI",
        component=rapport["job"],
        environment=environment,
        event_type="PIPELINE_FAILURE" if echec else "PIPELINE_OK",
        severity="HIGH" if echec else "LOW",
        message=f"Pipeline {rapport['job']} : {rapport['status']}",
    )
