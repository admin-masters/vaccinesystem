from __future__ import annotations
from typing import Any
from .models import UiStringTranslation
from .utils import STATE_LANG  # state -> primary lang map


def ui_lang_for_parent(parent: Any, child: Any) -> str:
    """
    Derive UI language for the parent.
    - First, try parent's preferred language.
    - Else, derive from child's state (supports encrypted field).
    - Fall back to English if nothing is found.
    """
    state = None

    # Handle encrypted state (if method available)
    if hasattr(child, "get_state_encrypted"):
        try:
            state = child.get_state_encrypted()
        except Exception:
            state = None

    # If still not found, check normal or clinic-based state
    if not state:
        state = getattr(child, "state", "") or getattr(getattr(child, "clinic", None), "state", "")

    # Return resolved language
    return (getattr(parent, "pref_lang", "") or STATE_LANG.get(state) or "en").lower()


def t(lang: str, key: str, default: str = "") -> str:
    """
    Fetch translation text for a given key and language.
    Always reads from the 'masters' DB.
    Falls back to English if translation not found.
    """
    row = (
        UiStringTranslation.objects.using("masters")
        .filter(ui__key=key, language=lang)
        .values_list("text", flat=True)
        .first()
    )
    if row:
        return row

    # Fallback to English translation
    if lang != "en":
        row = (
            UiStringTranslation.objects.using("masters")
            .filter(ui__key=key, language="en")
            .values_list("text", flat=True)
            .first()
        )
        if row:
            return row

    # Final fallback: return default or key itself
    return default or key
