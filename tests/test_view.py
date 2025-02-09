import pytest

from view import View

import text_en as text
import tests.test_config as config


def test_show_message(capsys):
    message = "Test message"
    View.show_message(message)
    captured = capsys.readouterr()
    assert captured.out == f"\n{message}\n"

def test_show_menu(monkeypatch):
    # Mock the input function to return "1"
    monkeypatch.setattr('builtins.input', lambda _: "1")
    result = View.show_menu()
    assert result == "1"

def test_show_contacts_empty(capsys):
    View.show_contacts([])
    captured = capsys.readouterr()
    assert text.contact_found_error in captured.out

def test_show_contacts_with_data(capsys):
    contacts = [config.test_first_contact]
    View.show_contacts(contacts)
    captured = capsys.readouterr()
    assert config.TEST_FIRST_CONTACT_DATA["name"] in captured.out
    assert config.TEST_FIRST_CONTACT_DATA["phone"] in captured.out
    assert config.TEST_FIRST_CONTACT_DATA["comment"] in captured.out

@pytest.mark.parametrize("is_edit,inputs", [
    (False, [config.TEST_FIRST_CONTACT_DATA["name"],
             config.TEST_FIRST_CONTACT_DATA["phone"],
             config.TEST_FIRST_CONTACT_DATA["comment"]
            ]),
    (True, [config.TEST_FIRST_CONTACT_DATA["name"],
            config.TEST_FIRST_CONTACT_DATA["phone"],
            config.TEST_FIRST_CONTACT_DATA["comment"]
            ])
])
def test_get_contact_input(monkeypatch, is_edit, inputs):
    input_values = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_values))
    result = View.get_contact_input(is_edit)
    assert result == tuple(inputs)

def test_get_contact_input_empty_fields(monkeypatch):
    # Test handling of empty name and phone
    input_values = ["", config.TEST_FIRST_CONTACT_DATA["name"], "", config.TEST_FIRST_CONTACT_DATA["phone"], config.TEST_FIRST_CONTACT_DATA["comment"]]
    input_iterator = iter(input_values)
    monkeypatch.setattr('builtins.input', lambda _: next(input_iterator))
    result = View.get_contact_input(False)
    assert result == (config.TEST_FIRST_CONTACT_DATA["name"], config.TEST_FIRST_CONTACT_DATA["phone"], config.TEST_FIRST_CONTACT_DATA["comment"])

def test_get_search_term(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: config.TEST_FIRST_CONTACT_DATA["name"])
    result = View.get_search_term()
    assert result == config.TEST_FIRST_CONTACT_DATA["name"]

def test_get_contact_id_valid(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "1")
    result = View.get_contact_id()
    assert result == 1

def test_get_contact_id_invalid_then_valid(monkeypatch):
    input_values = ["abc", "1"]
    input_iterator = iter(input_values)
    monkeypatch.setattr('builtins.input', lambda _: next(input_iterator))
    result = View.get_contact_id()
    assert result == 1

@pytest.mark.parametrize("user_input,expected", [
    ("y", True),
    ("Y", True),
    ("n", False),
    ("N", False),
    ("anything", False)
])
def test_confirm_action(monkeypatch, user_input, expected):
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    result = View.confirm_action()
    assert result == expected
