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


# ------------------------------------------------------------------
# Partie des clients
# ------------------------------------------------------------------
def add_client(client):
    message = ""
    db, cursor = connexion_epicevents_bdd("database")
    # Préparez la requête SQL
    query = """
            INSERT INTO client (surname, name, email, phone_number, collaborateur_id, enterprise_id)
            VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (client['surname'],
              client['name'],
              client['email'],
              client['phone_number'],
              client['collaborateur'],
              client['enterprise'])
    # Essaye d'executer la requête SQL:
    try:
        cursor.execute(query, values)
        db.commit()
    except mysql.connector.IntegrityError:
        message = "Double Enterprise : Cette entreprise existe déjà"

    deconnexion_epicevents_bdd(cursor, db)
    return message


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
        results = [{'email': row[0],
                    'complet_name': row[1],
                    'phone_number': row[2],
                    'creation_date': row[3],
                    'last_update': row[4],
                    'collaborateur': row[5],
                    'enterprise': row[6]}for row in cursor.fetchall()]
    except mysql.connector.Error as err:
        results = ""
        message = f"Erreur {err.errno} : La requete n'a pas abouti"

    deconnexion_epicevents_bdd(cursor, db)

    return results, message


# ------------------------------------------------------------------
# Partie des événements
# ------------------------------------------------------------------
def event_extract():
    db, cursor = connexion_epicevents_bdd("database_select_only")
    message = ""
    query = """
    SELECT event.id,
    event.name,
    event.contract_id,
    client.complet_name AS complet_name,
    client.email AS email,
    client.phone_number AS phone_number,
    event.event_date_start,
    event.event_date_end,
    event.support_contact,
    event.location,
    event.attendees,
    event.notes
    FROM event
    JOIN client on event.client_id = client.id
    """
    # Essaye d'executer la requête SQL:
    try:
        cursor.execute(query)
        # Transforme le result en dictionnaire pour facilité la lecture
        results = [{'id': row[0],
                    'name': row[1],
                    'contract_id': row[2],
                    'complet_name': row[3],
                    'email': row[4],
                    'phone_number': row[5],
                    'date_start': row[6],
                    'date_end': row[7],
                    'support_contact': row[8],
                    'location': row[9],
                    'attendees': row[10],
                    'notes': row[11]}for row in cursor.fetchall()]
    except mysql.connector.Error as err:
        results = ""
        message = f"Erreur {err.errno} : La requete n'a pas abouti"

    deconnexion_epicevents_bdd(cursor, db)

    return results, message


# ------------------------------------------------------------------
# Partie des entreprises
# ------------------------------------------------------------------
def add_enterprise(enterprise):
    message = ""
    db, cursor = connexion_epicevents_bdd("database")
    # Préparez la requête SQL
    query = """
            INSERT INTO enterprise (name)
            VALUES (%s)
    """
    values = (enterprise['name'], )
    # Essaye d'executer la requête SQL:
    try:
        cursor.execute(query, values)
        db.commit()
    except mysql.connector.IntegrityError:
        message = "Double Enterprise : Cette entreprise existe déjà"

    deconnexion_epicevents_bdd(cursor, db)
    return message


def enterprise_extract():
    db, cursor = connexion_epicevents_bdd("database_select_only")
    message = ""
    query = """
    SELECT enterprise.id,
    enterprise.name,
    enterprise.creation_date
    FROM enterprise
    """
    # Essaye d'executer la requête SQL:
    try:
        cursor.execute(query)
        # Transforme le result en dictionnaire pour facilité la lecture
        results = [{'id': row[0],
                    'name': row[1],
                    'creation_date': row[2]}for row in cursor.fetchall()]
    except mysql.connector.Error as err:
        results = ""
        message = f"Erreur {err.errno} : La requete n'a pas abouti"

    deconnexion_epicevents_bdd(cursor, db)

    return results, message


# ------------------------------------------------------------------
# Partie des contrats
# ------------------------------------------------------------------
def contract_extract():
    db, cursor = connexion_epicevents_bdd("database_select_only")
    message = ""
    query = """
    SELECT contract.total_amount_contract,
    contract.amount_be_paid,
    contract.signature_contract,
    client.complet_name AS complet_name
    FROM contract
    JOIN client on contract.client_id = client.id
    """
    # Essaye d'executer la requête SQL:
    try:
        cursor.execute(query)
        # Transforme le result en dictionnaire pour facilité la lecture
        results = [{'total': row[0],
                    'amount_be_paid': row[1],
                    'signature': row[2],
                    'client': row[3]}for row in cursor.fetchall()]
    except mysql.connector.Error as err:
        results = ""
        message = f"Erreur {err.errno} : La requete n'a pas abouti"

    deconnexion_epicevents_bdd(cursor, db)

    return results, message


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
        results = ""
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
    values = (user['surname'],
              user['name'],
              user['department'],
              user['identifiant'],
              user['password'],
              user['salt'])
    # Essaye d'executer la requête SQL:
    try:
        cursor.execute(query, values)
        db.commit()
    except mysql.connector.IntegrityError:
        message = "Double Identifiant : Cet identifiant est déjà utilisé"

    deconnexion_epicevents_bdd(cursor, db)
    return message


def control_user_bdd(identifiant):
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
