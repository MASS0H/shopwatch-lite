from dataclasses import dataclass

NIVEAUX = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

PROCEDURES = {
    "oomkilled": "Conteneur arrete faute de memoire : augmenter la limite memoire.",
    "pipeline": "Echec de pipeline : lire les logs du job puis relancer apres correction.",
    "vulnerabilite": "Vulnerabilite : mettre a jour la dependance vers une version corrigee.",
}


@dataclass
class Evenement:
    id: str
    timestamp: str
    source: str
    component: str
    environment: str
    event_type: str
    severity: str
    message: str
    status: str = "NEW"


@dataclass
class Analyse:
    event_id: str
    level: str
    explanation: str
    action: str
    sensitive: bool
    sources: list


@dataclass
class Notification:
    event_id: str
    channel: str
    recipient: str
    text: str
