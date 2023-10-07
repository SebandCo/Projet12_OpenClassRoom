from user_app import control_user
import pytest


# Fixture pour le mock de la fonction 'connexion_epicevents_bdd'
@pytest.fixture
def mock_cursor(mocker):
    mock_db = mocker.Mock()
    mock_cursor = mocker.Mock()
    mocker.patch('exchange_bdd.connexion_epicevents_bdd', return_value=(mock_db, mock_cursor))
    return mock_cursor


# Test lorsque l'utilisateur est valide
def test_connexion_user(mock_user_bdd, mock_cursor):
    mock_cursor = mock_cursor
    mock_cursor.fetchone.return_value = mock_user_bdd

    # bdd.control_user(identifiant, password)
    valid_user, message = control_user(mock_user_bdd[7], mock_user_bdd[8])

    assert valid_user is True
    assert message == ""


# Test lorsque l'utilisateur n'est pas valide
def test_not_connexion_user(mock_user_bdd, mock_cursor):
    # Mock de la fonction 'connexion_epicevents_bdd'
    mock_cursor = mock_cursor
    mock_cursor.fetchone.return_value = None

    # bdd.control_user(identifiant, password)
    valid_user, message = control_user("Identifiant inconnu", mock_user_bdd[8])
    expected_value_message = "User Unknown"

    assert valid_user is False
    assert expected_value_message in message


# Test lorsque le mot de passe est invalide
def test_not_connexion_wrong_passworduser(mock_user_bdd, mock_cursor):
    # Mock de la fonction 'connexion_epicevents_bdd'
    mock_cursor = mock_cursor
    mock_cursor.fetchone.return_value = mock_user_bdd

    # bdd.control_user(identifiant, password)
    valid_user, message = control_user(mock_user_bdd[7], "wrong password")
    expected_value_message = "Wrong Password"

    assert valid_user is False
    assert expected_value_message in message
