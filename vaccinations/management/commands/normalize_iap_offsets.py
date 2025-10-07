from django.core.management.base import BaseCommand
from vaccinations.models import VaccineDose
import re, unicodedata

W, M, Y = 7, 30, 365

def S(s: str) -> str:
    s = unicodedata.normalize("NFKD", (s or "")).replace("\u00A0", " ")
    return s.strip().lower()

class Command(BaseCommand):
    help = "Normalize VaccineDose offsets and anchor_policy to IAP rules (case-insensitive)."

    def handle(self, *args, **opts):
        updated = 0

        def set_fields(d, policy, min_days, max_days=None):
            nonlocal updated
            changed = False
            if d.anchor_policy != policy:
                d.anchor_policy = policy; changed = True
            if d.min_offset_days != min_days:
                d.min_offset_days = min_days; changed = True
            if (d.max_offset_days or None) != (max_days or None):
                d.max_offset_days = max_days; changed = True
            if changed:
                d.save(update_fields=["anchor_policy","min_offset_days","max_offset_days"])
                updated += 1

        for d in VaccineDose.objects.select_related("vaccine").all():
            name = S(d.vaccine.name)
            key  = S(getattr(d, "series_key", ""))         # normalized Series Key (lower)
            seq  = getattr(d, "series_seq", 1)

            # --- Birth (0 days) ---
            if "bcg" in name or "opv" in name:
                set_fields(d, "A", 0, None); continue
            if "hep b" in name and (seq == 1 or "1" in name):
                set_fields(d, "A", 0, None); continue

            # --- 6w/10w/14w primaries ---
            if key in {"dtp","hib","ipv","hepb","pcv","rota"}:
                if seq == 1: set_fields(d, "L", 6*W, None);  continue
                if seq == 2: set_fields(d, "L", 10*W, None); continue
                if seq == 3: set_fields(d, "L", 14*W, None); continue

            # --- Influenza series ---
            if key == "influenza":
                # 1: 6m; 2: +1m; 3..: +1y each
                if seq == 1: set_fields(d, "L", 6*M, None);              continue
                if seq == 2: set_fields(d, "I", 7*M, None);              continue
                if seq == 3: set_fields(d, "I", 7*M + 365, None);        continue
                if seq == 4: set_fields(d, "I", 7*M + 2*365, None);      continue
                if seq == 5: set_fields(d, "I", 7*M + 3*365, None);      continue

            # --- Typhoid (6–9m) ---
            if "typhoid" in name:
                set_fields(d, "A", 6*M, 9*M); continue

            # --- MMR (9m, 15m, 4–6y) ---
            if "mmr" in name:
                if seq == 1: set_fields(d, "A", 9*M, None);    continue
                if seq == 2: set_fields(d, "L", 15*M, None);   continue
                if seq == 3: set_fields(d, "L", 4*Y, 6*Y);     continue

            # --- HepA (12m, 18–19m) ---
            if "hep a" in name:
                if seq == 1: set_fields(d, "A", 12*M, None);   continue
                if seq == 2: set_fields(d, "L", 18*M, 19*M);   continue

            # --- Varicella (15m, 18–19m) ---
            if "varicella" in name or re.search(r"\bvar\b", name):
                if seq == 1: set_fields(d, "A", 15*M, None);   continue
                if seq == 2: set_fields(d, "L", 18*M, 19*M);   continue

            # --- 12–15m PCV booster ---
            if key == "pcv" and seq == 4:
                set_fields(d, "L", 12*M, 15*M); continue

            # --- 16–18m boosters (DTP/Hib/IPV) ---
            if key in {"dtp","hib","ipv"} and seq == 4:
                set_fields(d, "L", 16*M, 18*M); continue

            # --- 4–6y boosters for DTP/IPV handled via seq==5 ---
            if key in {"dtp","ipv"} and seq == 5:
                set_fields(d, "L", 4*Y, 6*Y); continue

            # --- Tdap/Td (10–12y) under DTP series ---
            if key == "dtp" and ("tdap" in name or re.search(r"\btd\b", name)):
                set_fields(d, "L", 10*Y, 12*Y); continue

            # --- HPV program (girls 9–15y) ---
            if "hpv" in name:
                set_fields(d, "A", 9*Y, 15*Y); continue

        # Final sweep: fix any lingering tiny offsets by name
        allowed_small = {0, 42, 70, 98}
        for d in VaccineDose.objects.all():
            n = S(d.vaccine.name)
            if d.min_offset_days is not None and d.min_offset_days < 30 and d.min_offset_days not in allowed_small:
                if "ipv" in n:    set_fields(d, "L", 6*W, None)
                elif "mmr" in n:  set_fields(d, "A", 9*M, None)
                elif "pcv" in n:  set_fields(d, "L", 6*W, None)
                elif "tdap" in n or re.search(r"\btd\b", n): set_fields(d, "L", 10*Y, 12*Y)
                elif "varicella" in n or re.search(r"\bvar\b", n): set_fields(d, "A", 15*M, None)
                elif "typhoid" in n: set_fields(d, "A", 6*M, 9*M)
                elif "hib" in n or "dtp" in n or "hep b" in n or "rota" in n:
                    set_fields(d, "L", 6*W, None)

        self.stdout.write(self.style.SUCCESS("Offsets normalized."))
