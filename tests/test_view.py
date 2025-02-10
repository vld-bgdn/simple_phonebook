import pytest

from typing import List
from _pytest.capture import CaptureFixture
from _pytest.monkeypatch import MonkeyPatch
from view import View
from model import Contact

import text_en as text

"""
Common args for test fuctions:
    monkeypatch: Pytest fixture for modifying functions/attributes
    user_input: String to simulate user input
    is_edit: Boolean flag indicating edit mode
    inputs: List of input strings to test
    expected: Expected boolean result
    capsys: Pytest fixture to capture stdout/stderr

    test_first_contact: Fixture providing test Contact instance
"""


def test_show_message(capsys: CaptureFixture[str]) -> None:
    """Test displaying a message to the user."""
    message = "Test message"
    View.show_message(message)
    captured = capsys.readouterr()
    assert captured.out == f"\n{message}\n"


def test_show_menu(monkeypatch: MonkeyPatch) -> None:
    """Test menu display and option selection."""
    monkeypatch.setattr('builtins.input', lambda _: "1")
    result = View.show_menu()
    assert result == "1"


def test_show_contacts_empty(capsys: CaptureFixture[str]) -> None:
    """Test displaying empty contact list."""
    View.show_contacts([])
    captured = capsys.readouterr()
    assert text.contact_found_error in captured.out


def test_show_contacts_with_data(capsys: CaptureFixture[str],
                                 test_first_contact: Contact) -> None:
    """Test displaying contacts with data."""
    contacts = [test_first_contact]
    View.show_contacts(contacts)
    captured = capsys.readouterr()
    assert test_first_contact.name in captured.out
    assert test_first_contact.phone in captured.out
    assert test_first_contact.comment in captured.out


@pytest.mark.parametrize("is_edit,inputs", [
    (False, ["Test Name", "1234567890", "Test Comment"]),
    (True, ["Test Name", "1234567890", "Test Comment"])
])
def test_get_contact_input(monkeypatch: MonkeyPatch,
                           is_edit: bool,
                           inputs: List[str]) -> None:
    """Test getting contact information from user input."""
    input_values = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_values))
    result = View.get_contact_input(is_edit)
    assert result == tuple(inputs)


def test_get_contact_input_empty_fields(monkeypatch: MonkeyPatch) -> None:
    """Test handling of empty input fields."""
    input_values = ["", "Test Name", "", "1234567890", "Test Comment"]
    input_iterator = iter(input_values)
    monkeypatch.setattr('builtins.input', lambda _: next(input_iterator))
    result = View.get_contact_input(False)
    assert result == ("Test Name", "1234567890", "Test Comment")


def test_get_search_term(monkeypatch: MonkeyPatch) -> None:
    """Test getting search term from user."""
    test_term = "Test Search"
    monkeypatch.setattr('builtins.input', lambda _: test_term)
    result = View.get_search_term()
    assert result == test_term


def test_get_contact_id_valid(monkeypatch: MonkeyPatch) -> None:
    """Test getting valid contact ID from user."""
    monkeypatch.setattr('builtins.input', lambda _: "1")
    result = View.get_contact_id()
    assert result == 1


def test_get_contact_id_invalid_then_valid(monkeypatch: MonkeyPatch) -> None:
    """Test handling invalid then valid contact ID input."""
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
def test_confirm_action(monkeypatch: MonkeyPatch,
                        user_input: str,
                        expected: bool) -> None:
    """Test action confirmation dialog."""
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    result = View.confirm_action()
    assert result == expected
