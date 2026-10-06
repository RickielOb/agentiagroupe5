"""Appel à l'API Gemini. La clé est lue dans le fichier .env."""
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


class MissingApiKeyError(Exception):
    """La clé GEMINI_API_KEY est absente du fichier .env."""


class EmptyResponseError(Exception):
    """L'API a renvoyé une réponse vide ou invalide."""


def _get_client() -> genai.Client:
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise MissingApiKeyError("GEMINI_API_KEY est absente du fichier .env")
    return genai.Client(api_key=api_key)


def ask_agent(system_prompt: str, messages: list[dict]) -> str:
    """Envoie le prompt système et tout l'historique, retourne la réponse.

    messages : liste de {"role": "user" | "assistant", "content": str}
    """
    client = _get_client()
    contents = [
        types.Content(
            role="user" if m["role"] == "user" else "model",
            parts=[types.Part(text=m["content"])],
        )
        for m in messages
    ]
    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.5,
        ),
    )
    text = (response.text or "").strip()
    if not text:
        raise EmptyResponseError("Réponse vide")
    return text
