from flask import Flask, render_template, request
import exchange_bdd as bdd
import user_app as userapp


app = Flask(__name__)


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


# ------------------------------------------------------------------
# Chemin des événements
# ------------------------------------------------------------------
@app.route("/event_display")
def event_display():
    results, message = bdd.event_extract()
    if len(message) > 0:
        return render_template("event_templates/event_home.html", message=message)
    else:
        return render_template("event_templates/event_display.html", liste_event=results)


@app.route("/event_home")
def event_home():
    return render_template("event_templates/event_home.html")


# ------------------------------------------------------------------
# Chemin des clients
# ------------------------------------------------------------------
@app.route("/client_display")
def client_display():
    results, message = bdd.client_extract()
    if len(message) > 0:
        return render_template("client_templates/client_home.html", message=message)
    else:
        return render_template("client_templates/client_display.html", liste_client=results)


@app.route("/client_home")
def client_home():
    return render_template("client_templates/client_home.html")


# ------------------------------------------------------------------
# Chemin des contrats
# ------------------------------------------------------------------
@app.route("/contract_home")
def contract_home():
    return render_template("contract_templates/contract_home.html")


@app.route("/contract_display")
def contract_display():
    results, message = bdd.contract_extract()
    if len(message) > 0:
        return render_template("contract_templates/contract_home.html", message=message)
    else:
        return render_template("contract_templates/contract_display.html", liste_contract=results)


# ------------------------------------------------------------------
# Chemin des entreprises
# ------------------------------------------------------------------
@app.route("/enterprise_home")
def enterprise_home():
    return render_template("enterprise_templates/enterprise_home.html")


@app.route("/enterprise_display")
def enterprise_display():
    results, message = bdd.enterprise_extract()
    if len(message) > 0:
        return render_template("enterprise_templates/enterprise_home.html", message=message)
    else:
        return render_template("enterprise_templates/enterprise_display.html", liste_entreprise=results)


# ------------------------------------------------------------------
# Chemin des utilisateurs
# ------------------------------------------------------------------
@app.route("/user_home")
def user_home():
    return render_template("user_templates/user_home.html")


@app.route("/user_display")
def user_display():
    results, message = bdd.user_extract()
    if len(message) > 0:
        return render_template("user_templates/user_home.html", message=message)
    else:
        return render_template("user_templates/user_display.html", liste_user=results)


@app.route("/user_creation", methods=["POST", "GET"])
def user_creation():
    if request.method == "POST":
        # Controle que les données saisies sont correctes
        user, message_request = userapp.user_creation(request)
        if len(message_request) > 0:
            return render_template("user_templates/user_creation.html", message=message_request)
        else:
            # Controle que l'utilisateur a été correctement ajouté à la base de donnée
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
