"""Prompts et listes de choix de l'agent « Professeur de réseaux »."""

TOPICS = [
    "Modèle OSI", "TCP/IP", "IPv4", "DHCP", "DNS",
    "Routeur", "Switch", "TCP vs UDP", "LAN vs WAN", "Subnetting",
]

MODES = [
    "Expliquer",
    "Donner un exemple",
    "Créer un quiz",
    "Tester mes connaissances",
]

LEVELS = ["Débutant", "Intermédiaire"]

SYSTEM_PROMPT = """Tu es un professeur de réseaux informatiques.
Tes utilisateurs sont des étudiants en Licence. Réponds en français.

Tu dois :
- utiliser un langage simple ;
- expliquer progressivement ;
- définir les termes techniques dès leur première utilisation ;
- donner des exemples concrets ;
- adapter la difficulté au niveau (Débutant ou Intermédiaire) ;
- vérifier la compréhension en posant parfois une courte question à la fin.

Sujets couverts : modèle OSI, TCP/IP, IPv4, DHCP, DNS, routeur, switch,
TCP et UDP, LAN et WAN, subnetting.
Si la question sort clairement des réseaux informatiques, indique-le
poliment et ramène l'étudiant vers un sujet réseau.

Mode « Expliquer » :
- explique le sujet avec des mots simples, puis termine par un exemple concret.

Mode « Donner un exemple » :
- donne un exemple concret et réaliste, commenté étape par étape.

Mode « Créer un quiz » :
- le quiz comporte 5 questions à choix multiples (A, B, C, D) ;
- pose UNE SEULE question à la fois, au format « Question 1/5 » ;
- n'écris jamais la réponse avant que l'étudiant ait répondu ;
- attends la réponse, indique si elle est correcte, explique la correction ;
- pose ensuite la question suivante ;
- après la question 5, donne le score sur 5 et un conseil de révision.

Mode « Tester mes connaissances » :
- session de 5 questions de difficulté progressive, mélangeant QCM et
  questions courtes ;
- même fonctionnement : une question à la fois, correction, puis suite ;
- à la fin, donne le score sur 5 et les points à revoir.

Règles de sécurité :
- ne demande jamais de mot de passe ni de clé secrète ;
- n'invente pas d'informations ; si tu n'es pas certain, dis-le clairement ;
- pour les calculs (subnetting), détaille les étapes et vérifie ton résultat.
"""


TOPIC_SUGGESTIONS = {
    "Modèle OSI": [
        "Pourquoi y a-t-il 7 couches dans le modèle OSI ?",
        "Quelle est la différence entre la couche 2 et la couche 3 ?",
        "Explique-moi le principe d'encapsulation avec un exemple",
    ],
    "TCP/IP": [
        "Quelle est la différence entre le modèle OSI et TCP/IP ?",
        "Quels sont les 4 niveaux du modèle TCP/IP ?",
        "À quoi sert la couche Internet dans TCP/IP ?",
    ],
    "IPv4": [
        "À quoi sert le masque de sous-réseau ?",
        "Quelle est la différence entre IP publique et IP privée ?",
        "C'est quoi une adresse de broadcast ?",
    ],
    "DHCP": [
        "Pourquoi a-t-on besoin d'une adresse IP automatique ?",
        "Explique-moi le processus DORA étape par étape",
        "Quelle est la différence avec une IP statique ?",
    ],
    "DNS": [
        "Comment un nom de domaine est-il traduit en IP ?",
        "C'est quoi un enregistrement DNS de type A et CNAME ?",
        "Que se passe-t-il quand le serveur DNS met en cache une réponse ?",
    ],
    "Routeur": [
        "Quelle est la différence fondamentale entre un routeur et un switch ?",
        "Comment fonctionne une table de routage ?",
        "C'est quoi une passerelle par défaut (default gateway) ?",
    ],
    "Switch": [
        "À quoi sert la table d'adresses MAC dans un switch ?",
        "Pourquoi un switch évite-t-il les collisions ?",
        "Qu'est-ce qu'un domaine de diffusion (broadcast domain) ?",
    ],
    "TCP vs UDP": [
        "Pourquoi le streaming ou le jeu vidéo utilise-t-il souvent UDP ?",
        "Comment fonctionne la poignée de main (Three-Way Handshake) de TCP ?",
        "Pourquoi dit-on que TCP est orienté connexion et UDP non connecté ?",
    ],
    "LAN vs WAN": [
        "Quelle est la différence de portée entre un LAN et un WAN ?",
        "Quels équipements relient un réseau local à Internet ?",
        "Qu'est-ce qu'un MAN par rapport à un LAN et un WAN ?",
    ],
    "Subnetting": [
        "Comment calculer le nombre d'hôtes utilisables avec un masque /26 ?",
        "Explique-moi la méthode du « nombre magique » pour trouver les sous-réseaux",
        "Pourquoi découpe-t-on un réseau IP en sous-réseaux ?",
    ],
}


def build_user_prompt(topic: str, mode: str, level: str) -> str:
    """Construit le message utilisateur à partir du formulaire."""
    return (
        f"Sujet : {topic}\n"
        f"Mode : {mode}\n"
        f"Niveau : {level}\n\n"
        "Adapte ta réponse au sujet, au mode et au niveau de l'étudiant."
    )
