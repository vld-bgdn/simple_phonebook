import json
from config import PATH
import text_en as text


class Contact:
    def __init__(self, id: int, name: str, phone: str, comment: str = ""):
        self.id = id
        self.name = name
        self.phone = phone
        self.comment = comment

    @classmethod
    def from_dict(cls, data: dict) -> 'Contact':
        return cls(
            id=data["id"],
            name=data["name"],
            phone=data["phone"],
            comment=data.get("comment", "")
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "comment": self.comment
        }


class FileHandler:
    def __init__(self, filename: str = PATH):
        self.filename = filename

    def read_contacts(self) -> list[Contact]:
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                result = []
                for contact in data:
                    cnt_obj = Contact.from_dict(contact)
                    result.append(cnt_obj)
                return result
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def write_contacts(self, contacts) -> bool:
        try:
            with open(self.filename, 'w') as file:
                json_data = [contact.to_dict() for contact in contacts]
                json.dump(json_data, file, indent=2)
            return True
        except Exception as e:
            print(f"{text.save_error}{e}")
            return False
