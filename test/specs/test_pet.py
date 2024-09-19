from test.api.api_pet import add_pet, delete_pet
from test.helpers.utils import (generate_random_pet_data, set_debug_file_name,
                                api_test, clear_log_files, schema_validation)
import json

created_pet_ids = []


def test_setup():
    set_debug_file_name("api_pet")
    clear_log_files()


#
# POST /pet tests
#
def test_add_pet():
    """
        Test the functionality of adding a new pet to the Pet Store.

        Actions:
        - Generate random pet data.
        - Perform a POST request to add a new pet with the generated data.
        - Retrieve the JSON response and HTTP status code.

        Expected Outcome:
        - The status code should be 201, indicating a successful addition.
        - The response JSON should contain the added pet's information.
        - The added pet's name, category, and status should match the generated data.
        - Cleanup: The added pet ID is stored for later removal.
        """
    # Generate random pet data
    test_data = generate_random_pet_data()

    # Perform a POST request to add a new pet
    response = add_pet(test_data["id"], test_data["category"], test_data["name"], test_data["status"],
                       test_data["photoUrls"], test_data["tags"])
    pet = json.loads(response.text)

    # Store the created pet ID for cleanup
    created_pet_ids.append(pet['id'])

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{test_data["id"]}',
                                f'"name":"{test_data["name"]}"',
                                f'"category":{{"id":{test_data["category"]["id"]},'
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"',
                                '"tags"',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_schema():
    """
        Test the schema of adding a new pet to the Pet Store.

        Actions:
        - Generate random pet data.
        - Perform a POST request to add a new pet with the generated data.
        - Retrieve the JSON response and HTTP status code.

        Expected Outcome:
        - The response body and headers should match the known good schema.
        - Cleanup: The added pet ID is stored for later removal.
        """
    # Generate random pet data
    test_data = generate_random_pet_data()

    # Perform a POST request to add a new pet
    response = add_pet(test_data["id"], test_data["category"], test_data["name"], test_data["status"],
                       test_data["photoUrls"], test_data["tags"])
    pet = json.loads(response.text)

    # Store the created pet ID for cleanup
    created_pet_ids.append(pet['id'])

    # Validate the outcome of the test with a single assert statement
    test_results = schema_validation("pet", "/v2/pet", "POST",
                                     response, False, True)
    assert test_results == "No mismatch values"


def test_add_pet_with_id_missing():
    """
        Test the functionality of adding a new pet to the Pet Store with ID missing.

        Actions:
        - Generate random pet data.
        - Perform a POST request to add a new pet with the generated data (but ID missing).
        - Retrieve the JSON response and HTTP status code.

        Expected Outcome:
        - The status code should be 201, indicating a successful addition.
        - The response JSON should contain the added pet's information.
        - The added pet's name, category, and status should match the generated data.
        - Cleanup: The added pet ID is stored for later removal.
        """
    # Generate random pet data
    test_data = generate_random_pet_data()

    # Perform a POST request to add a new pet
    response = add_pet(None, test_data["category"], test_data["name"], test_data["status"],
                       test_data["photoUrls"], test_data["tags"])
    pet = json.loads(response.text)

    # Store the created pet ID for cleanup
    created_pet_ids.append(pet['id'])

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"name":"{test_data["name"]}"',
                                f'"category":{{"id":{test_data["category"]["id"]},'
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"',
                                '"tags"',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_id_invalid_data_type():
    """
        Test the functionality of adding a new pet to the Pet Store with ID invalid (data type).

        Actions:
        - Generate random pet data.
        - Perform a POST request to add a new pet with the generated data (but ID invalid, data type).
        - Retrieve the JSON response and HTTP status code.

        Expected Outcome:
        - The status code should be 201, indicating a successful addition.
        - The response JSON should contain the added pet's information.
        - The added pet's name, category, and status should match the generated data.
        - Cleanup: The added pet ID is stored for later removal.
        """
    # Generate random pet data
    test_data = generate_random_pet_data()

    # Perform a POST request to add a new pet
    response = add_pet("abc", test_data["category"], test_data["name"], test_data["status"],
                       test_data["photoUrls"], test_data["tags"])
    pet = json.loads(response.text)

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            500,
                            [
                                '"code":500', '"type":"unknown"',
                                '"message":"something bad happened"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_id_invalid_negative_one():
    """
        Test the functionality of adding a new pet to the Pet Store with ID invalid (-1).

        Actions:
        - Generate random pet data.
        - Perform a POST request to add a new pet with the generated data (but ID invalid, -1).
        - Retrieve the JSON response and HTTP status code.

        Expected Outcome:
        - The status code should be 201, indicating a successful addition.
        - The response JSON should contain the added pet's information.
        - The added pet's name, category, and status should match the generated data.
        - Cleanup: The added pet ID is stored for later removal.
        """
    # Generate random pet data
    test_data = generate_random_pet_data()

    # Perform a POST request to add a new pet
    response = add_pet(-1, test_data["category"], test_data["name"], test_data["status"],
                       test_data["photoUrls"], test_data["tags"])
    pet = json.loads(response.text)

    # Store the created pet ID for cleanup
    created_pet_ids.append(pet['id'])

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"name":"{test_data["name"]}"',
                                f'"category":{{"id":{test_data["category"]["id"]},'
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"',
                                '"tags"',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_cleanup_created_pets():
    print(f"\n\nPost suite pet cleanup...")
    for pet_id in created_pet_ids:
        response = delete_pet(pet_id)
        if response.status_code == 200:
            print(f"Deleted pet with ID {pet_id}")
        else:
            print(f"Failed to delete pet with ID {pet_id}, status code: {response.status_code}")
