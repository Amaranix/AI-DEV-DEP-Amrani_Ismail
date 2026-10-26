"""Tests aux limites du contrat d'entrée (TP4, étape B).

PredictRequest promet un champ « text », chaîne de 1 à 2000 caractères.
Ce fichier vérifie cette promesse à ses frontières, puis au hasard (hypothesis).
"""
import json
from pathlib import Path

import pytest

pytest.importorskip("hypothesis")
from hypothesis import HealthCheck, given, settings  # noqa: E402
from hypothesis import strategies as st  # noqa: E402

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


@pytest.fixture(scope="module")
def client():
    """Portée « module » : l'API démarre une fois pour tout le fichier (hypothesis l'exige)."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as c:  # le « with » exécute le lifespan : le modèle est chargé
        yield c


def en_json(valeur: object) -> bytes:
    """Corps de requête JSON, sous forme d'octets : permet aussi d'envoyer un corps invalide."""
    return json.dumps(valeur).encode("utf-8")


CAS = [
    pytest.param(en_json({"text": ""}), 422, id="texte-vide"),
    pytest.param(en_json({"text": "   "}), 422, id="espaces-seuls"),
    pytest.param(en_json({"text": "a"}), 200, id="un-caractere"),
    pytest.param(en_json({"text": "a" * 2000}), 200, id="2000-caracteres"),
    pytest.param(en_json({"text": "a" * 2001}), 422, id="2001-caracteres"),
    pytest.param(en_json({}), 422, id="champ-absent"),
    pytest.param(en_json({"text": 42}), 422, id="type-invalide-42"),
    pytest.param(b"pas du json", 422, id="corps-non-json"),
    pytest.param(en_json({"text": "\x85"}), 422, id="espace-unicode-x85"),
]


@pytest.mark.parametrize("corps, code_attendu", CAS)
def test_frontieres_du_contrat(client, corps, code_attendu):
    reponse = client.post("/predict", content=corps, headers={"Content-Type": "application/json"})
    assert reponse.status_code == code_attendu
    if code_attendu == 422:
        detail = reponse.json().get("detail")
        assert isinstance(detail, list), f"detail n'est pas une liste pour 422 : {detail!r}"
        assert len(detail) > 0
        for err in detail:
            assert isinstance(err, dict)
            assert "loc" in err
            assert "msg" in err
            assert "type" in err


@settings(deadline=None, max_examples=50, suppress_health_check=[HealthCheck.filter_too_much])
@given(st.text(min_size=1, max_size=2000).filter(lambda s: bool(s.strip())))
def test_propriete_texte_valide_repond_200(client, texte):
    reponse = client.post("/predict", json={"text": texte})
    assert reponse.status_code == 200
    data = reponse.json()
    assert data["label"] in {"POSITIVE", "NEGATIVE", "INDETERMINE"}
    assert 0.0 <= data["score"] <= 1.0


@settings(deadline=None, max_examples=50)
@given(st.text(alphabet=" \t\r\n\x85\u00a0\u2000\u2001\u2002\u2003\u2009", min_size=1, max_size=2000))
def test_propriete_texte_espaces_repond_422(client, texte):
    reponse = client.post("/predict", json={"text": texte})
    assert reponse.status_code == 422
    detail = reponse.json().get("detail")
    assert isinstance(detail, list)
    assert len(detail) > 0
