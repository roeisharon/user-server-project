class User:
    """
    Represents a single user in the system.
    Attributes:
        id (str): Israeli ID number of the user (validated externally).
        name (str): Full name of the user.
        phone (str): Phone number in Israeli format.
        address (str): Residential or contact address.
    """

    def __init__(self, id, name, phone, address):
        """
        Initializes a User instance with the given attributes.

        Args:
            id (str): Israeli ID number.
            name (str): User's name.
            phone (str): User's phone number.
            address (str): User's address.
        """
        self.id = id
        self.name = name
        self.phone = phone
        self.address = address

    def to_dict(self):
        """
        Converts the User object to a dictionary.

        Returns:
            dict: A dictionary representation of the user,
                  suitable for JSON serialization or API response.
        """
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "address": self.address
        }
            