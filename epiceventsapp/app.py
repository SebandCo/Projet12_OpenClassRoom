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
    # Manque chiffrement du mot de passe
    password = request.form.get("password")
    valid_identifiant, error_message = bdd.control_user(identifiant, password)
    if valid_identifiant:
        return render_template("home.html")
    else:
        return render_template("index.html", message=error_message)


@app.route("/user_home")
def user_home():
    return render_template("user_templates/user_home.html")


@app.route("/user_creation", methods=["POST"])
def user_creation():
    user = userapp.user_creation(request)
    print(user)
    return render_template("user_templates/user_creation.html")


if __name__ == '__main__':
    app.run(debug=True)
