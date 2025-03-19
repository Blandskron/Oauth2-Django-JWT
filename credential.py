import base64
import hashlib
import os

# Generar un code_verifier aleatorio
code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8").rstrip("=")

# Aplicar SHA-256 y codificar en base64 URL-safe
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode("utf-8")).digest()
).decode("utf-8").rstrip("=")

print(f"Code Verifier: {code_verifier}")
print(f"Code Challenge: {code_challenge}")
