from flask import Flask, render_template, request, session, redirect, url_for
import exchange_bdd as bdd
import user_app as userapp
import enterprise_app as enterpriseapp
import client_app as clientapp
import event_app as eventapp
import contract_app as contractapp
from role_decorator import requires_roles, login_required

app = Flask(__name__)
# remplacer motdepassesecret par votre mot de passe
app.secret_key = "motdepassesecret"

MESSAGEREDIRECT = "No Authorisation : Vous n'avez pas les droits nécessaires pour accéder à cette page."


# Permet d'envoyer session par défault pour chaque template
@app.context_processor
def inject_session():
    return dict(session=session)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/acceuil", methods=["POST"])
def acceuil():
    identifiant = request.form.get("identifiant")
    password = request.form.get("password")
    valid_identifiant, error_message = userapp.control_user(identifiant, password)
    if valid_identifiant:
        return render_template("home.html")
    else:
        return render_template("index.html", message=error_message)


@app.route("/home")
@login_required
def home():
    return render_template("home.html")


@app.route('/logout')
def logout():
    session.pop('user_role', None)
    return redirect(url_for('index'))


# ------------------------------------------------------------------
# Chemin des événements - Menu - Accès - Création - Roles
# ------------------------------------------------------------------
@app.route("/event_display")
@login_required
def event_display():
    results, message = bdd.event_extract()
    if len(message) > 0:
        return render_template("event_templates/event_home.html", message=message)
    else:
        return render_template("event_templates/event_display.html", liste_event=results)


@app.route("/event_creation", methods=["POST", "GET"])
@login_required
def event_creation():
    if request.method == "POST":
        if session.get('user_role') not in ["commercial"]:
            # Controle que les données saisies sont correctes
            event, message_request = eventapp.event_creation(request)
            if len(message_request) > 0:
                results_contract, message_enterprise = bdd.enterprise_extract()
                message_request += message_enterprise
                results_client, message_client = bdd.client_extract()
                message_request += message_client
                return render_template("event_templates/event_creation.html",
                                       liste_contract=results_contract,
                                       liste_client=results_client,
                                       message=message_request)
            else:
                message_bdd = bdd.add_event(event)
                if message_bdd == "":
                    message = f"L'événement' {event['name']} a été rajouté à la base de données"
                    return render_template("event_templates/event_home.html", message=message)
                else:
                    results_contract, message_enterprise = bdd.enterprise_extract()
                    message_request += message_enterprise
                    results_client, message_client = bdd.client_extract()
                    message_request += message_client
                    return render_template("event_templates/event_creation.html",
                                           liste_contract=results_contract,
                                           liste_client=results_client,
                                           message=message_bdd)
        else:
            return render_template("home.html", message=MESSAGEREDIRECT)
    elif request.method == "GET":
        results_contract, message = bdd.contract_extract()
        if len(message) > 0:
            return render_template("event_templates/event_home.html", message=message)
        else:
            results_client, message = bdd.client_extract()
            if len(message) > 0:
                return render_template("event_templates/event_home.html", message=message)
            else:
                print(results_contract)
                print(results_client)
                return render_template("event_templates/event_creation.html",
                                       liste_contract=results_contract,
                                       liste_client=results_client)


@app.route("/event_home")
@login_required
def event_home():
    return render_template("event_templates/event_home.html")


# ------------------------------------------------------------------
# Chemin des clients - Menu - Accès - Création - Roles
# ------------------------------------------------------------------
@app.route("/client_display")
@login_required
def client_display():
    results, message = bdd.client_extract()
    if len(message) > 0:
        return render_template("client_templates/client_home.html", message=message)
    else:
        return render_template("client_templates/client_display.html", liste_client=results)


@app.route("/client_creation", methods=["POST", "GET"])
@login_required
def client_creation():
    if request.method == "POST":
        if session.get('user_role') not in ["commercial"]:
            # Controle que les données saisies sont correctes
            client, message_request = clientapp.client_creation(request)
            if len(message_request) > 0:
                results, message_extract = bdd.enterprise_extract()
                message_request += message_extract
                return render_template("client_templates/client_creation.html", liste_entreprise=results, message=message_request)
            else:
                message_bdd = bdd.add_client(client)
                if message_bdd == "":
                    message = f"Le client {client['surname']}, {client['name']} a été rajouté à la base de données"
                    return render_template("client_templates/client_home.html", message=message)
                else:
                    results, message_extract = bdd.enterprise_extract()
                    message += message_extract
                    return render_template("client_templates/client_creation.html", liste_entreprise=results, message=message_bdd)
        else:
            return render_template("home.html", message=MESSAGEREDIRECT)
    elif request.method == "GET":
        results, message = bdd.enterprise_extract()
        if len(message) > 0:
            return render_template("client_templates/client_home.html", message=message)
        else:
            return render_template("client_templates/client_creation.html", liste_entreprise=results)


