from django.core.management.base import BaseCommand, CommandError
from vaccinations.models import UiString, UiStringTranslation
import csv, pathlib

class Command(BaseCommand):
    help = "Import UI translations from a CSV file with columns: key,description,language,text"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str)

    def handle(self, *args, **opts):
        path = pathlib.Path(opts["csv_path"])
        if not path.exists():
            raise CommandError(f"File not found: {path}")
        with path.open("r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            created = updated = 0
            for row in reader:
                key = (row.get("key") or "").strip()
                desc = (row.get("description") or "").strip()
                lang = (row.get("language") or "").strip().lower()
                text = (row.get("text") or "").strip()
                if not key or not lang or not text:
                    continue
                ui, _ = UiString.objects.get_or_create(key=key, defaults={"description": desc})
                if desc and ui.description != desc:
                    ui.description = desc
                    ui.save(update_fields=["description"])
                obj, was_created = UiStringTranslation.objects.update_or_create(
                    ui=ui, language=lang, defaults={"text": text}
                )
                created += int(was_created)
                updated += int(not was_created)
        self.stdout.write(self.style.SUCCESS(f"Imported OK. Created {created}, updated {updated}."))
