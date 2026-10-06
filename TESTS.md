# Scénarios de test

À exécuter dans l'application, puis compléter la colonne « Statut ».

| N° | Entrée | Résultat attendu | Statut |
|----|--------|------------------|--------|
| 1 | Sujet : Modèle OSI, Mode : Expliquer, Niveau : Débutant | Explication simple des 7 couches, avec un exemple concret | Réussi / Échoué |
| 2 | Sujet : TCP vs UDP, Mode : Expliquer, Niveau : Intermédiaire | Comparaison claire (fiabilité, vitesse, usages) | Réussi / Échoué |
| 3 | Sujet : DNS, Mode : Donner un exemple | Exemple de résolution d'un nom de domaine, étape par étape | Réussi / Échoué |
| 4 | Sujet : IPv4, Mode : Créer un quiz | Une seule question QCM « Question 1/5 », sans la réponse | Réussi / Échoué |
| 5 | Session complète de 5 questions (Tester mes connaissances) | Correction après chaque réponse, score /5 à la fin | Réussi / Échoué |
| 6 | Question de suivi : « Peux-tu réexpliquer plus simplement ? » | L'agent tient compte du contexte précédent | Réussi / Échoué |
| 7 | Retirer la clé du .env | Message d'erreur « Clé API absente » | Réussi / Échoué |
| 8 | Envoyer un message vide dans le chat | Aucun appel API (message vide ignoré) | Réussi / Échoué |
