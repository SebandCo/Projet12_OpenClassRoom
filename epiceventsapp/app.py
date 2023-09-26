from flask import Flask, render_template, request
import exchange_bdd as bdd


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/acceuil", methods=["POST"])
def acceuil():
    user = request.form.get("user")
    # Manque chiffrement du mot de passe
    password = request.form.get("password")
    valid_user, error_message = bdd.control_user(user, password)
    if valid_user:
        enterprises = bdd.browse_enterprise()
        return str(enterprises)
    else:
        return render_template("index.html", message=error_message)


if __name__ == '__main__':
    app.run(debug=True)
