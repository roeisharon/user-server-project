import json
from validator import is_valid_israeli_id, is_valid_phone
from user import User
from flask import Flask, jsonify, request

#Initializing Flask app
app = Flask(__name__)
# In-memory storage for users (id: User)
users_map = {}

def load_users_from_file(fileName):
    """
    Loads users from a JSON file into the users_map dictionary.
    Invalid users (bad ID or phone) are skipped.

    Args:
        fileName (str): The name of the JSON file to read from.

    Returns:
        dict: A dictionary mapping user IDs to User objects.
    """
    try:
        with open(fileName, 'r') as file:
            data = json.load(file)
            for user in data:
                id = str(user['id'])
                name = user['name']
                phone = user['phone']
                address = user['address']
                if not is_valid_israeli_id(id):
                    print(f"Invalid ID {id} for user {name}. Skipping.")
                    continue
                if not is_valid_phone(phone):
                    print(f"Invalid phone {phone} for user {name}. Skipping.")
                    continue
                users_map[id] = User(id, name, phone, address)
        print(f"Loaded {len(users_map)} users from {fileName}.")

    except FileNotFoundError:
        print(f"File {fileName} not found. Starting with an empty user map.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {fileName}. Starting with an empty user map.")
    
    return users_map

@app.route('/users', methods=['GET'])
def get_users():
    """
    Returns a list of all user names in the system.

    Returns:
        Response: JSON list of names with HTTP 200.
    """
    usernames = [user.name for user in users_map.values()]
    return jsonify(usernames),200

@app.route('/users/<name>', methods=['GET'])
def get_user_by_name(name):
    """
    Retrieves a user's full information by name (case-insensitive).

    Args:
        name (str): The name to search for in the users_map.

    Returns:
        Response: JSON user data with HTTP 200 if found,
                  or error message with HTTP 404.
    """
    name = name.lower()   #make sure names are matched in a case-insensitive manner
    for user in users_map.values():
        if user.name.lower() == name:
            return jsonify(user.to_dict()), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    """
    Creates a new user from a POST request.
    Performs validation and prevents duplicates.

    Request JSON must contain:
    - id, name, phone, address

    Returns:
        Response: JSON representation of the created user with HTTP 201,
                  or error message with HTTP 400.
    """
    try:
        data = request.get_json()
        if data is None:
            raise ValueError("Empty or invalid JSON")
    except Exception:
        return jsonify({"error": "Invalid JSON input"}), 400
    
    # Check for required fields existence
    required_fields = ['id', 'name', 'phone', 'address']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing field: {field}"}), 400

    id = str(data.get('id'))
    name = data.get('name')
    phone = data.get('phone')
    address = data.get('address')

    if not is_valid_israeli_id(id):
        return jsonify({"error": "Invalid ID"}), 400
    if not is_valid_phone(phone):
        return jsonify({"error": "Invalid phone number"}), 400
    
    if id in users_map:
        return jsonify({"error": "User already exists"}), 400

    # Create a new user and add to the map
    user = User(id, name, phone, address)
    users_map[id] = user
    
    save_users_to_file('users.json')
    print(f"User {name} with ID {id} added successfully.")
    
    return jsonify(user.to_dict()), 201

def save_users_to_file(fileName):
    """
    Writes the current users_map into a JSON file.

    This serves as a lightweight alternative to a database.
    It allows the application to handle data across sessions
    without requiring an external DB system.

    Args:
        fileName (str): The filename to write to.
    """
    data = [user.to_dict() for user in users_map.values()]
    with open(fileName, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == '__main__':
    users_map = load_users_from_file('users.json')
    app.run(debug=True)

