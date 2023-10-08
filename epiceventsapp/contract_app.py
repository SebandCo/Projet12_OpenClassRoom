def contract_creation(request):
    message = ""

    # Récupération des différents champs
    client = request.form.get("client")
    total_amount_contract = request.form.get("total_amount_contract")
    amount_be_paid = request.form.get("amount_be_paid")
    signature_contract = request.form.get("signature_contract")

    # Controle de la valeur du champs "client"
    if not client:
        message += "- No Client : Vous avez oublié de renseigner le nom du client\n"

    # Controle de la valeur du champs "total_amount_contract"
    if not total_amount_contract:
        message += "- No Total Contract : Vous avez oublié de renseigner le montant du contrat\n"
    else:
        total_amount_contract = int(total_amount_contract)
        if total_amount_contract <= 0:
            message += "- Total Contract Negative : Le montant du contrat doit être positif\n"

        # Controle de la valeur du champs "amount_be_paid"
        if not amount_be_paid:
            message += "- No Amount Be Paid : Vous avez oublié de renseigner le montant restant à payer\n"
        else:
            amount_be_paid = int(amount_be_paid)
            if amount_be_paid < 0:
                message += "- Amount Be Paid Negative : Le montant restant à payer ne peux pas être negatif\n"
            elif amount_be_paid > total_amount_contract:
                message += "- Amount Be Paid Excessive: Le montant restant à payer ne peux pas être supérieur au contrat\n"

    # Controle de la valeur du champs "signature_contract"
    if not signature_contract:
        message += "- No Signature : Vous avez oublié de renseigner la signature\n"

    if message == "":
        contract = {"client": client,
                    "total_amount_contract": total_amount_contract,
                    "amount_be_paid": amount_be_paid,
                    "signature_contract": signature_contract}
    else:
        contract = ""

    return contract, message
