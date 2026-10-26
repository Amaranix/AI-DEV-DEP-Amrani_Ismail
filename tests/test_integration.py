"""Tests d'intégration : l'API telle qu'elle tourne vraiment (TP4, étape D).

Les tests du TP3 vérifient des réponses ; ceux-ci vérifient le démarrage de l'API
et son comportement quand le modèle manque ou tombe en panne.
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

RACINE = Path(__file__).resolve().parents[1]
if str(RACINE / "src") not in sys.path:
    sys.path.insert(0, str(RACINE / "src"))
import predict  # noqa: E402

MODELE = RACINE / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


def test_demarrage_reel_charge_le_modele():
    """D.1 : un client ouvert par « with » exécute le lifespan."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        reponse = client.get("/health")
    assert reponse.status_code == 200
    assert "TP2" in reponse.json()["model"]


def test_modele_absent_refuse_de_demarrer(monkeypatch):
    """D.2 : chemin du modèle redirigé vers fichier inexistant, cache vidé, FileNotFoundError."""
    from fastapi.testclient import TestClient

    from api.main import app

    faux_chemin = RACINE / "models" / "inexistant.joblib"
    monkeypatch.setattr(predict, "MODELE", faux_chemin)
    predict.charger_modele.cache_clear()

    with pytest.raises(FileNotFoundError):
        with TestClient(app):
            pass

    predict.charger_modele.cache_clear()


def test_modele_non_charge_repond_503():
    """D.3 : l'API démarrée, modèle retiré de app.state, 503 sur /health et /predict."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        app.state.classifier = None
        r_health = client.get("/health")
        assert r_health.status_code == 503
        assert r_health.json()["detail"] == "Modèle non chargé"

        r_predict = client.post("/predict", json={"text": "Service impeccable"})
        assert r_predict.status_code == 503
        assert r_predict.json()["detail"] == "Modèle non chargé"


def test_modele_en_panne_runtime_error_repond_500():
    """D.4 : predict lève RuntimeError -> 500 sans fuite de message interne."""
    from fastapi.testclient import TestClient

    from api.main import app

    mock_clf = MagicMock()
    mock_clf.predict.side_effect = RuntimeError("panne interne critique")
    mock_clf.model_name = "mock-modele"

    with TestClient(app) as client:
        client.app.state.classifier = mock_clf
        reponse = client.post("/predict", json={"text": "Test panne"})
        assert reponse.status_code == 500
        assert reponse.json()["detail"] == "Erreur interne du serveur"
        assert "panne interne critique" not in reponse.text


def test_modele_en_panne_value_error_repond_500():
    """D.4 : predict lève ValueError('bug interne') -> 500 sans fuite."""
    from fastapi.testclient import TestClient

    from api.main import app

    mock_clf = MagicMock()
    mock_clf.predict.side_effect = ValueError("bug interne")
    mock_clf.model_name = "mock-modele"

    with TestClient(app) as client:
        client.app.state.classifier = mock_clf
        reponse = client.post("/predict", json={"text": "Test panne"})
        assert reponse.status_code == 500
        assert reponse.json()["detail"] == "Erreur interne du serveur"
        assert "bug interne" not in reponse.text
