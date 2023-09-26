import mysql.connector

HOST = "localhost"
DATABASE = "epicevents"


def connexion_epicevents_bdd(HOST, user, password, DATABASE):
    db = mysql.connector.connect(
        host=HOST,
        user=user,
        password=password,
        database=DATABASE
    )
    cursor = db.cursor()
    return db, cursor


def deconnexion_epicevents_bdd(cursor, db):
    cursor.close()
    db.close()
    return


def control_user(user, password):
    valid_user = False
    error_message = ""
    try:
        connexion_epicevents_bdd(HOST, user, password, DATABASE)
        valid_user = True
    except mysql.connector.errors.ProgrammingError as err:
        valid_user = False
        if err.errno == 1045:
            error_message = "Erreur 1045 : L'utilisateur n'est pas connu de la base de données ou le mot de passe est incorrect"
        else:
            error_message = f"Erreur {err.errno}"

    return valid_user, error_message


def browse_enterprise():
    # A supprimer quand page de connexion valide et fonctionnel
    user = "adminepicevents"
    password = "mdpepicevents"

    db, cursor = connexion_epicevents_bdd(HOST, user, password, DATABASE)
    cursor.execute("SELECT name FROM enterprise")
    enterprises = cursor.fetchall()
    deconnexion_epicevents_bdd(cursor, db)
    return enterprises
