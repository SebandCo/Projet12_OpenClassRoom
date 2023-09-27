import mysql.connector
import configparser

# Créer un objet ConfigParser et lire le fichier de config
config = configparser.ConfigParser()
config.read('config.ini')

# Déclaration des champs d'accès à la base de données
CONFIG_HOST = config['database']['host']
CONFIG_USER = config['database']['user']
CONFIG_PASSWORD = config['database']['password']
CONFIG_DATABASE = config['database']['database']


def connexion_epicevents_bdd():
    db = mysql.connector.connect(
        host=CONFIG_HOST,
        user=CONFIG_USER,
        password=CONFIG_PASSWORD,
        database=CONFIG_DATABASE
    )
    cursor = db.cursor()
    return db, cursor


def deconnexion_epicevents_bdd(cursor, db):
    cursor.close()
    db.close()
    return


def control_user(identifiant, password):
    valid_identifiant = False
    error_message = ""
    try:
        connexion_epicevents_bdd()
        valid_identifiant = True
    except mysql.connector.errors.ProgrammingError as err:
        valid_identifiant = False
        if err.errno == 1045:
            error_message = "Erreur 1045 : L'utilisateur n'est pas connu de la base de données ou le mot de passe est incorrect"
        else:
            error_message = f"Erreur {err.errno}"

    return valid_identifiant, error_message


def creation_user(user):
    pass
