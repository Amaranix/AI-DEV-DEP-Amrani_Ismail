# Fiche de cadrage : Questions sur le règlement intérieur

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Répondre précisément aux questions des étudiants et du personnel sur le règlement intérieur de l'école en citant systématiquement les articles officiels applicables.

## Utilisateur final (obligatoire)

Les étudiants, les enseignants et le personnel administratif de l'établissement d'enseignement.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [ ] Machine learning
- [x] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

(a) Il n'existe pas d'historique de questions/réponses étiquetées, mais les règlements intérieurs et chartes existent déjà sous forme documentaire. (b) La réponse doit être impérativement vérifiable en citant le numéro précis de l'article officiel pour éviter toute contestation. (c) Le volume est modéré (quelques dizaines de questions par jour), ce qui rend le coût par requête d'un système RAG tout à fait négligeable pour l'école.

## Données nécessaires et leur origine (obligatoire)

Documents officiels PDF ou Markdown du règlement des études, charte informatique, règlement intérieur et calendrier universitaire publiés par la direction.

## Métrique de succès et seuil d'acceptation (obligatoire)

Taux de réponses correctes avec citation exacte des articles d'au moins 90 % évalué sur un banc de 30 questions de référence.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Une information erronée peut induire un étudiant en erreur sur une absence ou un examen ; un lien vers le document source officiel et un contact vers la scolarité accompagnent chaque réponse.

## Risques éthiques ou de confidentialité (obligatoire)

Risque d'injection dans les questions ou de divulgation de données personnelles ; les questions sont filtrées et aucune donnée nominative n'est envoyée ni conservée.

## Approche écartée et pourquoi (facultatif)

Modèle génératif seul écarté car il risque d'halluciner des articles de loi ou des règles inexistantes qui pénaliseraient injustement les étudiants.
