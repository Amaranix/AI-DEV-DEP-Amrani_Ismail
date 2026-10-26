# Semaine 5 : L'interface Streamlit, notes du binôme

**Module :** Développement et déploiement d'applications intelligentes  
**Binôme :** Lamzouri Ishak (`@inazuma2004`) & Amrani Ismail (`@Amaranix`)  
**Date :** Octobre 2026  

---

## 1. Pourquoi l'interface n'importe-t-elle jamais `predict()` ni le fichier `.joblib` ?

L'interface Streamlit agit en pur **client HTTP** découplé du modèle. En s'interdisant d'importer directement `predict()` ou `models/sentiment.joblib`, nous respectons la règle fondamentale d'architecture logicielle : **la séparation stricte des responsabilités**.
- Le modèle de Machine Learning et sa logique d'inférence s'exécutent au sein du service backend dédié (FastAPI, port 8000).
- L'interface frontend (Streamlit, port 8501) ne gère que la présentation et la restitution utilisateur.
- **Bénéfice opérationnel immédiat** : Si le modèle est réentraîné, mis à jour (nouvelle version, passage à un LLM) ou même déporté sur une machine cloud distante, l'interface graphique continue de fonctionner sans modifier une seule ligne de son code source.

---

## 2. Que montre l'interface quand le modèle hésite, et pourquoi est-ce mieux qu'un verdict forcé ?

Quand la confiance du modèle tombe sous le seuil d'abstention opérationnel (`SEUIL_ABSTENTION = 0.60`), l'API répond avec le label `INDETERMINE`. L'interface affiche alors :
- Le verdict explicite : **« Je ne sais pas : à faire vérifier par un humain »** accompagné du score de confiance réel (ex: 52 %).
- Un encadré informatif bleu (`st.info`) précisant que le score est sous le seuil d'abstention et requiert un arbitrage humain.

**Pourquoi est-ce supérieur à un verdict forcé ?**  
Un verdict forcé à 51 % donne à l'utilisateur non technique une fausse illusion de certitude. Dans le cas d'avis clients mécontents ou ambigus, une mauvaise classification automatique peut retarder la prise en charge d'un litige grave. En formalisant l'incertitude (*Human-in-the-loop*), l'entreprise sécurise sa relation client et n'automatise que ce dont elle est mathématiquement sûre.

---

## 3. Que voit l'utilisateur quand l'API tombe ? Et le fichier `data/avis_exemple.csv` : combien d'avis partent vers un humain ?

- **Quand l'API est arrêtée ou injoignable :**
  Dès l'ouverture ou le rechargement de la page, `client.sante()` détecte la rupture de connexion HTTP (`ConnectError`). L'interface affiche un message d'erreur rouge clair :
  `🚨 API injoignable : lancez d'abord uvicorn api.main:app`
  Si l'utilisateur tente d'analyser un avis alors que l'API vient d'être coupée, un avertissement explicite indique l'impossibilité de joindre le service, sans faire crasher l'application Streamlit.

- **Traitement du fichier `data/avis_exemple.csv` :**
  Le lot d'exemples contient 6 avis. L'analyse par lot renvoie le résumé :
  `{'INDETERMINE': 1, 'NEGATIVE': 2, 'POSITIVE': 3}`
  Sur les 6 avis, **1 avis part vers un humain** (l'avis inventé *"xqzvb wlkptr grombu"*, score 51,6 %), tandis que les 5 autres (3 positifs, 2 négatifs) sont immédiatement qualifiés et téléchargeables au format CSV (`resultats.csv`).
