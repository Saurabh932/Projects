class Contactbook:
    def __init__(self):
        self.contact_data = []

    def create_contact(self, name, phone_number, email, address):
        for contact in self.contact_data:
            if contact["name"].lower() == name.lower():
                return "Contact already exists."

        data = {
            "name": name,
            "phone_number": phone_number,
            "email": email,
            "address": address
        }

        self.contact_data.append(data)
        return data

    def update_contact(self, name, phone_number, email, address):
        for contact in self.contact_data:
            if contact["name"].lower() == name.lower():
                contact["phone_number"] = phone_number
                contact["email"] = email
                contact["address"] = address
                return contact
        return "Contact not found."

    def delete_contact(self, name):
        for contact in self.contact_data:
            if contact["name"].lower() == name.lower():
                self.contact_data.remove(contact)
                return "Deleted successfully"
        return "Contact not found."

    def search_contact(self, name):
        for contact in self.contact_data:
            if contact["name"].lower() == name.lower():
                return contact
        return "Contact not found."

    def view_contact(self):
        return self.contact_data
