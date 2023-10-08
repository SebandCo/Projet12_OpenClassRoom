from contract_app import contract_creation


def test_good_contract(mock_contract_request):
    contract, message = contract_creation(mock_contract_request)
    expected_value_contract = mock_contract_request.form
    expected_value_message = ""

    assert contract["client"] == expected_value_contract["client"]
    assert contract["total_amount_contract"] == expected_value_contract["total_amount_contract"]
    assert contract["amount_be_paid"] == expected_value_contract["amount_be_paid"]
    assert contract["signature_contract"] == expected_value_contract["signature_contract"]
    assert message == expected_value_message


def test_wrong_contract_client(mock_contract_request):
    mock_contract_request.form["client"] = ""
    contract, message = contract_creation(mock_contract_request)
    expected_value_message = "No Client"
    assert contract == ""
    assert expected_value_message in message


def test_wrong_contract_total_amount(mock_contract_request):
    mock_contract_request.form["total_amount_contract"] = None
    contract, message = contract_creation(mock_contract_request)
    expected_value_message = "No Total Contract"
    assert contract == ""
    assert expected_value_message in message

    mock_contract_request.form["total_amount_contract"] = -1000
    contract, message = contract_creation(mock_contract_request)
    expected_value_message = "Total Contract Negative"
    assert contract == ""
    assert expected_value_message in message


def test_wrong_contract_be_paid(mock_contract_request):
    mock_contract_request.form["amount_be_paid"] = None
    contract, message = contract_creation(mock_contract_request)
    expected_value_message = "No Amount Be Paid"
    assert contract == ""
    assert expected_value_message in message

    mock_contract_request.form["amount_be_paid"] = -1000
    contract, message = contract_creation(mock_contract_request)
    expected_value_message = "Amount Be Paid Negative"
    assert contract == ""
    assert expected_value_message in message

    mock_contract_request.form["amount_be_paid"] = mock_contract_request.form["total_amount_contract"] + 1
    contract, message = contract_creation(mock_contract_request)
    expected_value_message = "Amount Be Paid Excessive"
    assert contract == ""
    assert expected_value_message in message


def test_wrong_contract_signature(mock_contract_request):
    mock_contract_request.form["signature_contract"] = ""
    contract, message = contract_creation(mock_contract_request)
    expected_value_message = "No Signature"
    assert contract == ""
    assert expected_value_message in message
