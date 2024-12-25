import json
import os


def load_phonebook(filename):
    """Load contacts from JSON file"""
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file) or []
        return []
    except Exception as e:
        print(f"Error loading file: {e}")
        return []


def save_phonebook(contacts, filename):
    """Save contacts to JSON file"""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(contacts, file, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False


def generate_id(contacts):
    """Generate new unique ID for contact"""
    if not contacts:
        return 1
    return max(contact["id"] for contact in contacts) + 1


def show_all_contacts(contacts):
    """Display all contacts"""
    if not contacts:
        print("\nNo contacts found.")
        return

    print("\nAll contacts:")
    for contact in contacts:
        print(f"\nID: {contact['id']}")
        print(f"Name: {contact['name']}")
        print(f"Phone: {contact['phone']}")
        print(f"Comment: {contact['comment']}")
        print("-" * 30)


def create_contact(contacts):
    """Create new contact"""
    try:
        print("\nCreating new contact:")
        name = input("Enter name: ").strip()
        while not name:
            print("Name cannot be empty!")
            name = input("Enter name: ").strip()

        phone = input("Enter phone number: ").strip()
        while not phone:
            print("Phone number cannot be empty!")
            phone = input("Enter phone number: ").strip()

        comment = input("Enter comment (optional): ").strip()

        new_contact = {
            "id": generate_id(contacts),
            "name": name,
            "phone": phone,
            "comment": comment,
        }

        contacts.append(new_contact)
        print("\nContact created successfully!")
        return contacts
    except Exception as e:
        print(f"Error creating contact: {e}")
        return contacts


def find_contact(contacts):
    """Find contact by specific field or across all fields"""
    if not contacts:
        print("\nNo contacts to search")
        return

    print("\nSearch options:")
    print("1. Search by name")
    print("2. Search by phone")
    print("3. Search by comment")
    print("4. Search in all fields")

    search_option = input("\nChoose search option (1-4): ").strip()

    if search_option not in ['1', '2', '3', '4']:
        print("Invalid option!")
        return

    search_term = input("\nEnter search term: ").strip().lower()
    found_contacts = []

    for contact in contacts:
        if search_option == '1':  # Search by name
            if search_term in contact["name"].lower():
                found_contacts.append(contact)
        elif search_option == '2':  # Search by phone
            if search_term in contact["phone"].lower():
                found_contacts.append(contact)
        elif search_option == '3':  # Search by comment
            if search_term in contact["comment"].lower():
                found_contacts.append(contact)
        else:  # Search in all fields
            if (search_term in contact["name"].lower() or
                search_term in contact["phone"].lower() or
                search_term in contact["comment"].lower()):
                found_contacts.append(contact)

    if found_contacts:
        print(f"\nFound {len(found_contacts)} contact(s):")
        for contact in found_contacts:
            print(f"\nID: {contact['id']}")
            print(f"Name: {contact['name']}")
            print(f"Phone: {contact['phone']}")
            print(f"Comment: {contact['comment']}")
            print("-" * 30)
    else:
        print("\nNo contacts found")


def edit_contact(contacts):
    """Edit existing contact"""
    if not contacts:
        print("\nNo contacts to edit")
        return contacts

    try:
        contact_id = input("\nEnter contact ID to edit: ").strip()
        if not contact_id.isdigit():
            print("Invalid ID format!")
            return contacts

        contact_id = int(contact_id)
        contact_to_edit = None

        for contact in contacts:
            if contact["id"] == contact_id:
                contact_to_edit = contact
                break

        if not contact_to_edit:
            print(f"Contact with ID {contact_id} not found!")
            return contacts

        print("\nCurrent contact details:")
        print(f"Name: {contact_to_edit['name']}")
        print(f"Phone: {contact_to_edit['phone']}")
        print(f"Comment: {contact_to_edit['comment']}")

        print("\nEnter new details (press Enter to keep current value):")

        name = input("New name: ").strip()
        if name:
            contact_to_edit["name"] = name

        phone = input("New phone: ").strip()
        if phone:
            contact_to_edit["phone"] = phone

        comment = input("New comment: ").strip()
        if comment:
            contact_to_edit["comment"] = comment

        print("\nContact updated successfully!")
        return contacts

    except Exception as e:
        print(f"Error editing contact: {e}")
        return contacts


def delete_contact(contacts):
    """Delete existing contact"""
    if not contacts:
        print("\nNo contacts to delete")
        return contacts

    try:
        contact_id = input("\nEnter contact ID to delete: ").strip()
        if not contact_id.isdigit():
            print("Invalid ID format!")
            return contacts

        contact_id = int(contact_id)
        contact_to_delete = None

        for contact in contacts:
            if contact["id"] == contact_id:
                contact_to_delete = contact
                break

        if not contact_to_delete:
            print(f"Contact with ID {contact_id} not found!")
            return contacts

        print("\nContact to delete:")
        print(f"Name: {contact_to_delete['name']}")
        print(f"Phone: {contact_to_delete['phone']}")
        print(f"Comment: {contact_to_delete['comment']}")

        confirm = (
            input("\nAre you sure you want to delete this contact? (y/n): ")
            .strip()
            .lower()
        )
        if confirm == "y":
            contacts.remove(contact_to_delete)
            print("\nContact deleted successfully!")
        else:
            print("\nDeletion cancelled")

        return contacts

    except Exception as e:
        print(f"Error deleting contact: {e}")
        return contacts


def main():
    filename = "phonebook.json"
    contacts = load_phonebook(filename)

    while True:
        print("\nPhonebook Menu:")
        print("1. Show all contacts")
        print("2. Create new contact")
        print("3. Find contact")
        print("4. Edit contact")
        print("5. Delete contact")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            show_all_contacts(contacts)
        elif choice == "2":
            contacts = create_contact(contacts)
            save_phonebook(contacts, filename)
        elif choice == "3":
            find_contact(contacts)
        elif choice == "4":
            contacts = edit_contact(contacts)
            save_phonebook(contacts, filename)
        elif choice == "5":
            contacts = delete_contact(contacts)
            save_phonebook(contacts, filename)
        elif choice == "6":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice! Please try again")


if __name__ == "__main__":
    main()
