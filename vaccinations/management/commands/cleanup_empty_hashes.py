# vaccinations/management/commands/cleanup_empty_hashes.py
from django.core.management.base import BaseCommand
from django.db import models
from vaccinations.models import Parent

class Command(BaseCommand):
    help = "Clean up Parent records with empty whatsapp_hash and fix them"

    def handle(self, *args, **opts):
        # Find parents with empty or null hash
        empty_hash_parents = Parent.objects.using("patients").filter(
            models.Q(whatsapp_hash='') | models.Q(whatsapp_hash__isnull=True)
        )
        
        self.stdout.write(f"Found {empty_hash_parents.count()} parents with empty/null hash")
        
        fixed = 0
        deleted = 0
        
        for parent in empty_hash_parents:
            # Try to get the whatsapp number
            try:
                whatsapp_num = parent.whatsapp_e164  # This should decrypt if possible
                if whatsapp_num and len(whatsapp_num.replace('+', '').replace(' ', '')) >= 10:
                    # We have a valid number, fix the hash
                    parent.whatsapp_e164 = whatsapp_num  # This will set both enc and hash
                    parent.save(using="patients", update_fields=["whatsapp_e164_enc", "whatsapp_hash"])
                    fixed += 1
                    self.stdout.write(f"Fixed parent {parent.id} with number {whatsapp_num}")
                else:
                    # No valid number, check if this parent has children
                    if parent.children.using("patients").exists():
                        self.stdout.write(f"Parent {parent.id} has children but no valid WhatsApp number - skipping")
                    else:
                        # No children, safe to delete
                        parent.delete(using="patients")
                        deleted += 1
                        self.stdout.write(f"Deleted parent {parent.id} (no valid number, no children)")
            except Exception as e:
                self.stdout.write(f"Error processing parent {parent.id}: {e}")
                # Check if this parent has children
                if parent.children.using("patients").exists():
                    self.stdout.write(f"Parent {parent.id} has children but corrupted data - skipping")
                else:
                    # No children, safe to delete
                    parent.delete(using="patients")
                    deleted += 1
                    self.stdout.write(f"Deleted parent {parent.id} (corrupted data, no children)")
        
        self.stdout.write(self.style.SUCCESS(f"Cleanup complete: {fixed} fixed, {deleted} deleted"))
