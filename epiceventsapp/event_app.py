MAX_LEN_VALUE = 70
MAX_LEN_VALUE_LOCATION = 140
MAX_LEN_VALUE_NOTES = 500


def event_creation(request):
    message = ""
    # Récupération des différents champs
    name = request.form.get("name")
    contract = request.form.get("contract")
    client = request.form.get("client")
    event_date_start = request.form.get("event_date_start")
    event_date_end = request.form.get("event_date_end")
    support_contact = request.form.get("support_contact")
    location = request.form.get("location")
    attendees = request.form.get("attendees")
    notes = request.form.get("notes")

    # Controle de la valeur du champs "name"
    if not name:
        message += "- No Name : Vous avez oublié de renseigner le nom\n"
    elif len(name) > MAX_LEN_VALUE:
        message += f"- Too Long Name : Le nom est limité à {MAX_LEN_VALUE}\n"

    # Controle de la valeur du champs "contract"
    if not contract:
        message += "- No Contract : Vous avez oublié de renseigner le numéro de contrat\n"

    # Controle de la valeur du champs "client"
    if not client:
        message += "- No Client : Vous avez oublié de renseigner le client\n"

    # Controle de la valeur du champs "event_date_start"
    if not event_date_start:
        message += "- No Date Start : Vous avez oublié de renseigner la date de début\n"
    else:
        # Controle de la valeur du champs "event_date_end"
        if not event_date_end:
            message += "- No Date End : Vous avez oublié de renseigner la date de fin\n"
        elif event_date_end <= event_date_start:
            message += "- Date Incorrect : La date de fin ne peut pas être inférieur à la date de début\n"

    # Controle de la valeur du champs "support_contact"
    if not support_contact:
        message += "- No Support Contact : Vous avez oublié de renseigner le nom du contact\n"
    elif len(support_contact) > MAX_LEN_VALUE:
        message += f"- Too Long Support Contact : Le nom du contact est limité à {MAX_LEN_VALUE}\n"

    # Controle de la valeur du champs "location"
    if not location:
        message += "- No Location : Vous avez oublié de renseigner la localisation\n"
    elif len(location) > MAX_LEN_VALUE_LOCATION:
        message += f"- Too Long Location : La localisation est limité à {MAX_LEN_VALUE_LOCATION}\n"

    # Controle de la valeur du champs "attendees"
    if not attendees:
        message += "- No Attendees : Vous avez oublié de renseigner le nombre de participant\n"
    else:
        attendees = int(attendees)
        if attendees <= 0:
            message += "- Attendees Negative : Le nombre de participant doit être positif\n"

    # Controle de la valeur du champs "notes"
    if len(notes) > MAX_LEN_VALUE_NOTES:
        message += f"- Too Long Notes : La partie note est limité à {MAX_LEN_VALUE_NOTES}\n"

    if message == "":
        event = {"name": name,
                 "contract": contract,
                 "client": client,
                 "event_date_start": event_date_start,
                 "event_date_end": event_date_end,
                 "support_contact": support_contact,
                 "location": location,
                 "attendees": attendees,
                 "notes": notes}
    else:
        event = ""

    return event, message
