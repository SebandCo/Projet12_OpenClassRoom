from flask import session

MAX_LEN_VALUE = 70
MAX_LEN_VALUE_PHONE = 20
MAX_LEN_VALUE_EMAIL = 255


def client_creation(request):
    message = ""
    # Récupération des différents champs
    surname = request.form.get("surname")
    name = request.form.get("name")
    email = request.form.get("email")
    phone_number = request.form.get("phone_number")
    collaborateur = request.form.get("collaborateur")
    enterprise = request.form.get("enterprise")

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

    # Controle de la valeur du champs "email"
    if not email:
        message += "- No Email : Vous avez oublié de renseigner l'email\n"
    elif len(email) > MAX_LEN_VALUE_EMAIL:
        message += f"- Too Long Email : L'email est limité à {MAX_LEN_VALUE_EMAIL}\n"

    # Controle de la valeur du champs "phone_number"
    if not phone_number:
        message += "- No Phone : Vous avez oublié de renseigner le numéro de téléphone\n"
    elif len(phone_number) > MAX_LEN_VALUE_PHONE:
        message += f"- Too Long Phone : Le numéro de téléphone est limité à {MAX_LEN_VALUE_PHONE}\n"

    # Récupération du champs "collaborateur"
    collaborateur = session['id']

    # Récupération du champs "enterprise"
    if not enterprise:
        message += "- No Enterprise : Vous avez oublié de renseigner l'entreprise\n"

    if message == "":
        print("test")
        client = {"surname": surname,
                  "name": name,
                  "email": email,
                  "phone_number": phone_number,
                  "collaborateur": collaborateur,
                  "enterprise": enterprise}
    else:
        client = ""

    return client, message
