# Bilan Semaine 2 : Modèle de Sentiment, Évaluation et Analyse des Erreurs

**Module :** Développement et déploiement d'applications intelligentes  
**Auteurs :** Lamzouri Ishak (`@inazuma2004`) & Amrani Ismail (`@Amaranix`)  
**Fichiers associés :** `src/train.py`, `src/evaluate.py`, `src/predict.py`, `models/metrics.json`

---

## 1. Contexte & Démarche de Modélisation

En semaine 2, l'objectif est d'entraîner, d'évaluer et de sauvegarder un modèle d'analyse de sentiment dans un cadre rigoureux de MLOps et d'ingénierie logicielle :

### Pipeline scikit-learn unifié :
Le modèle est encapsulé dans un `Pipeline` combinant :
- **Vectorisation TF-IDF (`TfidfVectorizer`) :** Extraction d'unigrammes et bigrammes (`ngram_range=(1, 2)`), seuil de fréquence minimale (`min_df=2`) et mise à l'échelle sous-linéaire (`sublinear_tf=True`).
- **Régression Logistique (`LogisticRegression`) :** Modèle linéaire régularisé avec équilibrage des classes (`class_weight="balanced"`), 1000 itérations et graine pseudo-aléatoire fixée (`random_state=42`).

### Règle méthodologique anti-fuite (Data Leakage) :
Le découpage en jeu d'entraînement et jeu de test (`train_test_split`, 80 % / 20 %, stratifié) est exécuté **strictement avant** la vectorisation TF-IDF. Vectoriser le corpus complet avant le split introduirait une fuite d'information où le vocabulaire et les fréquences inverses de documents (IDF) du test influenceraient l'apprentissage, faussant la réalité des métriques.

---

## 2. Résultats Expérimentaux Comparés

Deux jeux de données ont été évalués avec le pipeline :

| Caractéristique | Jeu de Démonstration (`demo_reviews.csv`) | Jeu de Production (Allociné) |
| :--- | :---: | :---: |
| **Nombre total d'avis** | 290 avis | 20 000 avis |
| **Taille du vocabulaire TF-IDF** | 316 termes | 149 529 termes |
| **Échantillon de test** | 58 avis | 4 000 avis |
| **F1 Macro** | **0,879** | **0,9205** (seuil requis : 0,85) |
| **Exactitude (*Accuracy*)** | 87,9 % | **92,05 %** |
| **Rappel classe Négative** | 93,1 % | **91,13 %** |

---

## 3. Matrice de Confusion & Typologie des Erreurs

Sur le jeu Allociné (4 000 avis de test) :
```text
                 Prédiction :
                 negative    positive
Vérité: negative     1860         181   (Rappel négatif = 91,1%)
        positive      137        1822   (Rappel positif = 93,0%)
```

Sur 4 000 avis, 318 erreurs apparaissent (181 faux positifs et 137 faux négatifs).

---

## 4. Analyse Technique du Mécanisme des Erreurs

L'inspection détaillée des prédictions erronées démontre que les échecs ne sont pas aléatoires : ils portent quasi-exclusivement sur les **avis mitigés avec retournements de phrase**.

### Pourquoi le modèle se trompe-t-il sur ces cas ?
1. **Absence d'ordre dans le sac de mots (*Bag of Words*) :**  
   La vectorisation TF-IDF compte les fréquences de termes sans conserver l'agencement temporel ni la hiérarchie syntaxique des propositions.
2. **Structure discursive bipartite des avis clients :**  
   Un client commence souvent par formuler un grief avant de conclure sur une note très positive, ou inversement (*« X au début, mais finalement Y »*). La véritable intention de l'utilisateur réside dans la proposition finale (introduite par *« mais »*, *« cependant »*, *« en revanche »*).  
   Or, le modèle linéaire additionne aveuglément les coefficients de chaque mot : si la première partie comporte trop de termes forts (ex. *« cassé »*, *« refusé »*, *« retour payant »*), leur poids cumulé dépasse celui des termes positifs finals, même si l'avis conclut par *« très satisfait »*.

### Exemple direct tiré de nos données d'évaluation :
> **Texte :** `Taille trop petite et retour payant au déballage, sauf que ensuite produit conforme à la description, très satisfait.`  
> **Vérité :** `positive` | **Prédit :** `negative`  
> **Explication :** La densité de mots négatifs au début (*« trop petite »*, *« retour payant »*) biaise le score total, masquant la satisfaction réelle exprimée à la fin (*« très satisfait »*).

---

## 5. Perspectives de Résolution en Milieu Industriel

Pour surmonter cette faiblesse structurelle du TF-IDF :
1. **Passage aux Transformers contextuels :** Utiliser un modèle de langage pré-entraîné tel que `CamemBERT` ou des architectures bi-encodeurs (*Sentence-Transformers*) capables de capturer l'attention bidirectionnelle et le rôle pivot des conjonctions d'opposition.
2. **Pourquoi ce n'était pas l'objectif immédiat :** Un modèle TF-IDF linéaire s'entraîne en quelques secondes, ne nécessite aucun GPU, s'exécute en < 1 ms sur CPU en production et permet d'illustrer parfaitement l'intérêt de la gestion d'incertitude traitée au TP3.
