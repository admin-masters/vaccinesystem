# vaccinations/crypto.py
import base64, os, secrets
import hashlib, re
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.fernet import Fernet
from django.conf import settings

ACTIVE_KEY_ID = int(os.environ.get("DATA_KEY_ACTIVE", "1"))
# Key ring to support rotation, values are base64url 32‑byte keys
KEYS = {
    1: base64.urlsafe_b64decode(os.environ["DATA_KEY_1"]),
    # add 2,3,... as needed
}

SEARCH_PEPPER = base64.urlsafe_b64decode(os.environ["SEARCH_PEPPER"])  # for HMAC indexing

def _key(key_id: int | None = None) -> bytes:
    return KEYS[key_id or ACTIVE_KEY_ID]

def encrypt(plaintext: bytes, key_id: int | None = None, aad: bytes = b"") -> bytes:
    aes = AESGCM(_key(key_id))
    nonce = secrets.token_bytes(12)
    ct = aes.encrypt(nonce, plaintext, aad)
    # store as: key_id(1B) | nonce(12B) | ct
    return bytes([key_id or ACTIVE_KEY_ID]) + nonce + ct

def decrypt(blob: bytes, aad: bytes = b"") -> bytes:
    key_id = blob[0]
    nonce, ct = blob[1:13], blob[13:]
    aes = AESGCM(_key(key_id))
    return aes.decrypt(nonce, ct, aad)

def hmac_sha256(data: bytes) -> str:
    h = hmac.HMAC(SEARCH_PEPPER, hashes.SHA256())
    h.update(data); return h.finalize().hex()

# New functions for Parent model encryption and hashing
def digits(s: str) -> str:
    return "".join(ch for ch in (s or "") if ch.isdigit())

def last10(s: str) -> str:
    d = digits(s)
    return d[-10:] if len(d) >= 10 else d

def hash_last10(e164: str) -> str:
    return hashlib.sha256(last10(e164).encode("utf-8")).hexdigest()

def fernet():
    return Fernet(settings.PATIENT_DATA_FERNET_KEY)

def encrypt_str(s: str) -> bytes:
    return fernet().encrypt(s.encode("utf-8"))

def decrypt_str(b: bytes) -> str:
    return fernet().decrypt(b).decode("utf-8")
