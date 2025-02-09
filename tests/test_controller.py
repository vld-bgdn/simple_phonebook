import pytest

from controller import Phonebook

import tests.test_config as config
import text_en as text


class TestPhonebook:
    @pytest.fixture
    def phonebook(self, mocker):
        self.mock_file_handler = mocker.Mock()
        self.mock_view = mocker.Mock()
        return Phonebook(self.mock_file_handler, self.mock_view)

    def test_load_contacts(self, phonebook):
        self.mock_file_handler.read_contacts.reset_mock()
        self.mock_file_handler.read_contacts.return_value = [config.test_first_contact]

        phonebook.load_contacts()

        assert phonebook.contacts == [config.test_first_contact]
        self.mock_file_handler.read_contacts.assert_called_once()

    def test_save_contacts_successful(self, phonebook):
        self.mock_file_handler.write_contacts.return_value = True
        phonebook.modified = True

        phonebook.save_contacts()

        assert not phonebook.modified
        self.mock_file_handler.write_contacts.assert_called_once_with(phonebook.contacts)
        self.mock_view.show_message.assert_called_once()

    def test_save_contacts_failure(self, phonebook):
        self.mock_file_handler.write_contacts.return_value = False
        phonebook.modified = True

        phonebook.save_contacts()

        assert phonebook.modified
        self.mock_file_handler.write_contacts.assert_called_once_with(phonebook.contacts)
        self.mock_view.show_message.assert_called_once()

    def test_get_next_id_empty_contacts(self, phonebook):
        phonebook.contacts = []
        assert phonebook.get_next_id() == 1

    def test_get_next_id_with_contacts(self, phonebook):
        phonebook.contacts = [config.test_first_contact, config.test_second_contact]
        assert phonebook.get_next_id() == 3

    def test_create_contact(self, phonebook, mocker):
        self.mock_view.get_contact_input.return_value = config.test_first_contact_tuple
        mock_contacts = mocker.Mock()
        mock_contacts.__len__ = mocker.Mock(return_value=0)
        phonebook.contacts
        mocker.patch.object(phonebook, 'get_next_id', return_value=1)
        phonebook.create_contact()

        phonebook.contacts.append.assert_called_once()
        assert phonebook.modified
        self.mock_view.show_message.assert_called_once_with(text.contact_create_successful)

    def test_find_contacts(self, phonebook):
        test_contacts = [config.test_first_contact, config.test_second_contact]

        phonebook.contacts = test_contacts
        self.mock_view.get_search_term.return_value = config.test_first_contact.name

        phonebook.find_contacts()

        self.mock_view.show_contacts.assert_called_once()

    def test_edit_contact_successful(self, phonebook):
        phonebook.contacts = [config.test_second_contact]
        self.mock_view.get_contact_id.return_value = 2
        self.mock_view.get_contact_input.return_value = (
            config.test_second_updated_contact.name,
            config.test_second_updated_contact.phone,
            config.test_second_updated_contact.comment
            )
        phonebook.edit_contact()

        assert phonebook.modified
        assert phonebook.contacts[0].name == config.test_second_updated_contact.name
        assert phonebook.contacts[0].phone == config.test_second_updated_contact.phone
        assert phonebook.contacts[0].comment == config.test_second_updated_contact.comment

    def test_edit_contact_not_found(self, phonebook):
        phonebook.contacts = [config.test_first_contact]
        self.mock_view.get_contact_id.return_value = 2

        phonebook.edit_contact()

        self.mock_view.show_message.assert_called_with(any_string_containing(text.contact_found_error))

    def test_delete_contact_successful(self, phonebook):
        phonebook.contacts = [config.test_first_contact]
        self.mock_view.get_contact_id.return_value = 1

        phonebook.delete_contact()

        assert len(phonebook.contacts) == 0
        assert phonebook.modified
        self.mock_view.show_message.assert_called_once()

    def test_delete_contact_not_found(self, phonebook):
        phonebook.contacts = [config.test_first_contact]
        self.mock_view.get_contact_id.return_value = 2

        phonebook.delete_contact()

        assert len(phonebook.contacts) == 1
        self.mock_view.show_message.assert_called_with(any_string_containing(text.contact_found_error))

    def test_run_quit_without_changes(self, phonebook):
        self.mock_view.show_menu.return_value = "7"
        phonebook.modified = False

        phonebook.run()

        self.mock_view.show_menu.assert_called_once()
        self.mock_view.show_message.assert_called_once()

    def test_run_quit_with_changes(self, phonebook):
        self.mock_view.show_menu.return_value = "7"
        self.mock_view.confirm_action.return_value = True
        phonebook.modified = True
        self.mock_file_handler.write_contacts.return_value = True

        phonebook.run()

        self.mock_view.confirm_action.assert_called_once()
        self.mock_file_handler.write_contacts.assert_called_once()


def any_string_containing(substring):
    """Helper function for partial string matching in assert calls"""
    class StringContaining:
        def __eq__(self, other):
            return substring in other
    return StringContaining()
