# Se puede crear una clave con:
# python3 -c "import secrets; print(secrets.token_urlsafe(64))"


# pip install "python-jose[cryptography]"
# pip install "passlib[bcrypt]"
# pip install python-multipart

# pip install "bcrypt==4.0.1"

CLAVE_SECRETA = "saTHAnyWkNFmpPwaltC8y1oWGBUbXGPCjdlBMpFfUyjDDiMBZYRmY8W0LIpTIELeqNauNmF6gCxBmopzIZJ6cA"
ALGORITMO = "HS256"
MINUTOS_EXPIRACION_TOKEN = 600000 