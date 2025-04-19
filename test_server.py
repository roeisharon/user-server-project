import pytest
import json
from server import app, users_map
from user import User

# ───────────────────────────── Fixtures ───────────────────────────── #

@pytest.fixture(autouse=True)
def clear_users_map():
    """
    Automatically clears the in-memory users_map before every test.
    Ensures each test runs in isolation with a clean state.
    """
    users_map.clear()

@pytest.fixture
def client():
    """
    Creates and provides a Flask test client for simulating HTTP requests.
    Runs Flask in testing mode (does not start real server).
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# ───────────────────────────── Tests ───────────────────────────── #

#Test 1: GET /users/<name> - case insensitive 
def test_get_user_by_name_case_insensitive(client):
    """
    Verifies that user lookup is case-insensitive.
    """
    users_map['123456782'] = User("123456782", "Roei", "0501234567", "Tel Aviv") #manually inject a user 
    response = client.get('/users/ROEI')  # intentionally uppercase
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == "Roei"
    assert data['phone'] == "0501234567"

#Test 2: GET /users - base route
def test_get_users(client):
    """
    Verifies that GET /users returns a list of usernames.
    """
    users_map['123456782'] = User("123456782", "Roei", "0501234567", "Tel Aviv") #manually inject a user
    response = client.get('/users')
    assert response.status_code == 200
    assert "Roei" in response.get_json()

# Test 3: POST /users - covers edge cases
# Parametrize the test with different payloads each time
@pytest.mark.parametrize("payload, expected_status, expected_error", [
    # Missing field
    ({"id": "123456782", "name": "NoPhone", "address": "MissingPhone"}, 400, "Missing field: phone"),
    #Invalid ID
    ({"id": "12345", "name": "BadID", "phone": "0501234567", "address": "ShortTown"}, 400, "Invalid ID"),
    # Invalid phone
    ({"id": "123456782", "name": "BadPhone", "phone": "0591234567", "address": "NoReception"}, 400, "Invalid phone number"),
    #Valid user
    ({"id": "123456782", "name": "Tester123", "phone": "0531234567", "address": "TestCity"}, 201, None),
])
def test_post_user_variants(client, payload, expected_status, expected_error):
    """
    Tests multiple variants of user creation via POST /users.
    Covers:
    - Missing fields
    - Invalid ID
    - Invalid phone
    - Valid user with data written to file
    """
    response = client.post('/users', json=payload)
    assert response.status_code == expected_status
    data = response.get_json()

    if expected_error:
        assert expected_error in data['error']
    elif expected_status == 201:
        assert 'name' in data and 'phone' in data
        
        #check that user is saved to users.json (DB alternative)
        with open('users.json', 'r') as file:
            saved_data = json.load(file)
            assert any(user['id'] == payload['id'] for user in saved_data)
    
# Test 4: POST /users - duplicate ID
def test_post_user_duplicate_id(client):
    """
    Ensures that creating a user with an existing ID is rejected.
    """
    users_map['123456782'] = User("123456782", "Original", "0501234567", "Tel Aviv") #manually inject a user
    response = client.post('/users', json={
        "id": "123456782",
        "name": "Duplicate",
        "phone": "0539876543",
        "address": "ClashCity"
    })
    assert response.status_code == 400
    assert "already exists" in response.get_json()['error']