@app.route("/client_home")
@login_required
def client_home():
    return render_template("client_templates/client_home.html")


# ------------------------------------------------------------------
# Chemin des contrats - Menu - Accès - Création - Roles
# ------------------------------------------------------------------
@app.route("/contract_home")
@login_required
def contract_home():
    return render_template("contract_templates/contract_home.html")


@app.route("/contract_creation", methods=["POST", "GET"])
@login_required
def contract_creation():
    if request.method == "POST":
        if session.get('user_role') not in ["management"]:
            # Controle que les données saisies sont correctes
            contract, message_request = contractapp.contract_creation(request)
            if len(message_request) > 0:
                results_client, message_extract = bdd.client_extract()
                message_request += message_extract
                return render_template("contract_templates/contract_creation.html",
                                       liste_client=results_client,
                                       message=message_request)
            else:
                # Controle que l'utilisateur a été correctement ajouté à la base de donnée
                message_bdd = bdd.add_contract(contract)
                if message_bdd == "":
                    message = "Le contrat a été rajouté à la base de données"
                    return render_template("contract_templates/contract_home.html", message=message)
                else:
                    results_client, message_extract = bdd.client_extract()
                    message_request += message_extract
                    return render_template("contract_templates/contract_creation.html",
                                           liste_client=results_client,
                                           message=message_bdd)
        else:
            return render_template("home.html", message=MESSAGEREDIRECT)
    elif request.method == "GET":
        results_client, message = bdd.client_extract()
        if len(message) > 0:
            return render_template("contract_templates/contract_home.html", message=message)
        else:
            return render_template("contract_templates/contract_creation.html", liste_client=results_client)


@app.route("/contract_display")
@login_required
def contract_display():
    results, message = bdd.contract_extract()
    if len(message) > 0:
        return render_template("contract_templates/contract_home.html", message=message)
    else:
        return render_template("contract_templates/contract_display.html", liste_contract=results)


# ------------------------------------------------------------------
# Chemin des entreprises - Menu - Accès - Création - Roles
# ------------------------------------------------------------------
@app.route("/enterprise_home")
@login_required
def enterprise_home():
    return render_template("enterprise_templates/enterprise_home.html")


@app.route("/enterprise_display")
@login_required
def enterprise_display():
    results, message = bdd.enterprise_extract()
    if len(message) > 0:
        return render_template("enterprise_templates/enterprise_home.html", message=message)
    else:
        return render_template("enterprise_templates/enterprise_display.html", liste_entreprise=results)


@app.route("/enterprise_creation", methods=["POST", "GET"])
@login_required
def enterprise_creation():
    if request.method == "POST":
        if session.get('user_role') not in ["commercial"]:
            # Controle que les données saisies sont correctes
            enterprise, message_request = enterpriseapp.enterprise_creation(request)
            if len(message_request) > 0:
                return render_template("enterprise_templates/enterprise_creation.html", message=message_request)
            else:
                message_bdd = bdd.add_enterprise(enterprise)
                if message_bdd == "":
                    message = f"L'entreprise {enterprise['name']} a été rajouté à la base de données"
                    return render_template("enterprise_templates/enterprise_home.html", message=message)
                else:
                    return render_template("enterprise_templates/enterprise_creation.html", message=message_bdd)
        else:
            return render_template("home.html", message=MESSAGEREDIRECT)
    elif request.method == "GET":
        return render_template("enterprise_templates/enterprise_creation.html")


# ------------------------------------------------------------------
# Chemin des utilisateurs - Menu - Accès - Création - Roles
# ------------------------------------------------------------------
@app.route("/user_home")
@login_required
@requires_roles('management')
def user_home():
    return render_template("user_templates/user_home.html")


@app.route("/user_display")
@login_required
@requires_roles('management')
def user_display():
    results, message = bdd.user_extract()
    if len(message) > 0:
        return render_template("user_templates/user_home.html", message=message)
    else:
        return render_template("user_templates/user_display.html", liste_user=results)


@app.route("/user_creation", methods=["POST", "GET"])
@login_required
@requires_roles('management')
def user_creation():
    if request.method == "POST":
        # Controle que les données saisies sont correctes
        user, message_request = userapp.user_creation(request)
        if len(message_request) > 0:
            return render_template("user_templates/user_creation.html", message=message_request)
        else:
            message_bdd = bdd.add_user(user)
            if message_bdd == "":
                message = f"L'utilisateur {user['surname']}, {user['name']} a été rajouté à la base de données"
                return render_template("user_templates/user_home.html", message=message)
            else:
                return render_template("user_templates/user_creation.html", message=message_bdd)

    return render_template("user_templates/user_creation.html")


# ------------------------------------------------------------------
# Autres
# ------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
