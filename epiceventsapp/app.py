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
    valid_identifiant, error_message = bdd.control_user(identifiant, password)
    if valid_identifiant:
        return render_template("home.html")
    else:
        return render_template("index.html", message=error_message)


@app.route("/user_home")
def user_home():
    return render_template("user_templates/user_home.html")


@app.route("/user_creation", methods=["POST", "GET"])
def user_creation():
    if request.method == "POST":
        # Controle que les données saisies sont correctes
        user, message_request = userapp.user_creation(request)
        if len(message_request) > 0:
            return render_template("user_templates/user_creation.html", message=message_request)
        else:
            # Controle que l'utilisateur a été correctement ajouté à la base de donnée
            print(user)
            message_bdd = bdd.add_user(user)
            if message_bdd == "":
                message = f"L'utilisateur {user['surname']}, {user['name']} a été rajouté à la base de données"
                return render_template("user_templates/user_home.html", message=message)
            else:
                return render_template("user_templates/user_creation.html", message=message_bdd)

    return render_template("user_templates/user_creation.html")


if __name__ == '__main__':
    app.run(debug=True)
