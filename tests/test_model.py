import pytest
import json
import os

from typing import Dict
from model import Contact, FileHandler

"""
Common args for test fuctions:
    test_first_contact: Fixture providing test Contact instance
    test_second_contact: Fixture providing second test Contact instance
    test_contact_data: Fixture providing test contact dictionary data
    test_second_contact_data: Fixture providing second test contact data
    temp_file: Fixture providing temporary file path
"""


@pytest.fixture
def temp_file(tmp_path) -> str:
    """Create a temporary file path for testing.
    Args:
        tmp_path: pytest fixture providing temporary directory
    Returns:
        str: Path to temporary test file
    """
    file_path = tmp_path / "test_contacts.json"
    return str(file_path)


class TestContact:
    def test_contact_init(self, test_first_contact: Contact, test_contact_data: Dict) -> None:
        """Test Contact class initialization."""
        assert test_first_contact.id == test_contact_data["id"]
        assert test_first_contact.name == test_contact_data["name"]
        assert test_first_contact.phone == test_contact_data["phone"]
        assert test_first_contact.comment == test_contact_data["comment"]

    def test_from_dict(self, test_contact_data: Dict) -> None:
        """Test Contact.from_dict static method."""
        contact = Contact.from_dict(test_contact_data)
        assert contact.id == test_contact_data["id"]
        assert contact.name == test_contact_data["name"]
        assert contact.phone == test_contact_data["phone"]
        assert contact.comment == test_contact_data["comment"]

    def test_to_dict(self, test_first_contact: Contact, test_contact_data: Dict) -> None:
        """Test Contact.to_dict method."""
        contact_dict = test_first_contact.to_dict()
        assert contact_dict == test_contact_data


class TestFileHandler:
    def test_read_contacts_empty_file(self, temp_file: str) -> None:
        """Test reading contacts from an empty file."""
        with open(temp_file, 'w') as f:
            json.dump([], f)

        handler = FileHandler(temp_file)
        contacts = handler.read_contacts()
        assert contacts == []

    def test_read_contacts_with_data(self, temp_file: str,
                                     test_contact_data: Dict,
                                     test_second_contact_data: Dict) -> None:
        """Test reading contacts from a file with valid data."""
        test_data = [test_contact_data, test_second_contact_data]
        with open(temp_file, 'w') as f:
            json.dump(test_data, f)

        handler = FileHandler(temp_file)
        contacts = handler.read_contacts()

        assert len(contacts) == 2
        assert isinstance(contacts[0], Contact)
        assert contacts[0].name == test_contact_data["name"]
        assert contacts[1].name == test_second_contact_data["name"]

    def test_read_contacts_file_not_found(self, temp_file: str) -> None:
        """Test reading contacts when file doesn't exist."""
        handler = FileHandler(temp_file)
        contacts = handler.read_contacts()
        assert contacts == []

    def test_read_contacts_invalid_json(self, temp_file: str) -> None:
        """Test reading contacts from file with invalid JSON."""
        with open(temp_file, 'w') as f:
            f.write("invalid json data")

        handler = FileHandler(temp_file)
        contacts = handler.read_contacts()
        assert contacts == []

    def test_write_contacts(self, temp_file: str,
                            test_first_contact: Contact,
                            test_second_contact: Contact,
                            test_contact_data: Dict,
                            test_second_contact_data: Dict) -> None:
        """Test writing contacts to file."""
        handler = FileHandler(temp_file)
        contacts = [test_first_contact, test_second_contact]

        result = handler.write_contacts(contacts)
        assert result is True

        with open(temp_file, 'r') as f:
            data = json.load(f)

        assert len(data) == 2
        assert data[0]["name"] == test_contact_data["name"]
        assert data[1]["name"] == test_second_contact_data["name"]

    def test_write_contacts_error(self, temp_file: str, test_first_contact: Contact) -> None:
        """Test writing contacts when file operation fails."""
        handler = FileHandler(temp_file)

        os.makedirs(temp_file, exist_ok=True)

        contacts = [test_first_contact]
        result = handler.write_contacts(contacts)
        assert result is False
