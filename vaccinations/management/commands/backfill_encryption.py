# vaccinations/management/commands/backfill_encryption.py
from django.core.management.base import BaseCommand
from django.db import models
from vaccinations.models import Parent
from vaccinations.crypto import encrypt_str, hash_last10
from vaccinations.utils import normalize_msisdn

class Command(BaseCommand):
    help = "Backfill whatsapp_hash and encrypted number for Parent rows"

    def handle(self, *args, **opts):
        qs = Parent.objects.using("patients").filter(models.Q(whatsapp_hash__isnull=True) | models.Q(whatsapp_hash=""))
        fixed = 0
        for p in qs.iterator():
            num = getattr(p, "whatsapp_e164", "")  # property decrypts if present
            if not num:
                continue
            p.whatsapp_e164 = num  # setter fills enc + hash
            p.save(using="patients", update_fields=["whatsapp_e164_enc", "whatsapp_hash"])
            fixed += 1
        self.stdout.write(self.style.SUCCESS(f"Backfilled {fixed} parents."))
