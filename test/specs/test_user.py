from test.helpers.utils import (generate_random_user_data, set_debug_file_name,
                                api_test, clear_log_file, schema_validation)
from test.api.basic_requests import post, delete
import json

created_user_names = []


def test_setup():
    set_debug_file_name("api_user")
    clear_log_file("api_user")


#
# POST /user tests
#
def test_add_user():
    """
        Test the functionality of adding a new user to the Pet Store.

        Actions:
        - Generate random user data.
        - Perform a POST request to add a new user with the generated data.
        - Retrieve the JSON response and HTTP status code.

        Expected Outcome:
        - The status code should be 200, indicating a successful addition.
        - The response JSON should contain the added user's information.
        - The added user data should match the generated data.
        - Cleanup: The added user ID is stored for later removal.
        """
    # Generate random order data
    test_data = generate_random_user_data()

    # Perform a POST request to add a new order
    payload = {
        "id": test_data["id"],
        "username": test_data["username"],
        "firstName": test_data["first_name"],
        "lastName": test_data["last_name"],
        "email": test_data["email"],
        "password": test_data["password"],
        "phone": test_data["phone"],
        "userStatus": test_data["user_status"]
    }
    response = post("/v2/user", payload, {"content-type": "application/json"})

    # Store the created pet ID for cleanup
    created_user_names.append(test_data['username'])

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                '"code":200',
                                '"type":"unknown"',
                                f'"message":"{test_data["id"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_user_schema():
    """
        Test the schema of adding a new user to the Pet Store.

        Actions:
        - Generate random user data.
        - Perform a POST request to add a new user with the generated data.
        - Retrieve the JSON response and HTTP status code.

        Expected Outcome:
        - The response body and headers should match the known good schema.
        - Cleanup: The added order ID is stored for later removal.
        """
    # Generate random order data
    test_data = generate_random_user_data()

    # Perform a POST request to add a new order
    payload = {
        "id": test_data["id"],
        "username": test_data["username"],
        "firstName": test_data["first_name"],
        "lastName": test_data["last_name"],
        "email": test_data["email"],
        "password": test_data["password"],
        "phone": test_data["phone"],
        "userStatus": test_data["user_status"]
    }
    response = post("/v2/user", payload, {"content-type": "application/json"})

    # Store the created pet ID for cleanup
    created_user_names.append(test_data['username'])

    # Validate the outcome of the test with a single assert statement
    test_results = schema_validation("user", "/v2/user", "POST",
                                     response, True, True)
    assert test_results == "No mismatch values"


#
# User Clean-up
#
def test_cleanup_created_order():
    print(f"\n\nPost suite order cleanup...")
    for user_name in created_user_names:
        response = delete(f"/v2/user/{user_name}")
        if response.status_code == 200:
            print(f"Deleted user with username {user_name}")
        else:
            print(f"Failed to delete user with username {user_name}, status code: {response.status_code}")