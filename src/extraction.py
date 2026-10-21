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
    if not {"id_faille", "paquet", "risque", "date"}.issubset(rapport):
        raise ValueError("Un scan doit contenir id_faille, paquet, risque et date")
    gravites = {"critique": "BLOQUANT", "haut": "MAJEUR", "moyen": "MODERE"}
    return Signal(
        ref=f"SH-{numero:04d}",
        date=rapport["date"],
        origine="SCANNER",
        service=rapport["paquet"],
        env=env,
        categorie="FAILLE",
        gravite=gravites.get(rapport["risque"].lower(), "MINEUR"),
        texte=f"Faille {rapport['id_faille']} dans {rapport['paquet']}",
    )


def lire_build(rapport: dict, numero: int, env: str = "production") -> Signal:
    if not {"etape", "resultat", "date"}.issubset(rapport):
        raise ValueError("Un build doit contenir etape, resultat et date")
    echec = rapport["resultat"].lower() == "echec"
    return Signal(
        ref=f"SH-{numero:04d}",
        date=rapport["date"],
        origine="BUILD",
        service=rapport["etape"],
        env=env,
        categorie="BUILD_ECHEC" if echec else "BUILD_OK",
        gravite="MAJEUR" if echec else "MINEUR",
        texte=f"Build {rapport['etape']} : {rapport['resultat']}",
    )
