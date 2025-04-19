class User:
    """
    Represents a single user in the system.
    Attributes:
        id (str): Israeli ID number of the user 
        name (str): Full name of the user.
        phone (str): Valid Israeli phone number.
        address (str): Contact address.
    """

    def __init__(self, id, name, phone, address):
        """
        Initializes a User instance with the given attributes.
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
                  suitable for JSON or API response.
        """
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "address": self.address
        }
            