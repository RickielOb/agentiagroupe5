# Agent IA professeur de réseaux

## Projet
Introduction à l'IA – LP_ASUR, INPTIC Gabon, année 2025–2026.
Enseignant : Dr Axel MENGARA.

## Groupe 5
- Chef de groupe : OBIANG ASSOUME Michel Rickiel
- Membres : ABDOULAYI MBA Yaya, AGAYA AUBIN Michel Ange Elie, EKORE MINANG Priva,
  MACKAGA MACKAGA Lucas Verlain, MATSIENGUI Urielle Rolain, MEGA NZE Guy Oscar,
  MINKOUE ONDO, NDONG TOUNDA Marc Freddy, OBIANG Franck Dilane

## Objectif
Un professeur virtuel qui permet à un étudiant d'apprendre les réseaux
informatiques, de demander des explications et de tester ses connaissances.

## API et modèle
Google Gemini via la bibliothèque `google-genai`.
Modèle par défaut : `gemini-3.8-flash` (modifiable avec `GEMINI_MODEL` dans `.env`).

## Fonctionnalités
- 10 sujets : OSI, TCP/IP, IPv4, DHCP, DNS, routeur, switch, TCP/UDP, LAN/WAN, subnetting
- 4 modes : Expliquer, Donner un exemple, Créer un quiz, Tester mes connaissances
- 2 niveaux : Débutant, Intermédiaire
- Quiz interactif : une question à la fois, correction immédiate, score final
- Historique de conversation (questions de suivi sans perdre le contexte)
- Gestion des erreurs (clé absente, message vide, erreur API, réponse vide)

## Architecture
Utilisateur → Interface Streamlit (`app.py`) → Logique d'appel (`agent.py`)
→ Prompt système + historique (`prompts.py`) → API Gemini → Réponse affichée.

## Bibliothèques
streamlit, google-genai, python-dotenv

## Installation
```bash
pip install -r requirements.txt
```
Créer un fichier `.env` (voir `.env.example`) :
```
GEMINI_API_KEY=votre_cle
```

## Lancement
```bash
streamlit run app.py
```

## Tests réalisés
Voir `TESTS.md`.

## Limites connues
- Les réponses dépendent du modèle et peuvent contenir des erreurs (notamment en calcul de sous-réseaux).
- Le quiz n'a pas de score calculé par le code : le score est donné par l'IA.
- Nécessite une connexion Internet et une clé API valide (quotas limités en version gratuite).
