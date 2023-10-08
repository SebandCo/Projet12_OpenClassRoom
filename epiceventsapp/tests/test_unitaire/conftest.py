import pytest
from unittest import mock
import hashlib
import binascii
import os
from datetime import date


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
def mock_contract_request():
    request = mock.Mock()
    request.form = {"client": 1,
                    "total_amount_contract": 2000,
                    "amount_be_paid": 200,
                    "signature_contract": 1}
    return request


# Création d'un mock pour l'objet request
@pytest.fixture
def mock_event_request():
    request = mock.Mock()
    request.form = {"name": "Nom de l'event",
                    "contract": 1,
                    "client": 1,
                    "event_date_start": date(2020, 1, 1),
                    "event_date_end": date(2022, 1, 1),
                    "support_contact": "Mr Smith",
                    "location": "Maison",
                    "attendees": 250,
                    "notes": "Une note comme ça"}
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
