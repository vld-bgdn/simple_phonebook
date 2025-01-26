from model import Contact, FileHandler
from view import View
import text_en as text


class Phonebook:
    def __init__(self):
        self.file_handler = FileHandler()
        self.view = View()
        self.contacts = []
        self.modified = False
        self.load_contacts()

    def load_contacts(self):
        self.contacts = self.file_handler.read_contacts()

    def save_contacts(self):
        if self.file_handler.write_contacts(self.contacts):
            self.modified = False
            self.view.show_message(text.contact_save_successful)
        else:
            self.view.show_message(text.save_error)

    def get_next_id(self) -> int:
        return max([contact.id for contact in self.contacts], default=0) + 1

    def create_contact(self):
        name, phone, comment = self.view.get_contact_input()
        contact = Contact(self.get_next_id(), name, phone, comment)
        self.contacts.append(contact)
        self.modified = True
        self.view.show_message(text.contact_create_successful)

    def find_contacts(self):
        search_term = self.view.get_search_term().lower()
        found_contacts = [
            contact for contact in self.contacts
            if (search_term in contact.name.lower() or
                search_term in contact.phone.lower() or
                search_term in contact.comment.lower())
        ]
        self.view.show_contacts(found_contacts)

    def edit_contact(self):
        self.view.show_contacts(self.contacts)
        if not self.contacts:
            return

        contact_id = self.view.get_contact_id()
        contact = None

        for c in self.contacts:
            if c.id == contact_id:
                contact = c
                break

        if contact is None:
            self.view.show_message(text.contact_found_error)
            return

        self.view.show_message(text.contact_details)
        self.view.show_contacts([contact])

        name, phone, comment = self.view.get_contact_input(is_edit=True)

        if name:
            contact.name = name
        if phone:
            contact.phone = phone
        if comment:
            contact.comment = comment
        self.view.show_message(text.contact_update_successful)
        self.modified = True

    def delete_contact(self):
        self.view.show_contacts(self.contacts)
        if not self.contacts:
            return

        contact_id = self.view.get_contact_id()
        contact = next((c for c in self.contacts if c.id == contact_id), None)

        if contact:
            self.contacts.remove(contact)
            self.modified = True
            self.view.show_message(text.contact_delete_successful)
        else:
            self.view.show_message(text.contact_found_error)

    def run(self):
        while True:
            choice = self.view.show_menu()

            if choice == "1":
                self.view.show_contacts(self.contacts)
            elif choice == "2":
                self.create_contact()
            elif choice == "3":
                self.find_contacts()
            elif choice == "4":
                self.edit_contact()
            elif choice == "5":
                self.delete_contact()
            elif choice == "6":
                self.save_contacts()
            elif choice == '7':
                if self.modified:
                    if self.view.confirm_action():
                        self.save_contacts()
                self.view.show_message(text.phonebook_closing)
                break
            else:
                self.view.show_message(text.main_menu_user_choice_error)
