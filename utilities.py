import re

def verificar_contrasena(contrasena):
    """
    Verifica si una contraseña cumple con los siguientes requisitos:
    - Mayor de 8 caracteres
    - Al menos una mayúscula
    - Al menos un carácter especial (por ejemplo, !, @, #, $)
    """
    # Verifica la longitud
    if len(contrasena) < 8:
        return False

    # Verifica si hay al menos una mayúscula
    if not re.search(r'[A-Z]', contrasena):
        return False

    # Verifica si hay al menos un carácter especial
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', contrasena):
        return False

    # La contraseña cumple con todos los requisitos
    return True
