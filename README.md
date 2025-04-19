# 📃 User Server Project

## 📌 Project Summary

This project is a RESTful web server built with Python and Flask. It manages user data including name, phone number, ID, and address. The server reads from a JSON file at startup and allows access via RESTful API endpoints for retrieving or creating users. It validates Israeli IDs and phone numbers, persists new valid users to the file, and handles bad input or duplicates with clear error messages. A robust test suite built with pytest ensures reliable behavior and edge-case handling. The code is documented, tested, and ready to run on any Linux/macOS/Windows environment.

A simple RESTful server written in Python using Flask. It manages user data (ID, phone number, name, and address), validates the data, stores it in memory, and persists new users to a JSON file.

---

## ✅ Features

- Load user data from a JSON file
- Validate Israeli ID numbers and phone numbers
- REST API with:
  - `GET /users` - List all usernames
  - `GET /users/<name>` - Get full user info (case-insensitive)
  - `POST /users` - Create a new user
- Persist new users to `users.json`
- Extensive input validation
- Full test suite using `pytest`

---

## 🚀 How to Run the Server (Linux)

### Install Dependencies Automatically
After cloning the project and activating the virtual environment, you can install all required packages with:
```bash
pip install -r requirements.txt
```

Alternatively, you can install them manually (see below).

### 1. Clone or Download the Project
```bash
git clone <your-repo-url>
cd user_server_project
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Packages
```bash
pip install Flask pytest
```

### 4. Run the Server
```bash
python server.py
```
Visit: `http://localhost:5000`

### 5. Use curl to Test API
```bash
# Get all users
curl http://localhost:5000/users

# Get user by name
curl http://localhost:5000/users/roei

# Add a new user
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "id": "328957431",
    "name": "RoeiTest",
    "phone": "0531234567",
    "address": "Tel Aviv"
}'
```

---

## 💡 How to Run the Tests
```bash
pytest test_server.py
```

You should see:
```
collected 7 items
test_server.py .......                        [100%]
```

---

## 📁 File Structure
```
user_server_project/
├── server.py          # Main Flask server
├── user.py            # User class
├── validator.py       # ID and phone validation
├── users.json         # Loaded and updated user data
├── test_server.py     # Full pytest suite
├── requirements.txt   # Python dependencies file
├── venv/              # Python virtual environment
```

---

## 🤝 Author
Roei Sharon

---

## ✨ Notes
- All new users are validated and then saved to `users.json`
- If `users.json` is missing, the server starts with an empty map

