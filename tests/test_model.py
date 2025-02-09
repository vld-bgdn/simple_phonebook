import pytest
import json
import os

from model import Contact, FileHandler

import tests.test_config as config


@pytest.fixture
def temp_file(tmp_path):
    file_path = tmp_path / "test_contacts.json"
    return str(file_path)


class TestContact:
    def test_contact_init(self):
        contact = config.test_first_contact
        assert contact.id == config.TEST_FIRST_CONTACT_DATA["id"]
        assert contact.name == config.TEST_FIRST_CONTACT_DATA["name"]
        assert contact.phone == config.TEST_FIRST_CONTACT_DATA["phone"]
        assert contact.comment == config.TEST_FIRST_CONTACT_DATA["comment"]

    def test_from_dict(self):
        contact = Contact.from_dict(config.TEST_FIRST_CONTACT_DATA)
        assert contact.id == config.TEST_FIRST_CONTACT_DATA["id"]
        assert contact.name == config.TEST_FIRST_CONTACT_DATA["name"]
        assert contact.phone == config.TEST_FIRST_CONTACT_DATA["phone"]
        assert contact.comment == config.TEST_FIRST_CONTACT_DATA["comment"]

    def test_to_dict(self):
        contact = config.test_first_contact
        contact_dict = contact.to_dict()
        assert contact_dict == config.TEST_FIRST_CONTACT_DATA


class TestFileHandler:
    def test_read_contacts_empty_file(self, temp_file):
        with open(temp_file, 'w') as f:
            json.dump([], f)

        handler = FileHandler(temp_file)
        contacts = handler.read_contacts()
        assert contacts == []

    def test_read_contacts_with_data(self, temp_file):
        test_data = [config.TEST_FIRST_CONTACT_DATA, config.TEST_SECOND_CONTACT_DATA]
        with open(temp_file, 'w') as f:
            json.dump(test_data, f)

        handler = FileHandler(temp_file)
        contacts = handler.read_contacts()

        assert len(contacts) == 2
        assert isinstance(contacts[0], Contact)
        assert contacts[0].name == config.TEST_FIRST_CONTACT_DATA["name"]
        assert contacts[1].name == config.TEST_SECOND_CONTACT_DATA["name"]

    def test_read_contacts_file_not_found(self, temp_file):
        handler = FileHandler(temp_file)
        contacts = handler.read_contacts()
        assert contacts == []

    def test_read_contacts_invalid_json(self, temp_file):
        with open(temp_file, 'w') as f:
            f.write("invalid json data")

        handler = FileHandler(temp_file)
        contacts = handler.read_contacts()
        assert contacts == []

    def test_write_contacts(self, temp_file):
        handler = FileHandler(temp_file)
        contacts = [config.test_first_contact, config.test_second_contact]

        result = handler.write_contacts(contacts)
        assert result is True

        with open(temp_file, 'r') as f:
            data = json.load(f)

        assert len(data) == 2
        assert data[0]["name"] == config.TEST_FIRST_CONTACT_DATA["name"]
        assert data[1]["name"] == config.TEST_SECOND_CONTACT_DATA["name"]

    def test_write_contacts_error(self, temp_file):
        handler = FileHandler(temp_file)

        os.makedirs(temp_file, exist_ok=True)

        contacts = [config.test_first_contact]
        result = handler.write_contacts(contacts)
        assert result is False
