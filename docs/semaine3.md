# Semaine 3 : l'API, notes du binôme

> Deux questions, quelques phrases chacune. Répondez avec ce que vous avez observé, pas avec le cours.

## 1. Pourquoi l'API refuse-t-elle de démarrer sans `models/sentiment.joblib`, plutôt que de démarrer et de répondre 503 ?

### Ce que nous avons observé lors des tests et des manipulations (T20) :
- Dans `src/predict.py` (fonction `charger_modele()`), si `models/sentiment.joblib` est manquant, le code lève explicitement :
  ```python
  raise FileNotFoundError("models/sentiment.joblib absent : lancez python src/train.py")
  ```
- Dans `api/main.py`, l'initialisation du modèle s'effectue dans le gestionnaire de cycle de vie (`@asynccontextmanager async def lifespan(app)`). L'exception `FileNotFoundError` est donc levée avant que le serveur HTTP ne commence à écouter les requêtes. Le serveur Uvicorn crashe immédiatement et interrompt le processus.
- À l'inverse, dans `tests/test_integration.py::test_modele_non_charge_repond_503`, le statut 503 n'intervient que si l'API est déjà en cours d'exécution mais que `app.state.classifier` est `None` (indisponibilité en mémoire, renvoyant `{"detail": "Modèle non chargé"}`).

### Pourquoi le refus de démarrer est le bon choix technique :
1. **Signal immédiat d'échec de déploiement (Fail Fast) :** Si l'API démarrait sans modèle en renvoyant 503, les sondes de disponibilité (`healthchecks`) pourraient maintenir le conteneur en ligne et lui envoyer du trafic qui échouerait systématiquement. En crashant au démarrage, le système hôte ou l'orchestrateur détecte immédiatement que l'artéfact requis est manquant.
2. **Sémantique du code HTTP 503 :** Le statut 503 (*Service Unavailable*) est réservé à une indisponibilité **temporaire** (ex. pic de charge ou redémarrage à chaud). L'absence de fichier `.joblib` sur le disque est un problème permanent de configuration qui ne se résoudra jamais sans lancer l'entraînement (`python src/train.py`).

---

## 2. Un texte vide est refusé deux fois : par Pydantic, puis par `predict()`. Est-ce redondant ?

### Ce que nous avons observé lors des tests (T18) :
- **Au niveau HTTP (Pydantic / FastAPI dans `api/schemas.py`) :**
  - Si l'on envoie une chaîne vide `{"text": ""}`, le champ `Field(..., min_length=1)` rejette la requête avec l'erreur `string_too_short` :
    ```json
    {"type": "string_too_short", "loc": ["body", "text"], "msg": "String should have at least 1 character"}
    ```
  - Si l'on envoie des espaces seuls `{"text": "   "}`, le validateur `@field_validator("text")` applique `v.strip()` et lève `ValueError("texte vide")`, produisant un refus HTTP 422 avec l'erreur `value_error` :
    ```json
    {"type": "value_error", "loc": ["body", "text"], "msg": "Value error, texte vide"}
    ```
- **Au niveau de la bibliothèque métier (`src/predict.py`) :**
  La fonction pure `predict(texte)` vérifie de manière autonome :
  ```python
  if not isinstance(texte, str) or not texte.strip():
      raise ValueError("texte vide")
  ```

### Pourquoi cette double vérification est nécessaire :
Cette double vérification n'est pas une redondance inutile, mais l'application rigoureuse du principe de **défense en profondeur** et du **découplage logiciel** :
1. **Autonomie et réutilisabilité de `src/predict.py` :** Ce module a été conçu au TP2 pour fonctionner de façon autonome. S'il est importé directement dans un script de traitement par lot, un notebook ou un script CLI sans passer par l'API web, il doit garantir ses propres invariants et refuser les entrées invalides sans dépendre de Pydantic.
2. **Protection de la frontière d'entrée (API Gateway) :** Pydantic filtre les requêtes réseau dès la couche HTTP, avant tout appel au modèle scikit-learn. Cela évite d'engager des ressources d'inférence inutiles et garantit un format d'erreur normalisé (JSON structuré avec code HTTP 422) pour les clients de l'API.
