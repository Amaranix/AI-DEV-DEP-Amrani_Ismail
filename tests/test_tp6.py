"""Contrôles du TP6 : emplacement du modèle, API sans sys.path, paquet installable."""

from pathlib import Path

from click.testing import CliRunner

from sentiment_app import __version__
from sentiment_app.cli import main
from sentiment_app.predict import ENV_MODELE, chemin_modele

RACINE = Path(__file__).resolve().parents[1]


def test_le_modele_se_place_ou_l_on_veut(monkeypatch, tmp_path):
    fichier = tmp_path / "autre.joblib"
    fichier.write_bytes(b"")
    monkeypatch.setenv(ENV_MODELE, str(fichier))
    assert chemin_modele() == fichier


def test_l_api_ne_bricole_plus_le_chemin_de_python():
    for fichier in (RACINE / "api").glob("*.py"):
        texte = fichier.read_text(encoding="utf-8")
        assert "sys.path" not in texte, f"{fichier.name} modifie sys.path"


def test_version_du_paquet():
    assert __version__ == "0.6.0"


def test_cli_version():
    resultat = CliRunner().invoke(main, ["--version"])
    assert resultat.exit_code == 0
    assert "sentiment-app 0.6.0" in resultat.output


def test_predict_sans_modele_sort_avec_code_1(monkeypatch, tmp_path):
    monkeypatch.setenv(ENV_MODELE, str(tmp_path / "absent.joblib"))
    resultat = CliRunner().invoke(main, ["predict", "bon produit"])
    assert resultat.exit_code == 1
    assert "modèle introuvable" in resultat.output
