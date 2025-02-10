import pytest
from model import Contact

@pytest.fixture
def test_contact_data():
    return {
        "id": 1,
        "name": "Oleg Lutin",
        "phone": "89991112233",
        "comment": "Test comment"
    }

@pytest.fixture
def test_second_contact_data():
    return {
        "id": 2,
        "name": "Masha Butova",
        "phone": "899955544"
    }

@pytest.fixture
def test_first_contact(test_contact_data):
    return Contact(
        test_contact_data["id"],
        test_contact_data["name"],
        test_contact_data["phone"],
        test_contact_data["comment"]
    )

@pytest.fixture
def test_second_contact(test_second_contact_data):
    return Contact(
        test_second_contact_data["id"],
        test_second_contact_data["name"],
        test_second_contact_data["phone"]
    )

@pytest.fixture
def test_second_updated_contact(test_second_contact_data):
    return Contact(
        test_second_contact_data["id"],
        test_second_contact_data["name"],
        test_second_contact_data["phone"],
        "Updated"
    )

@pytest.fixture
def test_first_contact_tuple(test_contact_data):
    return (
        test_contact_data["name"],
        test_contact_data["phone"],
        test_contact_data["comment"]
    )
