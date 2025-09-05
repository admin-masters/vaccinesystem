from __future__ import annotations
from datetime import date, timedelta
from django.utils import timezone

def birth_window(dob: date, min_offset_days: int, max_offset_days: int | None):
    due_date = dob + timedelta(days=min_offset_days + 1)
    due_until_date = None if max_offset_days is None else dob + timedelta(days=max_offset_days)
    return due_date, due_until_date

def booster_window(prev_given: date, booster_min: int, prev_min: int, booster_max: int | None):
    delta_min = booster_min - prev_min
    due_date = prev_given + timedelta(days=delta_min + 1)
    if booster_max is None:
        return due_date, None
    delta_max = booster_max - prev_min
    return due_date, prev_given + timedelta(days=delta_max)

def today() -> date:
    return timezone.localdate()

def status_code_for(due_date: date | None, due_until: date | None, given_date: date | None) -> str:
    if given_date:
        return "given-on-date"
    if not due_date:
        return "due-on-a-future-date"
    t = today()
    if t < due_date:
        return "due-on-a-future-date"
    if (due_until is None and t >= due_date) or (due_until is not None and due_date <= t <= due_until):
        return "due-as-on-date"
    if due_until is not None and t > due_until:
        return "overdue"
    return "due-on-a-future-date"

# Simple Indian E.164 normaliser for WhatsApp (minimal; adapt as needed)
def normalize_msisdn(raw: str) -> str:
    digits = "".join(ch for ch in raw if ch.isdigit())
    if not digits:
        return raw.strip()
    if digits.startswith("91") and len(digits) == 12:
        return f"+{digits}"
    if len(digits) == 10:
        return f"+91{digits}"
    if raw.strip().startswith("+"):
        return raw.strip()
    return f"+{digits}"
