# Fiche de cadrage : Ordonnances incomplètes en pharmacie

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Détecter automatiquement si une ordonnance médicale transmise à la pharmacie contient tous les champs obligatoires et mentions légales avant sa délivrance.

## Utilisateur final (obligatoire)

Les préparateurs et pharmaciens d'officine au comptoir lors de la réception ou de la numérisation des ordonnances.

## Approche retenue (obligatoire)

Cocher une seule case :

- [x] Règles métier
- [ ] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

(a) Il n'existe pas au départ de base d'ordonnances étiquetées et la réglementation définit déjà précisément la liste exhaustive des mentions obligatoires (posologie, identification du prescripteur, signature, date). (b) La vérification doit être 100 % explicable et auditable : chaque champ manquant doit pouvoir être explicitement pointé et vérifié par le pharmacien. (d) La conséquence d'une erreur est critique car délivrer un médicament sur une fausse ou mauvaise ordonnance engage la responsabilité pénale et met en danger la santé du patient ; une validation humaine finale reste donc obligatoire.

## Données nécessaires et leur origine (obligatoire)

Champs textuels extraits des ordonnances (formulaire de saisie ou OCR) et référentiel réglementaire officiel des mentions obligatoires de prescription.

## Métrique de succès et seuil d'acceptation (obligatoire)

Taux de conformité des détections avec un rappel de 100 % sur les champs critiques légaux sur un jeu d'évaluation de 100 ordonnances tests.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Une fausse validation risquerait la délivrance d'un traitement inadapté ou non couvert ; le pharmacien valide toujours obligatoirement l'ordonnance à l'écran avant distribution.

## Risques éthiques ou de confidentialité (obligatoire)

Données médicales et de santé hautement sensibles protégées par le secret médical ; aucun envoi vers des API tierces externes et anonymisation stricte lors de tout stockage local.

## Approche écartée et pourquoi (facultatif)

Machine learning ou modèle génératif écartés car ils introduisent un risque d'hallucination ou d'imprécision inacceptable pour un contrôle réglementaire strict et déterministe.
