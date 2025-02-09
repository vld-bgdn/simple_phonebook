from model import Contact

TEST_FIRST_CONTACT_DATA = {
    "id": 1,
    "name": "Oleg Lutin",
    "phone": "89991112233",
    "comment": "Test comment"
}

TEST_SECOND_CONTACT_DATA = {
    "id": 2,
    "name": "Masha Butova",
    "phone": "899955544"
}

test_first_contact = Contact(
    TEST_FIRST_CONTACT_DATA["id"],
    TEST_FIRST_CONTACT_DATA["name"],
    TEST_FIRST_CONTACT_DATA["phone"],
    TEST_FIRST_CONTACT_DATA["comment"]
)

test_second_contact = Contact(
    TEST_SECOND_CONTACT_DATA["id"],
    TEST_SECOND_CONTACT_DATA["name"],
    TEST_SECOND_CONTACT_DATA["phone"]
)

test_second_updated_contact = Contact(
    TEST_SECOND_CONTACT_DATA["id"],
    TEST_SECOND_CONTACT_DATA["name"],
    TEST_SECOND_CONTACT_DATA["phone"],
    "Updated"
)

test_first_contact_tuple = (TEST_SECOND_CONTACT_DATA["id"],
    TEST_SECOND_CONTACT_DATA["name"],
    TEST_SECOND_CONTACT_DATA["phone"])
