import json
from validator import is_valid_israeli_id, is_valid_phone
from user import User
from flask import Flask, jsonify, request

app = Flask(__name__)
users_map = {}

def load_users_from_file(fileName):
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
    usernames = [user.name for user in users_map.values()]
    return jsonify(usernames),200

@app.route('/users/<name>', methods=['GET'])
def get_user_by_name(name):
    name = name.lower()   #make sure names are matched in a case-insensitive manner
    for user in users_map.values():
        if user.name.lower() == name:
            return jsonify(user.to_dict()), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if data is None:
            raise ValueError("Empty or invalid JSON")
    except Exception:
        return jsonify({"error": "Invalid JSON input"}), 400

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

    user = User(id, name, phone, address)
    users_map[id] = user
    
    save_users_to_file('users.json')
    print(f"User {name} with ID {id} added successfully.")
    
    return jsonify(user.to_dict()), 201

def save_users_to_file(fileName):
    data = [user.to_dict() for user in users_map.values()]
    with open(fileName, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == '__main__':
    users_map = load_users_from_file('users.json')
    app.run(debug=True)

