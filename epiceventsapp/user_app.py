import os
import hashlib
import binascii
import exchange_bdd as bdd
from flask import session

MAX_LEN_VALUE = 70


def control_user(identifiant, password):

    user_result, message = bdd.control_user_bdd(identifiant)

    if user_result is None:
        valid_identifiant = False
        message = "- User Unknown : L'utilisateur n'est pas connu de la base de données"
    else:
        user_id = user_result[0]
        user_role = user_result[4]
        user_salt = user_result[7]
        user_password = user_result[5]
        password_encode = password.encode('utf-8')
        hashed_password = binascii.hexlify(hashlib.pbkdf2_hmac('sha256',
                                                               password_encode,
                                                               user_salt,
                                                               100000))
        password_decode = hashed_password.decode('utf-8')
        # Si le mot de passe est correct
        if password_decode == user_password:
            valid_identifiant = True
            session['user_role'] = user_role
            session['id'] = user_id
        # Si le mot de passe est incorrect
        else:
            valid_identifiant = False
            message = "- Wrong Password : L'identifiant est connu mais le mot de passe est incorrect"

    return valid_identifiant, message


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


def user_edit(request, user_id):
    message = ""

    # Récupération des différents champs
    surname = request.form.get("surname")
    name = request.form.get("name")
    department = request.form.get("department")
    identifiant = request.form.get("identifiant")

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

    if message == "":
        user = {"surname": surname,
                "name": name,
                "department": department,
                "identifiant": identifiant,
                "id": user_id}
    else:
        user = ""

    return user, message
