from django.core.management.base import BaseCommand
from vaccinations.models import VaccineDose
from collections import defaultdict, deque

class Command(BaseCommand):
    help = "Audit VaccineDose linkage and offsets for logical schedule errors."

    def handle(self, *args, **opts):
        bad = False
        doses = list(VaccineDose.objects.select_related("previous_dose","vaccine").order_by("vaccine__name","sequence_index","id"))

        # 1) self-links
        self_links = [d for d in doses if d.previous_dose_id and d.previous_dose_id == d.id]
        if self_links:
            bad = True
            self.stdout.write(self.style.ERROR("Self-links:"))
            for d in self_links:
                self.stdout.write(f" - {d.id} {d.vaccine.name} seqidx={d.sequence_index} points to itself")

        # 2) cycles (DFS)
        by_id = {d.id: d for d in doses}
        visited, stack = {}, {}
        cycles = []

        def dfs(u):
            visited[u] = True
            stack[u] = True
            d = by_id[u]
            v = d.previous_dose_id
            if v and v in by_id:
                if v not in visited and dfs(v): return True
                elif stack.get(v):
                    cycles.append((u, v))
                    return True
            stack[u] = False
            return False

        for d in doses:
            if d.id not in visited:
                dfs(d.id)

        if cycles:
            bad = True
            self.stdout.write(self.style.ERROR("Cycles detected (sample edges):"))
            for u,v in cycles[:10]:
                self.stdout.write(f" - {u} -> {v}")

        # 3) silly offsets that indicate unit bugs
        weird = [d for d in doses if d.min_offset_days is not None and d.min_offset_days not in (0, 42, 70, 98) and d.min_offset_days < 30]
        if weird:
            bad = True
            self.stdout.write(self.style.ERROR("Unusually small min_offset_days (<30 and not 0/42/70/98):"))
            for d in weird[:25]:
                self.stdout.write(f" - id={d.id} {d.vaccine.name} min={d.min_offset_days} (prev={d.previous_dose_id})")

        if not bad:
            self.stdout.write(self.style.SUCCESS("Schedule audit: OK (no self-links, no cycles, offsets look sane)."))
        else:
            self.stdout.write(self.style.WARNING("Fix the above before recomputing due dates."))
