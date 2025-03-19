import base64
import os

# Generar una clave secreta aleatoria
secret_key = base64.urlsafe_b64encode(os.urandom(64)).decode("utf-8").rstrip("=")

print(f"Generated JWT Secret Key: {secret_key}")
