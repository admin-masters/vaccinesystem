from django.core.management.base import BaseCommand
from vaccinations.models import Parent


class Command(BaseCommand):
    help = "Scrub all parents' WhatsApp numbers by replacing them with anonymized unique placeholders"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show how many records would be updated without saving changes",
        )

    def handle(self, *args, **options):
        parents = Parent.objects.all().only("id", "whatsapp_e164")
        count = parents.count()

        if options.get("dry_run"):
            self.stdout.write(self.style.WARNING(f"[DRY-RUN] Would update {count} parent records"))
            return

        updated = 0
        for parent in parents.iterator(chunk_size=1000):
            # Preserve uniqueness by making each placeholder depend on the row id
            placeholder = f"redacted-{parent.id}"
            if parent.whatsapp_e164 != placeholder:
                parent.whatsapp_e164 = placeholder
                parent.save(update_fields=["whatsapp_e164"])
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"Updated {updated} parent records"))


