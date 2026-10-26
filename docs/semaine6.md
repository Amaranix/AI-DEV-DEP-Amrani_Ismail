# Semaine 6 : packaging de l'application

## Objectif du TP6

Transformer le projet sentiment-app en un paquet Python installable via `pip`, exposer une commande `sentiment` en ligne de commande, et produire une roue (`wheel`) distribuable indépendamment du dépôt.

## Architecture du paquet

Le TP6 réorganise le code autour d'un paquet `sentiment_app` installable :

| Fichier | Rôle |
| --- | --- |
| `sentiment_app/__init__.py` | Déclare la version `0.6.0` |
| `sentiment_app/predict.py` | Chargement du modèle et prédiction ; chemin configurable via `SENTIMENT_MODELE` |
| `sentiment_app/cli.py` | Interface CLI : `sentiment predict`, `sentiment serve`, `sentiment --version` |
| `src/predict.py` | Fichier de compatibilité : délègue au paquet (TP2-TP5 non cassés) |
| `api/model.py` | Pont API → paquet, sans `sys.path` |
| `pyproject.toml` | Métadonnées, dépendances, point d'entrée CLI, règles de découverte |

## Résolution du chemin du modèle

L'ancienne version codait le chemin en dur (relatif au dépôt). La nouvelle version cherche dans l'ordre :

1. La variable d'environnement `SENTIMENT_MODELE` (prioritaire)
2. `models/sentiment.joblib` relatif à la racine du paquet (mode développement)

Cela permet d'utiliser la roue installée *hors du dépôt* en pointant vers n'importe quel modèle :

```powershell
$env:SENTIMENT_MODELE = "C:\IA-DEV\sentiment-app\models\sentiment.joblib"
sentiment predict "Livraison rapide, très satisfait"
```

## Commande `sentiment`

Après `pip install -e .` :

```powershell
sentiment --version          # sentiment-app 0.6.0
sentiment predict "texte"    # POSITIVE 0.777 / NEGATIVE / INDETERMINE
sentiment serve              # lance l'API uvicorn sur 127.0.0.1:8000
```

La commande `predict` applique également le seuil d'abstention (0.6) : un avis ambigu reçoit `INDETERMINE` plutôt qu'un verdict forcé.

## La roue (wheel)

```powershell
python -m build --wheel
```

Produit `dist/sentiment_app-0.6.0-py3-none-any.whl`. La roue contient uniquement `api/`, `sentiment_app/` et `ui/` — ni tests, ni données, ni modèle. Ce tri est défini dans `pyproject.toml` par `[tool.setuptools.packages.find]`.

Une roue « pure Python » (`py3-none-any`) s'installe sur tous les systèmes sans compilation.

## Tests ajoutés

Cinq nouveaux tests dans `tests/test_tp6.py` :

| Test | Vérifie |
| --- | --- |
| `test_le_modele_se_place_ou_l_on_veut` | Variable `SENTIMENT_MODELE` prise en compte |
| `test_l_api_ne_bricole_plus_le_chemin_de_python` | Aucun `sys.path` dans `api/*.py` |
| `test_version_du_paquet` | `__version__ == "0.6.0"` |
| `test_cli_version` | `sentiment --version` affiche `sentiment-app 0.6.0` |
| `test_predict_sans_modele_sort_avec_code_1` | Code de sortie 1 quand le modèle est absent |

## Intégration continue

La CI ajoute une étape « Roue installée hors du dépôt (TP6) » qui :

1. Construit la roue avec `python -m build --wheel`
2. Crée un venv vierge dans `$RUNNER_TEMP/roue`
3. Installe la roue dans ce venv
4. Vérifie que `sentiment --version` fonctionne sans accès au dépôt

## Répartition du travail

- **Membre A (Lamzouri Ishak)** : création du paquet `sentiment_app/`, mise à jour de `api/model.py`, `pyproject.toml`, CI.
- **Membre B (Amrani Ismail)** : fichier de compatibilité `src/predict.py`, tests `test_tp6.py`, compte rendu, tag et push final.
