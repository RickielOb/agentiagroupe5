"""Interface Streamlit professionnelle « NETLAB — Parcours réseaux ».

Plateforme d'apprentissage interactif pour les réseaux informatiques (LP_ASUR, INPTIC Gabon).
Typographie éditoriale : Source Serif 4, IBM Plex Sans, IBM Plex Mono.
"""
import os
import streamlit as st

from agent import EmptyResponseError, MissingApiKeyError, ask_agent
from prompts import (
    LEVELS,
    MODES,
    SYSTEM_PROMPT,
    TOPIC_SUGGESTIONS,
    TOPICS,
    build_user_prompt,
)

# -----------------------------------------------------------------------------
# CONFIGURATION DE LA PAGE & ASSETS
# -----------------------------------------------------------------------------
LOGO_PATH = "assets/logo.png"
AVATAR_PATH = "assets/logo.png"

st.set_page_config(
    page_title="NETLAB — Parcours réseaux",
    page_icon=LOGO_PATH if os.path.exists(LOGO_PATH) else "⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialisation de la mémoire et de l'état du thème
if "messages" not in st.session_state:
    st.session_state.messages = []

if "topics_visited" not in st.session_state:
    st.session_state.topics_visited = set()

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False


def get_image_base64(path: str) -> str:
    """Retourne l'image en base64 pour l'intégration HTML fluide."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            import base64
            return base64.b64encode(f.read()).decode()
    return ""

LOGO_B64 = get_image_base64(LOGO_PATH)


# -----------------------------------------------------------------------------
# GESTION DU SYSTÈME DE VARIABLES (THÈMES & TYPOGRAPHIE)
# -----------------------------------------------------------------------------
def inject_theme(is_dark: bool) -> None:
    """Injecte la feuille de style avec les variables CSS et les polices."""
    if is_dark:
        theme_vars = """
        :root {
            --font-serif: 'Source Serif 4', Georgia, serif;
            --font-sans: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-mono: 'IBM Plex Mono', 'SF Mono', Consolas, monospace;
            --bg-app: #0B0F19;
            --bg-surface: #111827;
            --bg-sidebar: #0F172A;
            --bg-input: #1E293B;
            --border-color: #1E293B;
            --border-input: #334155;
            --text-primary: #F8FAFC;
            --text-secondary: #94A3B8;
            --bg-hover: #1E293B;
            --bg-option-selected: #1E3A8A;
            --chat-bottom-bg: rgba(11, 15, 25, 0.95);
            --user-bubble-bg: #1E293B;
            --user-bubble-border: #2563EB;
            --user-bubble-text: #F8FAFC;
        }
        """
    else:
        theme_vars = """
        :root {
            --font-serif: 'Source Serif 4', Georgia, serif;
            --font-sans: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-mono: 'IBM Plex Mono', 'SF Mono', Consolas, monospace;
            --bg-app: #F7F8FA;
            --bg-surface: #FFFFFF;
            --bg-sidebar: #FFFFFF;
            --bg-input: #FFFFFF;
            --border-color: #E2E8F0;
            --border-input: #CBD5E1;
            --text-primary: #0F172A;
            --text-secondary: #64748B;
            --bg-hover: #F1F5F9;
            --bg-option-selected: #EFF6FF;
            --chat-bottom-bg: rgba(247, 248, 250, 0.95);
            --user-bubble-bg: #EFF6FF;
            --user-bubble-border: #DBEAFE;
            --user-bubble-text: #1E3A8A;
        }
        """

    css_content = ""
    if os.path.exists("styles.css"):
        with open("styles.css", "r", encoding="utf-8") as f:
            css_content = f.read()

    st.markdown(f"<style>{theme_vars}\n{css_content}</style>", unsafe_allow_html=True)

inject_theme(st.session_state.dark_mode)


# -----------------------------------------------------------------------------
# LOGIQUE D'APPEL IA & GESTION DES ERREURS
# -----------------------------------------------------------------------------
def send(user_text: str) -> None:
    """Ajoute le message utilisateur, appelle l'agent Gemini, gère les erreurs."""
    st.session_state.messages.append({"role": "user", "content": user_text})
    try:
        with st.spinner("Analyse en cours par le tuteur NETLAB..."):
            answer = ask_agent(SYSTEM_PROMPT, st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    except MissingApiKeyError:
        st.session_state.messages.pop()
        st.error("Clé API absente : veuillez ajouter GEMINI_API_KEY dans votre fichier .env.")
    except EmptyResponseError:
        st.session_state.messages.pop()
        st.warning("Le service IA a renvoyé une réponse vide. Veuillez réessayer.")
    except Exception as e:
        st.session_state.messages.pop()
        st.error(f"Impossible de contacter le service IA ({e}).")


# -----------------------------------------------------------------------------
# BARRE LATÉRALE (SIDEBAR) : IDENTITÉ, THÈME & PARAMÈTRES
# -----------------------------------------------------------------------------
with st.sidebar:
    logo_img_html = f'<img src="data:image/png;base64,{LOGO_B64}" style="width: 36px; height: 36px; object-fit: contain;" alt="NETLAB Logo">' if LOGO_B64 else '<div style="width: 36px; height: 36px; border-radius: 8px; background: #2563EB;"></div>'
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.25rem;">
            {logo_img_html}
            <div>
                <span class="brand-title" style="font-size: 1.05rem; font-weight: 600; letter-spacing: -0.01em; text-transform: uppercase; display: block; line-height: 1.1;">NETLAB</span>
                <span style="font-size: 0.72rem; color: var(--text-secondary); font-weight: 500;">Parcours réseaux • INPTIC</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Interrupteur de Thème (Mode sombre aligné)
    col_theme_label, col_theme_toggle = st.columns([2.5, 1])
    with col_theme_label:
        st.markdown("<span style='font-size: 0.8rem; font-weight: 500; color: var(--text-secondary); line-height: 2.2;'>Mode sombre</span>", unsafe_allow_html=True)
    with col_theme_toggle:
        toggle_val = st.toggle("Mode sombre", value=st.session_state.dark_mode, label_visibility="collapsed")
        if toggle_val != st.session_state.dark_mode:
            st.session_state.dark_mode = toggle_val
            st.rerun()

    st.markdown("<div style='height: 0.35rem;'></div>", unsafe_allow_html=True)

    # Progression Globale (Valeur numérique en IBM Plex Mono)
    progress_pct = min(100, max(15, len(st.session_state.topics_visited) * 10))
    st.markdown(
        f"""
        <div style="background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: 8px; padding: 0.75rem 0.85rem; margin-bottom: 1.25rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; font-weight: 600; color: var(--text-secondary); margin-bottom: 0.4rem;">
                <span class="section-meta-label" style="margin: 0;">Progression globale</span>
                <span class="tech-mono" style="color: #2563EB; font-weight: 600; font-size: 0.82rem;">{progress_pct}%</span>
            </div>
            <div style="width: 100%; height: 4px; background: var(--bg-hover); border-radius: 9999px; overflow: hidden;">
                <div style="width: {progress_pct}%; height: 100%; background: #2563EB; border-radius: 9999px; transition: width 150ms ease;"></div>
            </div>
            <div style="font-size: 0.7rem; color: var(--text-secondary); margin-top: 0.4rem; font-weight: 400;">
                {len(st.session_state.topics_visited)} sur {len(TOPICS)} modules abordés
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sélecteurs de session
    topic = st.selectbox("Sujet du cours", TOPICS, index=0)
    mode = st.selectbox("Mode d'apprentissage", MODES, index=0)
    level = st.radio("Niveau d'étude", LEVELS, horizontal=True)

    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

    # Boutons d'Action (Empilés pleine largeur, libellés clairs)
    start_clicked = st.button("Commencer la leçon", type="primary", use_container_width=True)
    reset_clicked = st.button("Nouvelle leçon", type="secondary", use_container_width=True)

    # Informations d'Équipe (Groupe 5)
    st.markdown(
        """
        <div style="margin-top: 1.75rem; background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: 8px; padding: 0.85rem;">
            <div style="display: flex; align-items: center; gap: 0.4rem; font-size: 0.72rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.45rem; text-transform: uppercase; letter-spacing: 0.05em;">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                    <circle cx="9" cy="7" r="4"/>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                </svg>
                <span>Groupe 5 • LP_ASUR</span>
            </div>
            <div style="font-size: 0.72rem; color: var(--text-secondary); line-height: 1.45;">
                <strong style="color: var(--text-primary); font-weight: 600;">Chef de groupe :</strong><br>
                OBIANG ASSOUME Michel Rickiel<br>
                <div style="margin-top: 0.3rem;">
                    10 membres • INPTIC Gabon<br>
                    Enseignant : Dr Axel MENGARA
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Traitement des actions boutons
if reset_clicked:
    st.session_state.messages = []
    st.rerun()

if start_clicked:
    st.session_state.topics_visited.add(topic)
    send(build_user_prompt(topic, mode, level))
    st.rerun()


# -----------------------------------------------------------------------------
# EN-TÊTE ÉDITORIAL & FIL D'ARIANE
# -----------------------------------------------------------------------------
st.markdown(
    f"""
    <div style="margin-bottom: 1.75rem;">
        <span style="font-size: 13px; font-weight: 600; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 0.35rem;">
            Avant de commencer
        </span>
        <div style="display: flex; align-items: flex-start; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
            <div>
                <h1 style="font-family: var(--font-sans); font-size: 48px; font-weight: 600; font-style: italic; letter-spacing: -0.03em; color: var(--text-primary); margin: 0 0 0.45rem 0; line-height: 1.1;">
                    Une question en tête ?
                </h1>
                <p style="font-size: 0.92rem; color: var(--text-secondary); margin: 0; line-height: 1.5;">
                    Posez vos questions sur le <strong>{topic}</strong>, niveau {level.lower()}.
                </p>
            </div>
            <div style="display: flex; align-items: center; gap: 0.45rem; background: var(--bg-surface); color: #2563EB; padding: 0.4rem 0.85rem; border-radius: 8px; font-weight: 600; font-size: 0.82rem; border: 1px solid var(--border-color); height: 36px; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="2" y1="12" x2="22" y2="12"/>
                    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                </svg>
                <span>{topic}</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# FLUX DE CONVERSATION & SUGGESTIONS RAPIDES
# -----------------------------------------------------------------------------
if not st.session_state.messages:
    st.markdown(
        f"""
        <div style="margin-top: 1.5rem; margin-bottom: 1.25rem;">
            <span class="section-meta-label">
                Suggestions de questions sur {topic} :
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    suggestions = TOPIC_SUGGESTIONS.get(topic, [
        f"Peux-tu m'expliquer le concept de {topic} de manière synthétique ?",
        f"Donne-moi un exemple concret d'utilisation de {topic}",
        f"Lance un quiz interactif de 5 questions sur {topic}",
    ])

    cols = st.columns([1, 1, 1])
    for idx, (col, sug) in enumerate(zip(cols, suggestions)):
        with col:
            st.markdown(f'<div class="bubble-cloud-item bubble-cloud-item-{idx+1}">', unsafe_allow_html=True)
            if st.button(sug, key=f"sug_{idx}", use_container_width=True):
                st.session_state.topics_visited.add(topic)
                send(sug)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

else:
    # Flux des messages de discussion
    for m in st.session_state.messages:
        is_user = m["role"] == "user"
        with st.chat_message(
            "user" if is_user else "assistant",
            avatar=None if is_user else (AVATAR_PATH if os.path.exists(AVATAR_PATH) else None),
        ):
            st.markdown(m["content"])


# -----------------------------------------------------------------------------
# CHAMP DE SAISIE PRINCIPAL (EN BAS DE PAGE)
# -----------------------------------------------------------------------------
question = st.chat_input(f"Posez une question sur {topic} ou répondez au quiz...")
if question is not None:
    if question.strip():
        st.session_state.topics_visited.add(topic)
        send(question.strip())
        st.rerun()
    else:
        st.warning("Veuillez saisir un message avant d'envoyer.")
