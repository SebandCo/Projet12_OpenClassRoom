import pytest
import mysql.connector
import configparser
import exchange_bdd

config = configparser.ConfigParser()
config.read('config.ini')

host_config = config['database']['host']
user_config = config['database']['user']
password_config = config['database']['password']
database_config = config['database']['database']


def test_database_connection():
    try:
        db, cursor = exchange_bdd.connexion_epicevents_bdd()
        cursor = db.cursor()
        cursor.execute("SELECT 1")
    except mysql.connector.Error as error:
        pytest.fail(f"Erreur de connexion à la base de données: {error}")
