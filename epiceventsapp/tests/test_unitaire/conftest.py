import pytest
from unittest import mock
import hashlib
import binascii
import os


# Création d'un mock pour l'objet request
@pytest.fixture
def mock_user_request():
    request = mock.Mock()
    request.form = {"surname": "Séb",
                    "name": "Super",
                    "department": "Gestion",
                    "identifiant": "Super_Séb",
                    "password": "Super_password",
                    "password2": "Super_password"}
    return request


# Création d'un mock pour l'objet request
@pytest.fixture
def mock_client_request():
    request = mock.Mock()
    request.form = {"surname": "Client",
                    "name": "Famille",
                    "email": "client@gmail.com",
                    "phone_number": "0601020304",
                    "collaborateur": 1,
                    "enterprise": 1}
    return request


# Création d'un mock pour l'objet request
@pytest.fixture
def mock_enterprise_request():
    request = mock.Mock()
    request.form = {"name": "Entreprise Test"}
    return request


# Création d'un mock pour l'objet base de donnée
@pytest.fixture
def mock_user_bdd():
    salt = os.urandom(16)
    # Transforme le mot de passe pour l'encoder
    password = "Super_password"
    password = password.encode('utf-8')
    hashed_password = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
    hashed_password = binascii.hexlify(hashed_password)
    hashed_password_decode = hashed_password.decode('utf-8')

    user = [1,
            "Séb",
            "Super",
            "Séb Super",
            "Gestion",
            hashed_password_decode,
            "Super_Séb",
            salt,
            "Super_password"]
    return user


# Création d'un mock pour l'objet base de donnée
@pytest.fixture
def mock_enterprise_bdd():
    enterprise = [1,
                  "Super Entreprise"]
    return enterprise
