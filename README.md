# sentiment-app : Plateforme d'Analyse de Sentiment (TP1 à TP5)

Application fil rouge du cours *Développement et déploiement d'applications intelligentes*.  
Ce dépôt retrace l'ensemble des travaux réalisés de la semaine 1 à la semaine 5, du cadrage métier et de l'architecture logicielle, jusqu'au modèle de Machine Learning, son exposition par API REST FastAPI et son interface de déploiement interactive Streamlit.

---

## 👥 Membres du binôme & Traçabilité des rôles

| Rôle | Nom & Prénom | Identifiant GitHub | Responsabilités & Réalisations (TP1 à TP5) |
| :--- | :--- | :--- | :--- |
| **Membre A** | **Lamzouri Ishak** | [@inazuma2004](https://github.com/inazuma2004) | • Initialisation du dépôt Git & configuration de l'environnement virtuel (.venv)<br>• Cadrage métier : Cas 1 (Ordonnances - Règles métier) & Cas 2 (Règlement - RAG)<br>• Intégration du Kit TP2 (`train.py`, `evaluate.py`, `predict.py`)<br>• Entraînement du modèle de production sur Allociné (20 000 avis, $F_1 = 0,9205$)<br>• Exposition API FastAPI TP3 (`api/main.py`, `api/model.py`, routes `/health` et `/predict`)<br>• Écriture des tests aux limites TP4 (`test_limites.py`) et calibration du seuil d'abstention<br>• Intégration de l'interface Streamlit découplée TP5 (`ui/app.py`, `ui/client.py`) |
| **Membre B** | **Amrani Ismail** | [@Amaranix](https://github.com/Amaranix) | • Cadrage métier : Cas 3 (Priorisation des avis négatifs - Machine Learning)<br>• Génération des dépendances, recettes et tests d'intégration<br>• Recette fonctionnelle de l'API FastAPI (contrôles T15 à T20, gestion des refus 422)<br>• Implémentation des tests d'intégration TP4 (`test_integration.py`) et audit qualité `ruff`/`mypy`<br>• Rédaction du jeu d'or (`data/jeu_or.csv`) et analyse d'erreurs<br>• Validation du traitement de lot CSV TP5 (`data/avis_exemple.csv`) et validation des 97 tests (95 passed, 2 xfailed) |

---

## 🚀 Parcours Chronologique du Projet (Semaines 1 à 5)

### 📌 Semaine 1 : Cadrage Métier & Hygiène Logicielle (TP1)
- **Objectif :** Choisir l'approche technique adaptée pour 3 besoins métier et construire un dépôt reproductible.
- **Livrables :**
  - Fiches de cadrage argumentées selon la grille d'évaluation : [docs/cadrage/cas1-pharmacie.md](docs/cadrage/cas1-pharmacie.md) (*Règles métier*), [docs/cadrage/cas2-reglement.md](docs/cadrage/cas2-reglement.md) (*RAG*), et [docs/cadrage/cas3-avis-negatifs.md](docs/cadrage/cas3-avis-negatifs.md) (*Machine Learning*).
  - Politique stricte de versionnement Git via `.gitignore` (isolation totale de `.venv/` et des artefacts temporaires).
  - Contrôles T0 à T7 validés (38 tests passés au vert dès la première séance).

### 📌 Semaine 2 : Modèle de Sentiment, Entraînement & Évaluation (TP2)
- **Objectif :** Construire un pipeline scikit-learn reproductible (`TfidfVectorizer` + `LogisticRegression`), évaluer les performances et analyser la cause structurelle des erreurs.
- **Règles MLOps appliquées :**
  - Découpage stratifié `train_test_split` (80% / 20%) **avant** toute vectorisation pour bannir toute fuite de données (*data leakage*).
  - `models/metrics.json` est **versionné dans Git** (contrat de performance léger audité par la CI, tracé à $F_1 = 0{,}879$ sur le jeu démo conformément au pipeline CI, validé à $F_1 = 0{,}9205$ sur Allociné).
  - `models/sentiment.joblib` n'est **jamais versionné** (artefact binaire lourd exclu par le `.gitignore`, régénérable par commande).
- **Livrables :**
  - Modèle entraîné sur 20 000 avis Allociné : **$F_1$ Macro = 0,9205** (seuil exigé : 0,85).
  - Bilan d'analyse des erreurs sur les avis mitigés : [docs/semaine2.md](docs/semaine2.md).
  - 42 tests validés.

### 📌 Semaine 3 : Exposition du Modèle par une API REST FastAPI (TP3)
- **Objectif :** Exposer les capacités d'inférence du modèle derrière un service web standardisé.
- **Fonctionnalités :**
  - Endpoints REST : `GET /health` (état du service et modèle servi) et `POST /predict` (inférence avec probabilités).
  - Contrats Pydantic v2 stricts : rejet immédiat des requêtes invalides en code HTTP 422.
  - L'API charge le modèle une seule fois au démarrage (`lifespan`) et refuse de démarrer s'il manque.
- **Livrables :**
  - Code de l'API dans `api/` (`main.py`, `schemas.py`, `model.py`).
  - Suite de tests d'API automatisés (`tests/test_api.py`) : **51 tests passés**.
  - Bilan d'analyse d'API : [docs/semaine3.md](docs/semaine3.md).

### 📌 Semaine 4 : Tests Approfondis, Abstention & Qualité MLOps (TP4)
- **Objectif :** Identifier les angles morts du contrat d'entrée, introduire l'abstention et automatiser les garde-fous.
- **Réalisations :**
  - **Tests aux limites et de propriété (Hypothesis)** : validation des frontières (textes d'espaces, unicodes exotiques `\x85`).
  - **Mécanisme d'abstention opérationnel (`INDETERMINE`)** : seuil de confiance calibré à 60 % (`SEUIL_ABSTENTION = 0.60`).
  - **Jeu d'or annoté à la main** : 20 avis réels dans `data/jeu_or.csv` avec déclaration formelle des erreurs en `xfail(strict=True)`.
  - **Qualité statique & Couverture** : code vérifié par `ruff` et `mypy`, couverture de tests de l'API portée à **97,8 %**.
- **Livrables :**
  - Fichiers `tests/test_limites.py`, `tests/test_integration.py`, `tests/test_jeu_or.py`.
  - Bilan complet de qualité : [docs/semaine4.md](docs/semaine4.md).

### 📌 Semaine 5 : Interface Interactive Streamlit Découplée (TP5)
- **Objectif :** Rendre l'application accessible aux équipes métier via une interface web consommant exclusivement l'API.
- **Règles d'architecture respectées :**
  - L'interface n'importe **jamais** `sentiment.joblib` ni `predict()`. Elle délègue tout à `ui/client.py` par requêtes HTTP.
  - Gestion claire de l'abstention (« Je ne sais pas : à faire vérifier par un humain ») et des pannes de réseau.
  - Onglet d'analyse unitaire et onglet d'analyse par lot CSV avec téléchargement des résultats.
- **Livrables :**
  - Interface Streamlit dans `ui/` (`app.py`, `client.py`).
  - Tests unitaires et d'interface (`tests/test_client.py`, `tests/test_interface.py`).
  - Bilan d'interface : [docs/semaine5.md](docs/semaine5.md).
  - Suite de tests globale validée : **95 passed, 2 xfailed (97 tests au total)**.

---

## 📄 Les Documents Officiels & Journal de Bord

Tous les livrables d'évaluation demandés par l'enseignant sont déposés dans le dossier `docs/` :

1. **Journal de bord officiel (TP1 à TP5) :** [docs/journal-tp1-tp5.md](docs/journal-tp1-tp5.md)  
   *Traçabilité exhaustive commande par commande, difficultés résolues, répartition détaillée et bilans.*
2. **Compte Rendu Global Markdown :** [docs/compte-rendu.md](docs/compte-rendu.md)  
   *Synthèse scientifique des travaux, matrice de confusion et seuil d'incertitude.*
### 📌 Semaine 6 : Packaging & Distribution de l'Application (TP6)
- **Objectif :** Transformer l'application en un paquet Python installable, distribuable sous forme de roue wheel et manipulable via une CLI unifiée `sentiment`.
- **Fonctionnalités :**
  - Paquet `sentiment_app` installable via `pip install -e .` avec métadonnées configurées dans `pyproject.toml`.
  - Interface CLI Click : `sentiment --version`, `sentiment predict "<texte>"` et `sentiment serve`.
  - Intégration du seuil d'abstention (0.60) dans la commande console (`INDETERMINE` pour les entrées ambiguës).
  - Découplage du chemin du modèle via la variable d'environnement `SENTIMENT_MODELE` permettant l'exécution de la roue hors dépôt.
  - Suppression de l'insertion artisanale dans `sys.path` au sein de l'API.
- **Livrables :**
  - Paquet `sentiment_app/` (`cli.py`, `predict.py`, `__init__.py`).
  - Shim de compatibilité `src/predict.py`.
  - Fichier de compte rendu : [docs/semaine6.md](docs/semaine6.md).
  - Suite de tests de packaging (`tests/test_tp6.py`) : **97 tests réussis** (2 xfailed).

---

## 📚 Journaux de Bord & Comptes Rendus

1. **Journal de bord TP1 à TP6 (officiel) :**  
   - [journal-tp/journal-tp1-tp6 v-26-10-2026.md](journal-tp/journal-tp1-tp6%20v-26-10-2026.md)  
   - [docs/journal-tp1-tp6.md](docs/journal-tp1-tp6.md)
2. **Compte rendu synthétique :** [docs/compte-rendu.md](docs/compte-rendu.md)
3. **Bilans hebdomadaires :**  
   - [docs/semaine2.md](docs/semaine2.md) (Analyse des erreurs sac de mots)
   - [docs/semaine3.md](docs/semaine3.md) (Architecture d'exposition API)
   - [docs/semaine4.md](docs/semaine4.md) (Qualité statique, abstention et jeu d'or)
   - [docs/semaine5.md](docs/semaine5.md) (Interface découplée et gestion des pannes)
   - [docs/semaine6.md](docs/semaine6.md) (Packaging, CLI unifiée et roue isolée)

---

## 🔄 Intégration Continue (CI / CD)

Le dépôt intègre un pipeline automatisé via **GitHub Actions** ([.github/workflows/ci.yml](.github/workflows/ci.yml)) déclenché à chaque `push` et sur les tags `v*` :
1. **Vérification environnement :** validation par `scripts/check_setup.py`.
2. **Installation éditable :** `pip install -e .` pour lier le paquet `sentiment_app`.
3. **Entraînement automatique du modèle de test :** exécution reproductible de `make_demo.py` et `train.py`.
4. **Audit de qualité statique :** passage obligatoire de `ruff check .` et `mypy api`.
5. **Validation de couverture :** vérification que la couverture de tests dépasse **95%** (`--cov-fail-under=95`).
6. **Contrat MLOps :** validation du contrat de performance sur `models/metrics.json` ($F_1 \ge 0,85$).
7. **Roue installée hors du dépôt :** construction d'une wheel avec `python -m build --wheel`, installation dans un venv isolé éphémère et test de `sentiment --version`.

---

## 🛠️ Guide d'Exécution Locale Rapide

```bash
# 1. Cloner et installer l'environnement
git clone https://github.com/Amaranix/AI-DEV-DEP-Amrani_Ismail.git
cd AI-DEV-DEP-Amrani_Ismail
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
pip install -e .

# 2. Entraîner le modèle
python src/make_demo.py
python src/train.py

# 3. Lancer l'ensemble des tests automatisés
pytest -q

# 4. Utiliser la commande CLI sentiment
sentiment --version
sentiment predict "Livraison rapide, produit conforme, très satisfait"

# 5. Lancer l'API FastAPI
sentiment serve
# ou directement : uvicorn api.main:app --reload

# 6. Lancer l'interface Streamlit
streamlit run ui/app.py
```
