from user_app import user_creation, MAX_LEN_VALUE
import hashlib
import binascii


def test_good_user(mock_user_request):
    user, message = user_creation(mock_user_request)
    expected_value_user = mock_user_request.form
    expected_value_message = ""
    password_encode = expected_value_user["password"].encode('utf-8')
    expected_value_hashed_password = binascii.hexlify(hashlib.pbkdf2_hmac('sha256',
                                                                          password_encode,
                                                                          user["salt"],
                                                                          100000))

    assert user["surname"] == expected_value_user["surname"]
    assert user["name"] == expected_value_user["name"]
    assert user["department"] == expected_value_user["department"]
    assert user["identifiant"] == expected_value_user["identifiant"]
    assert user["password"] == expected_value_hashed_password
    assert message == expected_value_message


def test_wrong_user_surname(mock_user_request):
    mock_user_request.form["surname"] = ""
    user, message = user_creation(mock_user_request)
    expected_value_message = "No Surname"
    assert user == ""
    assert expected_value_message in message

    mock_user_request.form["surname"] = "a" * (MAX_LEN_VALUE+1)
    user, message = user_creation(mock_user_request)
    expected_value_message = "Too Long Surname"
    assert user == ""
    assert expected_value_message in message


def test_wrong_user_name(mock_user_request):
    mock_user_request.form["name"] = ""
    user, message = user_creation(mock_user_request)
    expected_value_message = "No Name"
    assert user == ""
    assert expected_value_message in message

    mock_user_request.form["name"] = "a" * (MAX_LEN_VALUE+1)
    user, message = user_creation(mock_user_request)
    expected_value_message = "Too Long Name"
    assert user == ""
    assert expected_value_message in message


def test_wrong_user_department(mock_user_request):
    mock_user_request.form["department"] = ""
    user, message = user_creation(mock_user_request)
    expected_value_message = "No Department"
    assert user == ""
    assert expected_value_message in message


def test_wrong_user_identifiant(mock_user_request):
    mock_user_request.form["identifiant"] = ""
    user, message = user_creation(mock_user_request)
    expected_value_message = "No Identifiant"
    assert user == ""
    assert expected_value_message in message

    mock_user_request.form["identifiant"] = "a" * (MAX_LEN_VALUE+1)
    user, message = user_creation(mock_user_request)
    expected_value_message = "Too Long Identifiant"
    assert user == ""
    assert expected_value_message in message


def test_wrong_user_password(mock_user_request):
    mock_user_request.form["password"] = ""
    user, message = user_creation(mock_user_request)
    expected_value_message = "No Password"
    assert user == ""
    assert expected_value_message in message

    mock_user_request.form["password"] = "a" * (MAX_LEN_VALUE+1)
    user, message = user_creation(mock_user_request)
    expected_value_message = "Too Long Password"
    assert user == ""
    assert expected_value_message in message

    mock_user_request.form["password"] = "different_password"
    user, message = user_creation(mock_user_request)
    expected_value_message = "Different Password"
    assert user == ""
    assert expected_value_message in message
