from django.core.management.base import BaseCommand
from vaccinations.models import VaccineDose
from collections import defaultdict
import re, unicodedata

def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", (s or "")).replace("\u00A0", " ")
    s = re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
    return s

def series_key_for(name: str) -> str:
    n = norm(name)
    if "influenza" in n:                                 return "Influenza"
    if any(k in n for k in ["dtwp","dtap","dtp","tdap"]) or re.search(r"\btd\b", n):
                                                         return "DTP"
    if "hib" in n:                                       return "Hib"
    if re.search(r"\bipv\b", n):                         return "IPV"
    if re.search(r"\bopv\b", n):                         return "OPV"
    if "pcv" in n:                                       return "PCV"
    if "rota" in n:                                      return "Rota"
    if "hep b" in n or re.search(r"\bhepb\b", n):        return "HepB"
    if "hep a" in n:                                     return "HepA"
    if "mmr" in n:                                       return "MMR"
    if "varicella" in n or re.search(r"\bvar\b", n):     return "Var"
    if "hpv" in n:                                       return "HPV"
    if "typhoid" in n:                                   return "Typhoid"
    if "bcg" in n:                                       return "BCG"
    # fallback: first token
    return (n.split() or ["misc"])[0].capitalize()

class Command(BaseCommand):
    help = "Backfill series_key and series_seq using normalized clinical series names."

    def add_arguments(self, parser):
        parser.add_argument("--reseq", action="store_true", help="Force reassign series_seq based on offsets.")

    def handle(self, *args, **opts):
        doses = list(VaccineDose.objects.select_related("vaccine").order_by("id"))
        for d in doses:
            d.series_key = series_key_for(d.vaccine.name)

        groups = defaultdict(list)
        for d in doses:
            groups[d.series_key].append(d)

        # Order primarily by min_offset_days (after normalization), then sequence_index, then id.
        for key, lst in groups.items():
            if opts["reseq"]:
                lst.sort(key=lambda x: ((x.min_offset_days if x.min_offset_days is not None else 10**9),
                                        (x.sequence_index or 0), x.id))
                for i, d in enumerate(lst, 1):
                    d.series_seq = i
                    d.save(update_fields=["series_key","series_seq"])
            else:
                for d in lst:
                    d.save(update_fields=["series_key"])
        self.stdout.write(self.style.SUCCESS(f"Backfilled {sum(len(v) for v in groups.values())} doses into {len(groups)} series."))
