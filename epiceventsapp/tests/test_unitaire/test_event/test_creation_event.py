from event_app import event_creation, MAX_LEN_VALUE, MAX_LEN_VALUE_LOCATION, MAX_LEN_VALUE_NOTES
from datetime import timedelta


def test_good_event(mock_event_request):
    event, message = event_creation(mock_event_request)
    expected_value_event = mock_event_request.form
    expected_value_message = ""

    assert event["name"] == expected_value_event["name"]
    assert event["contract"] == expected_value_event["contract"]
    assert event["client"] == expected_value_event["client"]
    assert event["event_date_start"] == expected_value_event["event_date_start"]
    assert event["event_date_end"] == expected_value_event["event_date_end"]
    assert event["support_contact"] == expected_value_event["support_contact"]
    assert event["location"] == expected_value_event["location"]
    assert event["attendees"] == expected_value_event["attendees"]
    assert event["notes"] == expected_value_event["notes"]
    assert message == expected_value_message


def test_wrong_event_name(mock_event_request):
    mock_event_request.form["name"] = ""
    event, message = event_creation(mock_event_request)
    expected_value_message = "No Name"
    assert event == ""
    assert expected_value_message in message

    mock_event_request.form["name"] = "a" * (MAX_LEN_VALUE+1)
    event, message = event_creation(mock_event_request)
    expected_value_message = "Too Long Name"
    assert event == ""
    assert expected_value_message in message


def test_wrong_event_contract(mock_event_request):
    mock_event_request.form["contract"] = ""
    event, message = event_creation(mock_event_request)
    expected_value_message = "No Contract"
    assert event == ""
    assert expected_value_message in message


def test_wrong_event_client(mock_event_request):
    mock_event_request.form["client"] = ""
    event, message = event_creation(mock_event_request)
    expected_value_message = "No Client"
    assert event == ""
    assert expected_value_message in message


def test_wrong_event_date_start(mock_event_request):
    mock_event_request.form["event_date_start"] = ""
    event, message = event_creation(mock_event_request)
    expected_value_message = "No Date Start"
    assert event == ""
    assert expected_value_message in message


def test_wrong_event_date_end(mock_event_request):
    mock_event_request.form["event_date_end"] = ""
    event, message = event_creation(mock_event_request)
    expected_value_message = "No Date End"
    assert event == ""
    assert expected_value_message in message

    mock_event_request.form["event_date_end"] = mock_event_request.form["event_date_start"] - timedelta(days=1)
    event, message = event_creation(mock_event_request)
    expected_value_message = "Date Incorrect"
    assert event == ""
    assert expected_value_message in message


def test_wrong_event_support_contact(mock_event_request):
    mock_event_request.form["support_contact"] = ""
    event, message = event_creation(mock_event_request)
    expected_value_message = "No Support Contact"
    assert event == ""
    assert expected_value_message in message

    mock_event_request.form["support_contact"] = "a" * (MAX_LEN_VALUE+1)
    event, message = event_creation(mock_event_request)
    expected_value_message = "Too Long Support Contact"
    assert event == ""
    assert expected_value_message in message


def test_wrong_event_location(mock_event_request):
    mock_event_request.form["location"] = ""
    event, message = event_creation(mock_event_request)
    expected_value_message = "No Location"
    assert event == ""
    assert expected_value_message in message

    mock_event_request.form["location"] = "a" * (MAX_LEN_VALUE_LOCATION+1)
    event, message = event_creation(mock_event_request)
    expected_value_message = "Too Long Location"
    assert event == ""
    assert expected_value_message in message


def test_wrong_event_attendees(mock_event_request):
    mock_event_request.form["attendees"] = ""
    event, message = event_creation(mock_event_request)
    expected_value_message = "No Attendees"
    assert event == ""
    assert expected_value_message in message


def test_wrong_event_notes(mock_event_request):
    mock_event_request.form["notes"] = "a" * (MAX_LEN_VALUE_NOTES+1)
    event, message = event_creation(mock_event_request)
    expected_value_message = "Too Long Notes"
    assert event == ""
    assert expected_value_message in message
