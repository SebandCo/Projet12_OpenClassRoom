import os
import hashlib
import binascii

MAX_LEN_VALUE = 70


def user_creation(request):
    message = ""

    # Récupération des différents champs
    surname = request.form.get("surname")
    name = request.form.get("name")
    department = request.form.get("department")
    identifiant = request.form.get("identifiant")
    password = request.form.get("password")
    password2 = request.form.get("password2")
    hashed_password = ""
    salt = ""

    # Controle de la valeur du champs "surname"
    if not surname:
        message += "- No Surname : Vous avez oublié de renseigner le prénom\n"
    elif len(surname) > MAX_LEN_VALUE:
        message += f"- Too Long Surname : Le prénom est limité à {MAX_LEN_VALUE}\n"

    # Controle de la valeur du champs "name"
    if not name:
        message += "- No Name : Vous avez oublié de renseigner le nom\n"
    elif len(name) > MAX_LEN_VALUE:
        message += f"- Too Long Name : Le nom est limité à {MAX_LEN_VALUE}\n"

    # Controle de la valeur du champs "department"
    if not department:
        message += "- No Department : Vous avez oublié de renseigner l'équipe\n"

    # Controle de la valeur du champs "identifiant"
    if not identifiant:
        message += "- No Identifiant : Vous avez oublié de renseigner l'identifiant\n"
    elif len(identifiant) > MAX_LEN_VALUE:
        message += f"- Too Long Identifiant : L'identifiant est limité à {MAX_LEN_VALUE}\n"

    # Controle de la valeur du champs "password"
    if not password:
        message += "- No Password : Vous avez oublié de renseigner le mot de passe\n"
    elif len(password) > MAX_LEN_VALUE:
        message += f"- Too Long Password : Le mot de passe est limité à {MAX_LEN_VALUE}\n"
    else:
        # Controle de la concordance de "password" et "password2"
        if password != password2:
            message += "- Different Password : Les deux mots de passe ne correspondent pas\n"
        else:
            # Génére un sel
            salt = os.urandom(16)
            # Transforme le mot de passe en UTF-8 pour l'encodage
            password = password.encode('utf-8')
            # Code le mot de passe  en bytes
            hashed_password = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
            # Le transforme en chaine hexadécimale
            hashed_password = binascii.hexlify(hashed_password)

    if message == "":
        user = {"surname": surname,
                "name": name,
                "department": department,
                "identifiant": identifiant,
                "password": hashed_password,
                "salt": salt}
    else:
        user = ""

    return user, message
