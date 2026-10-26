"""Chargement du modèle et prédiction, sans aucun chemin codé en dur vers le dépôt.

Le modèle est cherché dans cet ordre :
1. la variable d'environnement SENTIMENT_MODELE, si elle est définie ;
2. models/sentiment.joblib à la racine du dépôt, quand le paquet est utilisé depuis les sources.

Dans une roue installée hors du dépôt, il faut donc fournir SENTIMENT_MODELE.
"""

import os
from pathlib import Path

import joblib

# Seuil d'abstention : sous ce score, le modèle ne tranche pas.
# Aligné sur la valeur retenue au TP4 (courbe_seuil.py).
SEUIL_ABSTENTION = 0.6
ENV_MODELE = "SENTIMENT_MODELE"


class ModeleIntrouvable(FileNotFoundError):
    """Levée quand le fichier du modèle n'existe pas à l'endroit attendu."""


def chemin_modele() -> Path:
    """Renvoie le chemin du modèle selon la variable d'environnement ou le dépôt."""
    env = os.environ.get(ENV_MODELE)
    if env:
        return Path(env)
    racine = Path(__file__).resolve().parents[1]
    return racine / "models" / "sentiment.joblib"


def charger_modele(chemin: Path | None = None):
    """Charge le pipeline scikit-learn sauvegardé au TP2."""
    chemin = Path(chemin) if chemin is not None else chemin_modele()
    if not chemin.exists():
        raise ModeleIntrouvable(
            f"modèle introuvable : {chemin}. Définissez {ENV_MODELE} "
            "ou lancez python src/train.py dans le dépôt."
        )
    return joblib.load(chemin)


def predire(texte: str, modele=None) -> dict:
    """Renvoie {'label': ..., 'score': ...} avec abstention sous SEUIL_ABSTENTION."""
    if modele is None:
        modele = charger_modele()
    probas = modele.predict_proba([texte])[0]
    idx = int(probas.argmax())
    score = float(probas[idx])
    if score < SEUIL_ABSTENTION:
        return {"label": "INDETERMINE", "score": round(score, 4)}
    return {"label": str(modele.classes_[idx]).upper(), "score": round(score, 4)}
