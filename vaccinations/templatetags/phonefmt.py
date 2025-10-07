from django import template
import re

register = template.Library()

@register.filter
def phone_e164(raw: str):
    """Make a best-effort E.164-ish string for tel: links."""
    if not raw:
        return ""
    s = re.sub(r"[^\d+]", "", raw)  # remove everything except digits and '+'
    if s.startswith("+"):
        return s
    if s.startswith("0"):
        return "+91" + s[1:]   # default country code
    if s.startswith("91"):
        return "+" + s
    return "+91" + s
