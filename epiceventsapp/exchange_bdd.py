import mysql.connector
import configparser
import hashlib
import binascii

# Créer un objet ConfigParser et lire le fichier de config
config = configparser.ConfigParser()
config.read('config.ini')


def connexion_epicevents_bdd(config_section):
    db = mysql.connector.connect(
        host=config[config_section]['host'],
        user=config[config_section]['user'],
        password=config[config_section]['password'],
        database=config[config_section]['database']
    )
    cursor = db.cursor()
    return db, cursor


def deconnexion_epicevents_bdd(cursor, db):
    cursor.close()
    db.close()
    return


def add_user(user):
    message = ""
    db, cursor = connexion_epicevents_bdd("database")
    # Préparez la requête SQL
    query = """
            INSERT INTO collaborateur (surname, name, department, identifiant, password, salt)
            VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (user['surname'], user['name'], user['department'], user['identifiant'], user['password'], user['salt'])
    # Essaye d'executer la requête SQL:
    try:
        cursor.execute(query, values)
        db.commit()
    except mysql.connector.IntegrityError:
        message = "Double Identifiant : Cet identifiant est déjà utilisé"

    deconnexion_epicevents_bdd(cursor, db)
    return message


def control_user(identifiant, password):
    message = ""
    db, cursor = connexion_epicevents_bdd("database_identification")
    # Préparez la requête SQL
    query = """
            SELECT *
            FROM collaborateur
            WHERE identifiant = %s
    """
    value = (identifiant,)
    # Essaye d'executer la requête SQL:
    try:
        cursor.execute(query, value)
        user_result = cursor.fetchone()
        if user_result is None:
            valid_identifiant = False
            message = "- User Unknown : L'utilisateur n'est pas connu de la base de données"
        else:
            user_salt = user_result[7]
            user_password = user_result[5]
            password_encode = password.encode('utf-8')
            hashed_password = binascii.hexlify(hashlib.pbkdf2_hmac('sha256',
                                                                   password_encode,
                                                                   user_salt,
                                                                   100000))
            password_decode = hashed_password.decode('utf-8')
            # Si le mot de passe est correct
            if password_decode == user_password:
                valid_identifiant = True
            # Si le mot de passe est incorrect
            else:
                valid_identifiant = False
                message = "- Wrong Password : L'identifiant est connu mais le mot de passe est incorrect"
    except mysql.connector.Error as err:
        valid_identifiant = False
        message = f"Erreur {err.errno}"

    deconnexion_epicevents_bdd(cursor, db)
    return valid_identifiant, message
