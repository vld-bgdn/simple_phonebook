import text_en as text


class View:

    @staticmethod
    def show_message(message: str):
        print(f"\n{message}")

    @staticmethod
    def show_menu():
        for i, row in enumerate(text.main_menu_items):
            print(f'\t{i}. {row}' if i else row)
        return input(text.main_menu_user_choice)

    @staticmethod
    def show_contacts(contacts: dict):
        if not contacts:
            print(text.contact_found_error)
            return

        print(text.contact_main)
        for contact in contacts:
            print(f"{text.contact_id}{contact.id}")
            print(f"{text.contact_name}{contact.name}")
            print(f"{text.contact_phone}{contact.phone}")
            print(f"{text.contact_comment}{contact.comment}")
            print("-" * 30)

    @staticmethod
    def get_contact_input(is_edit=False) -> str:
        if not is_edit:
            print(text.contact_enter_detail)
            name = input(text.contact_name).strip()
            while not name:
                print(text.contact_field_error)
                name = input(text.contact_name).strip()

            phone = input(text.contact_phone).strip()
            while not phone:
                print(text.contact_field_error)
                phone = input(text.contact_phone).strip()

            comment = input(text.contact_comment).strip()
        else:
            print(text.contact_enter_new_details)
            name = input(text.contact_name).strip()
            phone = input(text.contact_phone).strip()
            comment = input(text.contact_comment).strip()
        print(name, phone, comment)
        return name, phone, comment

    @staticmethod
    def get_search_term() -> str:
        return input(text.contact_enter_search).strip()

    @staticmethod
    def get_contact_id() -> int:
        valid_input = False
        cnt_id = None
        while not valid_input:
            try:
                cnt_id = int(input(text.contact_enter_id))
                valid_input = True
            except ValueError:
                print(text.contact_enter_valid_number)
        return cnt_id

    @staticmethod
    def confirm_action() -> bool:
        response = input(text.save_confirm).lower()
        return response == text.save_approve
