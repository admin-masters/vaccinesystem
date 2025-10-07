from __future__ import annotations
from .models import UiStringTranslation
from .utils import STATE_LANG  # your existing state->lang map

def ui_lang_for_parent(parent, child) -> str:
    # prefer explicit setting, otherwise derive from child's state; fall back to English
    return (getattr(parent, "pref_lang", "") or STATE_LANG.get(child.state) or "en").lower()

def t(lang: str, key: str, default: str = "") -> str:
    row = (UiStringTranslation.objects
           .filter(ui__key=key, language=lang)
           .values_list("text", flat=True).first())
    if row:
        return row
    # single-step fallback to English
    if lang != "en":
        row = (UiStringTranslation.objects
               .filter(ui__key=key, language="en")
               .values_list("text", flat=True).first())
        if row:
            return row
    return default or key
