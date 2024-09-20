from test.helpers.utils import (generate_random_pet_data, set_debug_file_name,
                                api_test, clear_log_file, schema_validation,
                                string_gen)
from test.api.basic_requests import post, delete
import json

created_pet_ids = []


def test_setup():
    set_debug_file_name("api_pet")
    clear_log_file("api_pet")


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
    payload = {
        "id": test_data["id"],
        "category": test_data["category"],
        "name": test_data["name"],
        "status": test_data["status"],
        "photoUrls": test_data["photoUrls"],
        "tags": test_data["tags"]
    }
    response = post("/v2/pet", payload, {"content-type": "application/json"})
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
    payload = {
        "id": test_data["id"],
        "category": test_data["category"],
        "name": test_data["name"],
        "status": test_data["status"],
        "photoUrls": test_data["photoUrls"],
        "tags": test_data["tags"]
    }
    response = post("/v2/pet", payload, {"content-type": "application/json"})
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
    payload = {
        "category": test_data["category"],
        "name": test_data["name"],
        "status": test_data["status"],
        "photoUrls": test_data["photoUrls"],
        "tags": test_data["tags"]
    }
    response = post("/v2/pet", payload, {"content-type": "application/json"})
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
    payload = {
        "id": "bad",
        "category": test_data["category"],
        "name": test_data["name"],
        "status": test_data["status"],
        "photoUrls": test_data["photoUrls"],
        "tags": test_data["tags"]
    }
    response = post("/v2/pet", payload, {"content-type": "application/json"})

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
    payload = {
        "id": -1,
        "category": test_data["category"],
        "name": test_data["name"],
        "status": test_data["status"],
        "photoUrls": test_data["photoUrls"],
        "tags": test_data["tags"]
    }
    response = post("/v2/pet", payload, {"content-type": "application/json"})
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


def test_add_pet_with_id_null():
    """
        Test the functionality of adding a new pet to the Pet Store with ID null.

        Actions:
        - Generate random pet data.
        - Perform a POST request to add a new pet with the generated data (but ID null).
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
    payload = {
        "id": None,
        "category": test_data["category"],
        "name": test_data["name"],
        "status": test_data["status"],
        "photoUrls": test_data["photoUrls"],
        "tags": test_data["tags"]
    }
    response = post("/v2/pet", payload, {"content-type": "application/json"})
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


def test_add_pet_with_name_with_spaces():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["name"] += " with spaces"

    # Perform a POST request to add a new pet
    payload = {
        "id": test_data["id"],
        "category": test_data["category"],
        "name": test_data["name"],
        "status": test_data["status"],
        "photoUrls": test_data["photoUrls"],
        "tags": test_data["tags"]
    }
    response = post("/v2/pet", payload, {"content-type": "application/json"})
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


def test_add_pet_with_name_empty_string():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["name"] = ""

    # Perform a POST request to add a new pet
    payload = {
        "id": test_data["id"],
        "category": test_data["category"],
        "name": test_data["name"],
        "status": test_data["status"],
        "photoUrls": test_data["photoUrls"],
        "tags": test_data["tags"]
    }
    response = post("/v2/pet", payload, {"content-type": "application/json"})
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


def test_add_pet_with_name_missing():
    # Generate random pet data
    test_data = generate_random_pet_data()

    # Perform a POST request to add a new pet
    payload = {
        "id": test_data["id"],
        "category": test_data["category"],
        "status": test_data["status"],
        "photoUrls": test_data["photoUrls"],
        "tags": test_data["tags"]
    }
    response = post("/v2/pet", payload, {"content-type": "application/json"})
    pet = json.loads(response.text)

    # Store the created pet ID for cleanup
    created_pet_ids.append(pet['id'])

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{test_data["id"]}',
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


def test_add_pet_with_name_invalid_data_type():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["name"] = 123

    # Perform a POST request to add a new pet
    payload = {
        "id": test_data["id"],
        "category": test_data["category"],
        "name": test_data["name"],
        "status": test_data["status"],
        "photoUrls": test_data["photoUrls"],
        "tags": test_data["tags"]
    }
    response = post("/v2/pet", payload, {"content-type": "application/json"})
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


def test_add_pet_with_name_invalid_too_long():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["name"] = string_gen(1025)

    # Perform a POST request to add a new pet
    payload = {
        "id": test_data["id"],
        "category": test_data["category"],
        "name": test_data["name"],
        "status": test_data["status"],
        "photoUrls": test_data["photoUrls"],
        "tags": test_data["tags"]
    }
    response = post("/v2/pet", payload, {"content-type": "application/json"})
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


def test_add_pet_with_name_null():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["name"] = None

    # Perform a POST request to add a new pet
    payload = {
        "id": test_data["id"],
        "category": test_data["category"],
        "name": test_data["name"],
        "status": test_data["status"],
        "photoUrls": test_data["photoUrls"],
        "tags": test_data["tags"]
    }
    response = post("/v2/pet", payload, {"content-type": "application/json"})
    pet = json.loads(response.text)

    # Store the created pet ID for cleanup
    created_pet_ids.append(pet['id'])

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{test_data["id"]}',
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
        response = delete(f"/v2/pet/{pet_id}")
        if response.status_code == 200:
            print(f"Deleted pet with ID {pet_id}")
        else:
            print(f"Failed to delete pet with ID {pet_id}, status code: {response.status_code}")
