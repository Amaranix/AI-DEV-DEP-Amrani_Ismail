"""Pont entre l'API et le paquet sentiment_app.

L'API importe le paquet comme n'importe quelle dépendance installée,
sans modifier le chemin de recherche des modules Python.
"""

from pathlib import Path
import sys
from typing import Literal, TypedDict

from sentiment_app.predict import ModeleIntrouvable, charger_modele, predire

LabelType = Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]


class PredictResult(TypedDict):
    label: LabelType
    score: float
    text: str


class SentimentClassifier:
    """Enveloppe du modèle avec l'interface attendue par l'API."""

    model_name = "tfidf-logreg (TP2, models/sentiment.joblib)"

    def __init__(self) -> None:
        if "predict" in sys.modules:
            src_pred = sys.modules["predict"]
            if hasattr(src_pred, "MODELE") and not Path(src_pred.MODELE).exists():
                raise FileNotFoundError(f"models/sentiment.joblib absent : {src_pred.MODELE}")

        try:
            self.pipeline = charger_modele()
        except ModeleIntrouvable as err:
            raise FileNotFoundError(str(err)) from err

        classes = set(self.pipeline.classes_)
        classes_attendues = {"positive", "negative"}
        if not classes.issubset(classes_attendues):
            raise ValueError(f"Classes du modèle inconnues : {classes}")

    def predict(self, text: str) -> PredictResult:
        """Renvoie {'label': 'POSITIVE'|'NEGATIVE'|'INDETERMINE', 'score': float, 'text': aperçu}."""
        if not text.strip():
            raise ValueError("texte vide")
        r = predire(text, modele=self.pipeline)
        label_val: LabelType = "INDETERMINE"
        if r["label"] == "POSITIVE":
            label_val = "POSITIVE"
        elif r["label"] == "NEGATIVE":
            label_val = "NEGATIVE"
        return {"label": label_val, "score": float(r["score"]), "text": text[:100]}


def load_model() -> SentimentClassifier:
    """Construit le classifier pour FastAPI."""
    return SentimentClassifier()
