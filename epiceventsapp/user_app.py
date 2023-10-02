import os
import hashlib
import binascii

MAX_LEN_VALUE = 70

def user_creation(request):
    message = []

    # Récupération des différents champs
    surname = request.form.get("surname")
    name = request.form.get("name")
    department = request.form.get("department")
    identifiant = request.form.get("identifiant")
    password = request.form.get("password")
    password2 = request.form.get("password2")

    # Controle de la valeur du champs "surname"
    if len(surname) == 0:
        message.append("No Surname : Vous avez oublié de renseigner le prénom")
    elif len(surname) > MAX_LEN_VALUE:
        message.append(f"Too Long Surname : Le prénom est limité à {MAX_LEN_VALUE}")

    # Controle de la valeur du champs "name"
    if len(name) == 0:
        message.append("No Name : Vous avez oublié de renseigner le nom")
    elif len(name) > MAX_LEN_VALUE:
        message.append(f"Too Long Name : Le nom est limité à {MAX_LEN_VALUE}")

    # Controle de la valeur du champs "department"
    if len(department) == 0:
        message.append("No Department : Vous avez oublié de renseigner l'équipe")

    # Controle de la valeur du champs "identifiant"
    if len(identifiant) == 0:
        message.append("No Identifiant : Vous avez oublié de renseigner l'identifiant")
    elif len(identifiant) > MAX_LEN_VALUE:
        message.append(f"Too Long Identifiant : L'identifiant est limité à {MAX_LEN_VALUE}")
    else:
        # Controle de la valeur du champs "password"
        if len(password) == 0:
            message.append("No Password : Vous avez oublié de renseigner le mot de passe")
        elif len(password) > MAX_LEN_VALUE:
            message.append(f"Too Long Password : Le mot de passe est limité à {MAX_LEN_VALUE}")
        else:
            # Controle de la concordance de "password" et "password2"
            if password != password2:
                message.append("Different Password : Les deux mots de passe ne correspondent pas")
            else:
                # Génére un sel
                salt = os.urandom(16)
                # Code le mot de passe  en bytes
                hashed_password = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
                # Le transforme en chaine hexadécimale
                hashed_password = binascii.hexlify(hashed_password)
    


    user = {"surname": surname,
            "name": name,
            "department": department,
            "identifiant": identifiant,
            "password":hashed_password,
            "salt":salt}

    return user, message
