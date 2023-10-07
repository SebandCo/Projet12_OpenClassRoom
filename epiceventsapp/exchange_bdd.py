import mysql.connector
import configparser


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


def client_extract():
    db, cursor = connexion_epicevents_bdd("database_select_only")
    message = ""
    query = """
    SELECT client.email,
    client.complet_name,
    client.phone_number,
    client.creation_date,
    client.last_update,
    collaborateur.complet_name AS collaborateur_complet_name,
    enterprise.name AS enterprise_name
    FROM client
    JOIN collaborateur on client.collaborateur_id = collaborateur.id
    JOIN enterprise on client.enterprise_id = enterprise.id
    """
    # Essaye d'executer la requête SQL:
    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except mysql.connector.Error as err:
        message = f"Erreur {err.errno} : La requete n'a pas abouti"

    deconnexion_epicevents_bdd(cursor, db)

    return results, message


def contract_extract():
    db, cursor = connexion_epicevents_bdd("database_select_only")

    deconnexion_epicevents_bdd(cursor, db)
    return


def event_extract():
    db, cursor = connexion_epicevents_bdd("database_select_only")

    deconnexion_epicevents_bdd(cursor, db)
    return


# ------------------------------------------------------------------
# Partie des utilisateurs
# ------------------------------------------------------------------
def user_extract():
    db, cursor = connexion_epicevents_bdd("database_select_only")
    message = ""
    query = """
    SELECT collaborateur.complet_name,
    collaborateur.department,
    collaborateur.identifiant
    FROM collaborateur
    """
    # Essaye d'executer la requête SQL:
    try:
        cursor.execute(query)
        # Transforme le result en dictionnaire pour facilité la lecture
        results = [{'complet_name': row[0],
                    'department': row[1],
                    'identifiant': row[2]}for row in cursor.fetchall()]
    except mysql.connector.Error as err:
        message = f"Erreur {err.errno} : La requete n'a pas abouti"

    deconnexion_epicevents_bdd(cursor, db)

    return results, message


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


def control_user_bdd(identifiant, password):
    message = ""
    db, cursor = connexion_epicevents_bdd("database_select_only")
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

    except mysql.connector.Error as err:
        user_result = None
        message = f"Erreur {err.errno}"

    deconnexion_epicevents_bdd(cursor, db)
    return user_result, message
