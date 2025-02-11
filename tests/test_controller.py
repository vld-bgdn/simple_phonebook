import pytest

from typing import Any
from controller import Phonebook
from model import Contact

import text_en as text

"""
Common args for test fuctions:
    phonebook: Fixture providing test Phonebook instance
    mocker: pytest-mock fixture

    test_first_contact: Fixture providing first test Contact instance
    test_second_contact: Fixture providing second test Contact instance
    test_contact_tuple: Fixture providing test contact data tuple
    test_second_updated_contact: Fixture providing updated test Contact instance
"""


class TestPhonebook:
    @pytest.fixture
    def phonebook(self, mocker: Any) -> Phonebook:
        """Create a Phonebook instance with mocked dependencies.
        Returns:
            Phonebook: Test instance with mocked dependencies
        """
        self.mock_file_handler = mocker.Mock()
        self.mock_view = mocker.Mock()
        return Phonebook(self.mock_file_handler, self.mock_view)

    def test_load_contacts(self, phonebook: Phonebook, test_first_contact: Contact) -> None:
        """Test loading contacts from file handler."""
        self.mock_file_handler.read_contacts.reset_mock()
        self.mock_file_handler.read_contacts.return_value = [test_first_contact]

        phonebook.load_contacts()

        assert phonebook.contacts == [test_first_contact]
        self.mock_file_handler.read_contacts.assert_called_once()

    def test_save_contacts_successful(self, phonebook: Phonebook) -> None:
        """Test successful contact saving operation."""
        self.mock_file_handler.write_contacts.return_value = True
        phonebook.modified = True

        phonebook.save_contacts()

        assert not phonebook.modified
        self.mock_file_handler.write_contacts.assert_called_once_with(phonebook.contacts)
        self.mock_view.show_message.assert_called_once()

    def test_save_contacts_failure(self, phonebook: Phonebook) -> None:
        """Test failed contact saving operation."""
        self.mock_file_handler.write_contacts.return_value = False
        phonebook.modified = True

        phonebook.save_contacts()

        assert phonebook.modified
        self.mock_file_handler.write_contacts.assert_called_once_with(phonebook.contacts)
        self.mock_view.show_message.assert_called_once()

    def test_get_next_id_empty_contacts(self, phonebook: Phonebook) -> None:
        """Test ID generation with empty contact list."""
        phonebook.contacts = []
        assert phonebook.get_next_id() == 1

    def test_get_next_id_with_contacts(self, phonebook: Phonebook,
                                       test_first_contact: Contact,
                                       test_second_contact: Contact) -> None:
        """Test ID generation with existing contacts."""
        phonebook.contacts = [test_first_contact, test_second_contact]
        assert phonebook.get_next_id() == 3

    def test_create_contact(self, phonebook: Phonebook,
                            mocker: Any,
                            test_first_contact_tuple: tuple) -> None:
        """Test contact creation."""
        self.mock_view.get_contact_input.return_value = test_first_contact_tuple
        phonebook.contacts = []
        mocker.patch.object(phonebook, 'get_next_id', return_value=1)

        phonebook.create_contact()

        assert len(phonebook.contacts) == 1
        assert phonebook.modified
        self.mock_view.show_message.assert_called_once_with(text.contact_create_successful)

    def test_find_contacts(self, phonebook: Phonebook,
                           test_first_contact: Contact,
                           test_second_contact: Contact) -> None:
        """Test contact search functionality."""
        phonebook.contacts = [test_first_contact, test_second_contact]
        self.mock_view.get_search_term.return_value = test_first_contact.name

        phonebook.find_contacts()

        self.mock_view.show_contacts.assert_called_once()

    def test_edit_contact_successful(self, phonebook: Phonebook,
                                     test_second_contact: Contact,
                                     test_second_updated_contact: Contact) -> None:
        """Test successful contact editing."""
        phonebook.contacts = [test_second_contact]
        self.mock_view.get_contact_id.return_value = 2
        self.mock_view.get_contact_input.return_value = (
            test_second_updated_contact.name,
            test_second_updated_contact.phone,
            test_second_updated_contact.comment
        )

        phonebook.edit_contact()

        assert phonebook.modified
        assert phonebook.contacts[0].name == test_second_updated_contact.name
        assert phonebook.contacts[0].phone == test_second_updated_contact.phone
        assert phonebook.contacts[0].comment == test_second_updated_contact.comment

    def test_edit_contact_not_found(self, phonebook: Phonebook,
                                    test_first_contact: Contact) -> None:
        """Test editing non-existent contact."""
        phonebook.contacts = [test_first_contact]
        self.mock_view.get_contact_id.return_value = 2

        phonebook.edit_contact()

        self.mock_view.show_message.assert_called_with(
            any_string_containing(text.contact_found_error))

    def test_delete_contact_successful(self, phonebook: Phonebook,
                                       test_first_contact: Contact) -> None:
        """Test successful contact deletion."""
        phonebook.contacts = [test_first_contact]
        self.mock_view.get_contact_id.return_value = 1

        phonebook.delete_contact()

        assert len(phonebook.contacts) == 0
        assert phonebook.modified
        self.mock_view.show_message.assert_called_once()

    def test_delete_contact_not_found(self, phonebook: Phonebook,
                                      test_first_contact: Contact) -> None:
        """Test deleting non-existent contact."""
        phonebook.contacts = [test_first_contact]
        self.mock_view.get_contact_id.return_value = 2

        phonebook.delete_contact()

        assert len(phonebook.contacts) == 1
        self.mock_view.show_message.assert_called_with(
            any_string_containing(text.contact_found_error))

    def test_run_quit_without_changes(self, phonebook: Phonebook) -> None:
        """Test application exit without unsaved changes."""
        self.mock_view.show_menu.return_value = "7"
        phonebook.modified = False

        phonebook.run()

        self.mock_view.show_menu.assert_called_once()
        self.mock_view.show_message.assert_called_once()

    def test_run_quit_with_changes(self, phonebook: Phonebook) -> None:
        """Test application exit with unsaved changes."""
        self.mock_view.show_menu.return_value = "7"
        self.mock_view.confirm_action.return_value = True
        phonebook.modified = True
        self.mock_file_handler.write_contacts.return_value = True

        phonebook.run()

        self.mock_view.confirm_action.assert_called_once()
        self.mock_file_handler.write_contacts.assert_called_once()


def any_string_containing(substring: str) -> Any:
    """Helper function for partial string matching in assert calls.
    Args:
        substring: String to check for containment
    Returns:
        StringContaining: Custom matcher class instance
    """
    class StringContaining:
        def __eq__(self, other: str) -> bool:
            return substring in other
    return StringContaining()
