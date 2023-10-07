from client_app import client_creation, MAX_LEN_VALUE, MAX_LEN_VALUE_PHONE, MAX_LEN_VALUE_EMAIL


def test_good_client(mock_client_request):
    client, message = client_creation(mock_client_request)
    expected_value_client = mock_client_request.form
    expected_value_message = ""

    assert client["surname"] == expected_value_client["surname"]
    assert client["name"] == expected_value_client["name"]
    assert client["email"] == expected_value_client["email"]
    assert client["phone_number"] == expected_value_client["phone_number"]
    assert client["collaborateur"] == expected_value_client["collaborateur"]
    assert client["enterprise"] == expected_value_client["enterprise"]
    assert message == expected_value_message


def test_wrong_client_surname(mock_client_request):
    mock_client_request.form["surname"] = ""
    user, message = client_creation(mock_client_request)
    expected_value_message = "No Surname"
    assert user == ""
    assert expected_value_message in message

    mock_client_request.form["surname"] = "a" * (MAX_LEN_VALUE+1)
    user, message = client_creation(mock_client_request)
    expected_value_message = "Too Long Surname"
    assert user == ""
    assert expected_value_message in message


def test_wrong_client_name(mock_client_request):
    mock_client_request.form["name"] = ""
    user, message = client_creation(mock_client_request)
    expected_value_message = "No Name"
    assert user == ""
    assert expected_value_message in message

    mock_client_request.form["name"] = "a" * (MAX_LEN_VALUE+1)
    user, message = client_creation(mock_client_request)
    expected_value_message = "Too Long Name"
    assert user == ""
    assert expected_value_message in message


def test_wrong_client_email(mock_client_request):
    mock_client_request.form["email"] = ""
    user, message = client_creation(mock_client_request)
    expected_value_message = "No Email"
    assert user == ""
    assert expected_value_message in message

    mock_client_request.form["email"] = "a" * (MAX_LEN_VALUE_EMAIL+1)
    user, message = client_creation(mock_client_request)
    expected_value_message = "Too Long Email"
    assert user == ""
    assert expected_value_message in message


def test_wrong_client_phone_number(mock_client_request):
    mock_client_request.form["phone_number"] = ""
    user, message = client_creation(mock_client_request)
    expected_value_message = "No Phone"
    assert user == ""
    assert expected_value_message in message

    mock_client_request.form["phone_number"] = "a" * (MAX_LEN_VALUE_PHONE+1)
    user, message = client_creation(mock_client_request)
    expected_value_message = "Too Long Phone"
    assert user == ""
    assert expected_value_message in message


def test_wrong_client_enterprise(mock_client_request):
    mock_client_request.form["enterprise"] = ""
    user, message = client_creation(mock_client_request)
    expected_value_message = "No Enterprise"
    assert user == ""
    assert expected_value_message in message
