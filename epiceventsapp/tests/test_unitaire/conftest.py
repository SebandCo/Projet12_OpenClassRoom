import pytest
from unittest import mock
import hashlib
import binascii
import os


# Création d'un mock pour l'objet request
@pytest.fixture
def mock_request():
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
def mock_user():
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


# Création d'un mock pour l'objet request
@pytest.fixture
def mock_enterprise():
    enterprise = [1,
                  "Super Entreprise"]
    return enterprise
