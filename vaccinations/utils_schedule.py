from typing import Dict, Optional, List
from .models import ChildDose
from .models import VaccineDose
def build_series_prev_maps(child_doses: List[ChildDose]):
    """
    For each ChildDose, compute effective previous as:
      - previous member in the same series_key by series_seq (1-based).
    This ignores explicit previous_dose_id (we normalized it already).
    """
    by_dep = {cd.dose_id: cd for cd in child_doses}
    # Build index per series_seq
    per_series: Dict[str, List[ChildDose]] = {}
    for cd in child_doses:
        per_series.setdefault(cd.dose.series_key, []).append(cd)
    for key in per_series:
        per_series[key].sort(key=lambda x: x.dose.series_seq)

    prev_cd_by, prev_min_by = {}, {}
    for key, lst in per_series.items():
        for i, cd in enumerate(lst):
            if i == 0:
                prev_cd_by[cd.dose_id] = None
                prev_min_by[cd.dose_id] = None
            else:
                prev_cd_by[cd.dose_id] = lst[i-1]
                prev_min_by[cd.dose_id] = lst[i-1].dose.min_offset_days
    return prev_cd_by, prev_min_by
def clinical_display_label(dose: "VaccineDose") -> str:
    """
    Return the label we want to show as the vaccine title in parent/doctor UIs.
    We keep the 'dose_label' (e.g., 'Dose 1 / Booster') as a subtitle elsewhere.
    """
    try:
        name = (dose.vaccine.name or "").strip()
    except Exception:
        name = ""
    # Fall back to something deterministic if name missing:
    return name or f"Vaccine #{getattr(dose, 'vaccine_id', '?')}"