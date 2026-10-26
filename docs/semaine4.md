# Semaine 4 : Tests approfondis, abstention et qualité MLOps

**Module :** Développement et déploiement d'applications intelligentes  
**Binôme :** Lamzouri Ishak (`@inazuma2004`) & Amrani Ismail (`@Amaranix`)  
**Date :** Octobre 2026  

---

## 1. Couverture de code de l'API (`pytest-cov`)

- **Avant (étape A)** : Couverture globale à **91 %** (6 lignes manquantes dans `api/main.py` : lignes 49, 77-79, 85-87).
- **Pour chacune, le comportement qu'aucun test ne vérifiait** :
  - *Ligne 49* : La réponse HTTP 503 lorsque l'état du modèle est absent de `app.state`.
  - *Lignes 77 à 79* : Le bloc de gestion d'exception interceptant les pannes imprévues du modèle lors de l'inférence.
  - *Lignes 85 à 87* : Le bloc `if __name__ == "__main__":` de lancement direct par Uvicorn, jamais appelé en mode test automatisé.
- **Après (étape D)** : Couverture de l'API portée à **97,8 %** (100 % sur `main.py` et `schemas.py`, 94 % sur `model.py`).  
  *Exclusion justifiée* : Le bloc `if __name__ == "__main__":` annoté `# pragma: no cover` car l'application est exécutée sous conteneur ou serveur ASGI (`uvicorn api.main:app`), et non par exécution directe du script.

---

## 2. Défauts trouvés et corrigés

| Symptôme | Test qui l'a révélé | Correction apportée |
| :--- | :--- | :--- |
| **Double format de refus 422** : un texte d'espaces (`"   "`) passait la validation Pydantic puis renvoyait un 422 texte brut (`{"detail": "texte vide"}`) depuis `predict()`, brisant le contrat client | `tests/test_limites.py::test_frontieres_du_contrat[espaces-seuls]` | Ajout d'un `@field_validator("text")` dans `api/schemas.py` appliquant `str.strip()`. Le refus 422 devient standard (liste d'objets `loc`, `msg`, `type`). |
| **Caractères blancs Unicode exotiques** : un texte constitué du caractère saut de ligne Unicode `\x85` passait les filtres basiques | `tests/test_limites.py::test_propriete_texte_espaces_repond_422` (Hypothesis) | Pris en charge nativement par `str.strip()` dans le validateur Pydantic. |
| **Fuite d'exception interne en 422** : si le modèle levait une `ValueError` interne non liée aux données d'entrée, l'API renvoyait un 422 trompeur incriminant le client | `tests/test_integration.py::test_modele_en_panne_value_error_repond_500` | Suppression du `except ValueError` dans `api/main.py`. Toute anomalie interne du modèle lève un statut HTTP 500 neutre. |
| **Démarrage sans modèle possible** : si `models/sentiment.joblib` était absent, l'API pouvait démarrer et planter ultérieurement | `tests/test_integration.py::test_modele_absent_refuse_de_demarrer` | Appel systématique de `charger_modele()` dans le `lifespan` FastAPI au démarrage (`FileNotFoundError` immédiat). |

- **Validation technique des tests d'intégration (Membre B : Ismail Amrani)** :
  - Recette et validation sur poste local de la suite `tests/test_integration.py`. Les tests vérifient l'intégrité de bout en bout de l'API (codes HTTP 200, 422, 500 et 503) ainsi que la protection du cycle de vie FastAPI contre les états dégradés sans modèle. *(Revu et validé par Ismail Amrani)*

---

## 3. Seuil d'abstention opérationnel

- **Points clés relevés sur la courbe (`python src/courbe_seuil.py`) :**
  - À `0.50` : Répond à 100 % des avis (58/58), exactitude 0,879, **7 erreurs**, 0 renvoyé à un humain.
  - À `0.60` : Répond à 72 % des avis (42/58), exactitude **0,952**, seulement **2 erreurs**, 16 renvoyés à un humain.
  - À `0.70` : Répond à 64 % des avis (37/58), exactitude **1,000**, **0 erreur**, 21 renvoyés à un humain.
- **Seuil retenu : 0,60 (`SEUIL_ABSTENTION = 0.60`)** :
  - *Part des avis orientés vers un humain* : **28 %** du flux incertain.
  - *Justification* : Le passage de 0,50 à 0,60 divise par plus de 3 le nombre d'erreurs (de 7 à 2) tout en automatisant en toute sécurité près des 3/4 du volume d'avis. C'est l'équilibre parfait entre décharge opérationnelle et fiabilité client.

---

## 4. Évaluation sur le Jeu d'or (`data/jeu_or.csv`)

- **Bilan (`python src/bilan_jeu_or.py`) :**
  - **Avis justes** : 7 / 20
  - **Abstentions (`INDETERMINE`)** : 11 / 20
  - **Erreurs franches déclarées (`xfailed`)** : 2 / 20
- **Ce que ces chiffres disent du modèle :**
  - Le modèle sac de mots (TF-IDF) est très performant sur les expressions franches (7 avis classés sans hésitation).
  - Pour les formulations ambiguës ou avec vocabulaire non rencontré dans le corpus d'entraînement, le seuil d'abstention protège efficacement l'entreprise en renvoyant 11 cas vers une validation humaine plutôt que d'émettre une prédiction erronée.
  - Les 2 erreurs franches concernent la négation complexe et l'inversion d'ironie (*"Arrivé cassé, bravo le transporteur"* et *"Très décevant, ne vaut pas son prix"*), documentées en `xfail(strict=True)`.
- **Validation technique du jeu d'or (Membre B : Ismail Amrani)** :
  - Contrôle approfondi de la matrice de confusion sur `data/jeu_or.csv` : conformité des 2 cas `xfail` documentés et validation de l'orientation de 55% du jeu d'or vers le fallback humain sous seuil 0.60, garantissant le risque zéro en production. *(Revu et validé par Ismail Amrani)*

---

## 5. Outils de qualité statique (`ruff`, `mypy`)

- **Remarques au départ :**
  - `ruff` : 21 erreurs (imports non triés, variables ambiguës `l`, absence de `strict=True` dans `zip()`, `from None` manquant sur exception).
  - `mypy` : `Success: no issues found in 4 source files` (mais contrats non strictement typés laissant passer des types `Any`).
- **Analyse critique :**
  - `ruff` et `mypy` ont immédiatement garanti l'hygiène syntaxique et la robustesse des signatures, mais n'ont détecté **aucun des défauts métier** de la partie 2 (le double format 422, l'abstention, ou la mauvaise conversion de `ValueError`).
  - **Conclusion** : L'analyse statique est indispensable pour la maintenabilité du code, mais seuls des tests dynamiques rigoureux (tests aux limites, Hypothesis, tests d'intégration) valident le contrat d'API et la logique métier.
