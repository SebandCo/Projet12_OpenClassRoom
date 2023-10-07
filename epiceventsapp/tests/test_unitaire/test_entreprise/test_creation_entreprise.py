from enterprise_app import enterprise_creation, MAX_LEN_VALUE


def test_good_enterprise(mock_request):
    enterprise, message = enterprise_creation(mock_request)
    expected_value_enterprise = mock_request.form
    expected_value_message = ""

    assert enterprise["name"] == expected_value_enterprise["name"]
    assert message == expected_value_message


def test_wrong_enterprise_name(mock_request):
    mock_request.form["name"] = ""
    enterprise, message = enterprise_creation(mock_request)
    expected_value_message = "No Name"
    assert enterprise == ""
    assert expected_value_message in message

    mock_request.form["name"] = "a" * (MAX_LEN_VALUE+1)
    enterprise, message = enterprise_creation(mock_request)
    expected_value_message = "Too Long Name"
    assert enterprise == ""
    assert expected_value_message in message
