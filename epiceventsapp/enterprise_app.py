MAX_LEN_VALUE = 100


def enterprise_creation(request):
    message = ""

    # Récupération des différents champs
    name = request.form.get("name")

    # Controle de la valeur du champs "name"
    if not name:
        message += "- No Name : Vous avez oublié de renseigner le nom\n"
    elif len(name) > MAX_LEN_VALUE:
        message += f"- Too Long Name : Le nom est limité à {MAX_LEN_VALUE}\n"

    if message == "":
        enterprise = {"name": name}
    else:
        enterprise = ""

    return enterprise, message
