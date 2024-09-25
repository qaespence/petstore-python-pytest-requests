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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_name_over_1024_chars():
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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_category_id_missing():
    # Generate random pet data
    test_data = generate_random_pet_data()
    del test_data["category"]["id"]

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
                                f'"category":{{"id":0',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_category_id_invalid_data_type():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["category"]["id"] = "bad"

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


def test_add_pet_with_category_id_invalid_negative_one():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["category"]["id"] = -1

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_category_id_null():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["category"]["id"] = None

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
                                f'"category":{{"id":0',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_category_name_with_spaces():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["category"]["name"] += " with spaces"

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_category_name_empty_string():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["category"]["name"] = ""

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_category_name_missing():
    # Generate random pet data
    test_data = generate_random_pet_data()
    del test_data["category"]["name"]

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_category_name_invalid_data_type():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["category"]["name"] = 123

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_category_name_over_1024_chars():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["category"]["name"] = string_gen(1025)

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_category_name_null():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["category"]["name"] = None

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_photo_urls_1_valid():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["photoUrls"] = ["http://test.com/photo1.jpg"]

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_photo_urls_2_valid():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["photoUrls"] = ["http://test.com/photo1.jpg", "http://test.com/photo2.jpg"]

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                f'{test_data["photoUrls"][1]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_photo_urls_same_twice():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["photoUrls"] = ["http://test.com/photo1.jpg", "http://test.com/photo1.jpg"]

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"
    

def test_add_pet_with_photo_urls_1_invalid():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["photoUrls"] = ["not-a-url"]

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_photo_urls_a_mix_of_valid_and_invalid():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["photoUrls"] = ["http://test.com/photo1.jpg", "not-a-url"]

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_photo_urls_missing():
    # Generate random pet data
    test_data = generate_random_pet_data()
    del test_data["photoUrls"]

    # Perform a POST request to add a new pet
    payload = {
        "id": test_data["id"],
        "category": test_data["category"],
        "name": test_data["name"],
        "status": test_data["status"],
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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_photo_urls_invalid_data_type():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["photoUrls"] = 123

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


def test_add_pet_with_photo_urls_empty_list():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["photoUrls"] = []

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_photo_urls_null():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["photoUrls"] = None

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_tags_id_missing():
    # Generate random pet data
    test_data = generate_random_pet_data()
    del test_data["tags"][0]["id"]

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_tags_id_invalid_data_type():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["tags"][0]["id"] = "bad"

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


def test_add_pet_with_tags_id_invalid_negative_one():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["tags"][0]["id"] = -1

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_tags_id_null():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["tags"][0]["id"] = None

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_tags_name_with_spaces():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["tags"][0]["name"] += " with spaces"

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_tags_name_empty_string():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["tags"][0]["name"] = ""

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_tags_name_missing():
    # Generate random pet data
    test_data = generate_random_pet_data()
    del test_data["tags"][0]["name"]

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_tags_name_invalid_data_type():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["tags"][0]["name"] = 123

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_tags_name_over_1024_chars():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["tags"][0]["name"] = string_gen(1025)

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_tags_name_null():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["tags"][0]["name"] = None

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_status_available():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["status"] = "available"

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_status_pending():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["status"] = "pending"

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_status_sold():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["status"] = "sold"

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_status_unsupported():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["status"] = "unsupported"

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_status_missing():
    # Generate random pet data
    test_data = generate_random_pet_data()
    del test_data["status"]

    # Perform a POST request to add a new pet
    payload = {
        "id": test_data["id"],
        "category": test_data["category"],
        "name": test_data["name"],
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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_status_invalid_data_type():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["status"] = 123

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_pet_with_status_null():
    # Generate random pet data
    test_data = generate_random_pet_data()
    test_data["status"] = None

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
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}', f'{test_data["tags"][0]["name"]}'
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
