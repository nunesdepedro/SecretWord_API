from app.core.config import settings

MASTER_KEY = settings.MASTER_KEY.encode()  # Use the master key from settings

import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# generate key from master key
def _derive_key(master_key: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(master_key)


def encrypt_password(master_key: bytes, plaintext: str) -> str:
    salt = os.urandom(16)
    key = _derive_key(master_key, salt)

    aesgcm = AESGCM(key)
    nonce = os.urandom(12)

    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)

    # save everything in base64 for storage
    return base64.b64encode(salt + nonce + ciphertext).decode()


def decrypt_password(master_key: bytes, token: str) -> str:
    raw = base64.b64decode(token)

    salt = raw[:16]
    nonce = raw[16:28]
    ciphertext = raw[28:]

    key = _derive_key(master_key, salt)

    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None).decode()
