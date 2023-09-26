import mysql.connector
import exchange_bdd as bdd


# Class qui permet de générer le comportement de l'erreur spécifique 1045
class CustomProgrammingError1045(mysql.connector.errors.ProgrammingError):
    def __init__(self, message=""):
        self.errno = 1045
        self.msg = message


# Class qui permet de générer le comportement une erreur diverse
class CustomProgrammingError4321(mysql.connector.errors.ProgrammingError):
    def __init__(self, message=""):
        self.errno = 4321
        self.msg = message


# Test lorsque l'utilisateur est valide
def test_connexion_user(mocker):
    # Mock de la fonction 'connexion_epicevents_bdd'
    # Avec un connexion réussi donc valid_user = True et error_message est vide
    mocker.patch('exchange_bdd.connexion_epicevents_bdd', return_value=(True, None))

    valid_user, error_message = bdd.control_user('testuser', 'testpassword')

    assert valid_user is True
    assert error_message == ""


# Test lorsque l'utilisateur n'est pas valide
def test_not_connexion_user(mocker):
    # Mock de la fonction 'connexion_epicevents_bdd' pour forcer la lever une exception 1045
    # Via la classe CustomProgrammingError1045
    mocker.patch('exchange_bdd.connexion_epicevents_bdd',
                 side_effect=CustomProgrammingError1045("Access denied for user"))

    valid_user, error_message = bdd.control_user('invaliduser', 'invalidpassword')
    expected_value = "Erreur 1045"

    assert valid_user is False
    assert expected_value in error_message


# Test en cas de retour d'erreur
def test_not_connexion_error(mocker):
    # Mock de la fonction 'connexion_epicevents_bdd' pour forcer la lever une exception
    # Via la classe CustomProgrammingError4321
    mocker.patch('exchange_bdd.connexion_epicevents_bdd',
                 side_effect=CustomProgrammingError4321("Access denied for user"))

    valid_user, error_message = bdd.control_user('invaliduser', 'invalidpassword')
    expected_value = "Erreur 4321"

    assert valid_user is False
    assert expected_value in error_message
