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


def browse_enterprise():
    # A supprimer quand page de connexion valide et fonctionnel
    user = "adminepicevents"
    password = "mdpepicevents"

    db, cursor = connexion_epicevents_bdd(HOST, user, password, DATABASE)
    cursor.execute("SELECT name FROM enterprise")
    enterprises = cursor.fetchall()
    deconnexion_epicevents_bdd(cursor, db)
    return enterprises
