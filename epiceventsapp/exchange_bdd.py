import mysql.connector


def connexion_epicevents_bdd():
    db = mysql.connector.connect(
        host="localhost",
        user="adminepicevents",
        password="mdpepicevents",
        database="epicevents"
    )
    cursor = db.cursor()
    return db, cursor


def deconnexion_epicevents_bdd(cursor, db):
    cursor.close()
    db.close()
    return


def browse_enterprise():
    db, cursor = connexion_epicevents_bdd()
    cursor.execute("SELECT name FROM enterprise")
    enterprises = cursor.fetchall()
    deconnexion_epicevents_bdd(cursor, db)
    return enterprises
