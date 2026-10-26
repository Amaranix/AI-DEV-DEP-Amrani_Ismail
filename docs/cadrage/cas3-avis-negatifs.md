# Fiche de cadrage : Priorisation des avis négatifs

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Détecter et prioriser automatiquement les avis clients négatifs sur une plateforme e-commerce afin de traiter rapidement les insatisfactions critiques.

## Utilisateur final (obligatoire)

L'équipe du service client et les gestionnaires de l'expérience client de la plateforme e-commerce.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [x] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

(a) Des milliers d'avis clients avec leurs notes en étoiles associées sont déjà archivés et utilisables directement comme données étiquetées d'entraînement. (c) Le flux compte des milliers d'avis par jour : un classifieur de machine learning léger (Scikit-Learn/TF-IDF) a un coût d'inférence quasi nul comparé à des appels récurrents à un LLM. (d) La conséquence d'une mauvaise classification est modérée car l'avis reste consultable dans la file générale et les agents du support réajustent facilement les priorités.

## Données nécessaires et leur origine (obligatoire)

Base historique des avis clients du site e-commerce comprenant le texte du commentaire, la note de 1 à 5 étoiles et la date de publication.

## Métrique de succès et seuil d'acceptation (obligatoire)

Rappel supérieur à 0,90 sur la classe « négatif » avec un score F1 macro minimal de 0,85 sur le jeu de test pour ne manquer aucune réclamation critique.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Un avis négatif mal étiqueté sera traité avec un léger retard mais reste visible ; l'équipe support dispose d'un bouton de requalification alimentant les réentraînements continus.

## Risques éthiques ou de confidentialité (obligatoire)

Présence potentielle d'informations personnelles (noms, téléphones) dans les textes d'avis nécessitant une anonymisation préalable avant tout apprentissage.

## Approche écartée et pourquoi (facultatif)

Règles métier par mots-clés écartées car elles échouent face au sarcasme, aux fautes d'orthographe et à la diversité des formulations mécontentes des clients.
