"""Fichier de compatibilité : ancien emplacement de predict.py (TP2 à TP5).

Copié dans src/predict.py au contrôle T36, il permet de continuer à lancer
`python src/predict.py "texte"` après le déplacement du module dans le paquet.
"""

from functools import lru_cache
from pathlib import Path
import sys

from sentiment_app.predict import ModeleIntrouvable, predire

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"


@lru_cache(maxsize=1)
def charger_modele():
    """Chargé une seule fois par processus, pas à chaque appel."""
    import joblib
    if not MODELE.exists():
        raise FileNotFoundError(f"models/sentiment.joblib absent : {MODELE}")
    return joblib.load(MODELE)


def predict(texte: str) -> dict:
    """Renvoie {'label': 'positive'|'negative', 'score': float}."""
    if not isinstance(texte, str) or not texte.strip():
        raise ValueError("texte vide")
    pipeline = charger_modele()
    etiquette = str(pipeline.predict([texte])[0]).lower()
    score = float(pipeline.predict_proba([texte]).max())
    return {"label": etiquette, "score": round(score, 4)}


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print("usage : python src/predict.py \"texte de l'avis\"", file=sys.stderr)
        return 2
    try:
        pipeline = charger_modele()
    except (ModeleIntrouvable, FileNotFoundError) as erreur:
        print(f"Erreur : {erreur}", file=sys.stderr)
        return 1
    resultat = predire(" ".join(argv), modele=pipeline)
    print(f"{resultat['label'].lower()} (confiance {round(resultat['score'] * 100)}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
