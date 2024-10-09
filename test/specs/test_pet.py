from test.helpers.utils import (generate_random_pet_data, set_debug_file_name,
                                api_test, clear_log_file, schema_validation,
                                string_gen)
from test.api.basic_requests import post, delete, get, put
import json
import random
import pytest

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


#
# GET /pet/:pet_id tests
#
def create_test_pet():
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
    test_data["token"] = pet['id']

    return test_data


def test_fetch_pet():
    # Generate random pet
    test_data = create_test_pet()

    # Fetch pet
    response = get(f'/v2/pet/{test_data["token"]}')

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


def test_fetch_pet_schema():
    # Generate random pet
    test_data = create_test_pet()

    # Fetch pet
    response = get(f'/v2/pet/{test_data["token"]}')

    # Validate the outcome of the test with a single assert statement
    test_results = schema_validation("pet", "/v2/pet/:pet_id", "GET",
                                     response, False, True)
    assert test_results == "No mismatch values"


def test_fetch_pet_with_bad_token():
    # Fetch pet
    response = get('/v2/pet/bad')

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            404,
                            [
                                '"type":"unknown"',
                                '"message":"java.lang.NumberFormatException: For input string',
                                'bad'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


#
# PUT /pet tests
#
def test_update_pet_put_json_all_fields_valid():
    # Generate random pet
    old_test_data = create_test_pet()

    # Generate updated random pet data
    test_data = generate_random_pet_data()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": test_data["category"],
        "name": test_data["name"],
        "status": test_data["status"],
        "photoUrls": test_data["photoUrls"],
        "tags": test_data["tags"]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{test_data["name"]}"',
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}',
                                f'{test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_schema():
    # Generate random pet
    old_test_data = create_test_pet()

    # Generate updated random pet data
    test_data = generate_random_pet_data()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": test_data["category"],
        "name": test_data["name"],
        "status": test_data["status"],
        "photoUrls": test_data["photoUrls"],
        "tags": test_data["tags"]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = schema_validation("pet", "/v2/pet", "PUT",
                                     response, False, True)
    assert test_results == "No mismatch values"


def test_update_pet_put_json_category_id_valid():
    # Generate random pet
    old_test_data = create_test_pet()

    # Generate updated random pet data
    test_data = generate_random_pet_data()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": {"id": test_data["category"]["id"], "name": old_test_data["category"]["name"]},
        "name": old_test_data["name"],
        "status": old_test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": old_test_data["tags"]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{old_test_data["name"]}"',
                                f'"category":{{"id":{test_data["category"]["id"]}',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{old_test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_category_id_missing():
    # Generate random pet
    old_test_data = create_test_pet()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": {"name": old_test_data["category"]["name"]},
        "name": old_test_data["name"],
        "status": old_test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": old_test_data["tags"]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{old_test_data["name"]}"',
                                f'"category"',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{old_test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_category_id_invalid_data_type():
    # Generate random pet
    old_test_data = create_test_pet()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": {"id": "bad", "name": old_test_data["category"]["name"]},
        "name": old_test_data["name"],
        "status": old_test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": old_test_data["tags"]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

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


def test_update_pet_put_json_category_id_null():
    # Generate random pet
    old_test_data = create_test_pet()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": {"id": None, "name": old_test_data["category"]["name"]},
        "name": old_test_data["name"],
        "status": old_test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": old_test_data["tags"]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{old_test_data["name"]}"',
                                f'"category"',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{old_test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_category_name_valid():
    # Generate random pet
    old_test_data = create_test_pet()

    # Generate updated random pet data
    test_data = generate_random_pet_data()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": {"id": old_test_data["category"]["id"], "name": test_data["category"]["name"]},
        "name": old_test_data["name"],
        "status": old_test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": old_test_data["tags"]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{old_test_data["name"]}"',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                f'"name":"{test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{old_test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_category_name_missing():
    # Generate random pet
    old_test_data = create_test_pet()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": {"id": old_test_data["category"]["id"]},
        "name": old_test_data["name"],
        "status": old_test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": old_test_data["tags"]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{old_test_data["name"]}"',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{old_test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_category_name_invalid_data_type():
    # Generate random pet
    old_test_data = create_test_pet()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": {"id": old_test_data["category"]["id"], "name": 123},
        "name": old_test_data["name"],
        "status": old_test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": old_test_data["tags"]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{old_test_data["name"]}"',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                f'"name":"123"}}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{old_test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_category_name_null():
    # Generate random pet
    old_test_data = create_test_pet()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": {"id": old_test_data["category"]["id"], "name": None},
        "name": old_test_data["name"],
        "status": old_test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": old_test_data["tags"]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{old_test_data["name"]}"',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{old_test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_tags_id_valid():
    # Generate random pet
    old_test_data = create_test_pet()

    # Generate updated random pet data
    test_data = generate_random_pet_data()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": old_test_data["category"],
        "name": old_test_data["name"],
        "status": old_test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": [{"id": test_data["tags"][0]["id"], "name": old_test_data["tags"][0]["name"]}]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{old_test_data["name"]}"',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"', f'{test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{old_test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_tags_id_missing():
    # Generate random pet
    old_test_data = create_test_pet()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": old_test_data["category"],
        "name": old_test_data["name"],
        "status": old_test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": [{"name": old_test_data["tags"][0]["name"]}]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{old_test_data["name"]}"',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{old_test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_tags_id_invalid_data_type():
    # Generate random pet
    old_test_data = create_test_pet()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": old_test_data["category"],
        "name": old_test_data["name"],
        "status": old_test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": [{"id": "bad", "name": old_test_data["tags"][0]["name"]}]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

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


def test_update_pet_put_json_tags_id_null():
    # Generate random pet
    old_test_data = create_test_pet()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": old_test_data["category"],
        "name": old_test_data["name"],
        "status": old_test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": [{"id": None, "name": old_test_data["tags"][0]["name"]}]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{old_test_data["name"]}"',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{old_test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_tags_name_valid():
    # Generate random pet
    old_test_data = create_test_pet()

    # Generate updated random pet data
    test_data = generate_random_pet_data()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": old_test_data["category"],
        "name": old_test_data["name"],
        "status": old_test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": [{"id": old_test_data["tags"][0]["id"], "name": test_data["tags"][0]["name"]}]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{old_test_data["name"]}"',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{test_data["tags"][0]["name"]}',
                                f'"status":"{old_test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_name_valid():
    # Generate random pet
    old_test_data = create_test_pet()

    # Generate updated random pet data
    test_data = generate_random_pet_data()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": old_test_data["category"],
        "name": test_data["name"],
        "status": old_test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": old_test_data["tags"]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{test_data["name"]}"',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{old_test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_name_missing():
    # Generate random pet
    old_test_data = create_test_pet()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": old_test_data["category"],
        "status": old_test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": old_test_data["tags"]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{old_test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_name_invalid_data_type():
    # Generate random pet
    old_test_data = create_test_pet()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": old_test_data["category"],
        "name": 123,
        "status": old_test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": old_test_data["tags"]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"123"',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{old_test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_name_over_1024_chars():
    # Generate random pet
    old_test_data = create_test_pet()

    # Generate long name
    new_name = string_gen(1025)

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": old_test_data["category"],
        "name": new_name,
        "status": old_test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": old_test_data["tags"]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{new_name}"',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{old_test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_name_null():
    # Generate random pet
    old_test_data = create_test_pet()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": old_test_data["category"],
        "name": None,
        "status": old_test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": old_test_data["tags"]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{old_test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_photo_urls_valid():
    # Generate random pet
    old_test_data = create_test_pet()

    # Generate updated random pet data
    test_data = generate_random_pet_data()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": old_test_data["category"],
        "name": old_test_data["name"],
        "status": old_test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": old_test_data["tags"]
    }
    payload["photoUrls"][0] = test_data["photoUrls"][0]
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{old_test_data["name"]}"',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{test_data["photoUrls"][0]}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{old_test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_photo_urls_missing():
    # Generate random pet
    old_test_data = create_test_pet()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": old_test_data["category"],
        "name": old_test_data["name"],
        "status": old_test_data["status"],
        "tags": old_test_data["tags"]
    }

    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{old_test_data["name"]}"',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{old_test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_photo_urls_invalid_data_type():
    # Generate random pet
    old_test_data = create_test_pet()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": old_test_data["category"],
        "name": old_test_data["name"],
        "status": old_test_data["status"],
        "photoUrls": 123,
        "tags": old_test_data["tags"]
    }

    response = put("/v2/pet", payload, {"content-type": "application/json"})

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


def test_update_pet_put_json_photo_urls_empty_list():
    # Generate random pet
    old_test_data = create_test_pet()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": old_test_data["category"],
        "name": old_test_data["name"],
        "status": old_test_data["status"],
        "photoUrls": [],
        "tags": old_test_data["tags"]
    }

    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{old_test_data["name"]}"',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"photoUrls"',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{old_test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_photo_urls_null():
    # Generate random pet
    old_test_data = create_test_pet()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": old_test_data["category"],
        "name": old_test_data["name"],
        "status": old_test_data["status"],
        "photoUrls": None,
        "tags": old_test_data["tags"]
    }

    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{old_test_data["name"]}"',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{old_test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_status_valid_available_pending():
    # Generate random pet
    old_test_data = create_test_pet()

    # Generate updated random pet data
    test_data = generate_random_pet_data()
    test_data["status"] = "pending"

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": old_test_data["category"],
        "name": old_test_data["name"],
        "status": test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": old_test_data["tags"]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{old_test_data["name"]}"',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_status_valid_available_sold():
    # Generate random pet
    old_test_data = create_test_pet()

    # Generate updated random pet data
    test_data = generate_random_pet_data()
    test_data["status"] = "sold"

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": old_test_data["category"],
        "name": old_test_data["name"],
        "status": test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": old_test_data["tags"]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{old_test_data["name"]}"',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_status_valid_available_unsupported():
    # Generate random pet
    old_test_data = create_test_pet()

    # Generate updated random pet data
    test_data = generate_random_pet_data()
    test_data["status"] = "unsupported"

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": old_test_data["category"],
        "name": old_test_data["name"],
        "status": test_data["status"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": old_test_data["tags"]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{old_test_data["name"]}"',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}',
                                f'"status":"{test_data["status"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_status_missing():
    # Generate random pet
    old_test_data = create_test_pet()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": old_test_data["category"],
        "name": old_test_data["name"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": old_test_data["tags"]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{old_test_data["name"]}"',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_status_invalid_data_type():
    # Generate random pet
    old_test_data = create_test_pet()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": old_test_data["category"],
        "name": old_test_data["name"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": old_test_data["tags"],
        "status": 123
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{old_test_data["name"]}"',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}',
                                '"status":"123"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_status_null():
    # Generate random pet
    old_test_data = create_test_pet()

    # Perform a PUT request to update the pet
    payload = {
        "id": old_test_data["token"],
        "category": old_test_data["category"],
        "name": old_test_data["name"],
        "photoUrls": old_test_data["photoUrls"],
        "tags": old_test_data["tags"],
        "status": None
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{old_test_data["token"]}',
                                f'"name":"{old_test_data["name"]}"',
                                f'"category":{{"id":{old_test_data["category"]["id"]}',
                                f'"name":"{old_test_data["category"]["name"]}"}}',
                                '"photoUrls"', f'{old_test_data["photoUrls"][0]}',
                                '"tags"', f'{old_test_data["tags"][0]["id"]}',
                                f'{old_test_data["tags"][0]["name"]}'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_put_json_id_invalid_data_type():
    # Generate updated random pet data
    test_data = generate_random_pet_data()

    # Perform a PUT request to update the pet
    payload = {
        "id": "bad",
        "category": test_data["category"],
        "name": test_data["name"],
        "status": test_data["status"],
        "photoUrls": test_data["photoUrls"],
        "tags": test_data["tags"]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

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


# Skipping due to bug (expected 404, but returns 200)
@pytest.mark.skip(reason="Skipping due to bug (expected 404, but returns 200")
def test_update_pet_put_json_id_non_existing():
    # Find a non-existing pet ID
    bad_id = -1
    for i in range(1, 10):
        test_id = random.randint(1, 10000)
        response = get(f'/v2/pet/{test_id}')
        if response.status_code == 404:
            bad_id = test_id
            break

    # Generate updated random pet data
    test_data = generate_random_pet_data()

    # Perform a PUT request to update the pet
    payload = {
        "id": bad_id,
        "category": test_data["category"],
        "name": test_data["name"],
        "status": test_data["status"],
        "photoUrls": test_data["photoUrls"],
        "tags": test_data["tags"]
    }
    response = put("/v2/pet", payload, {"content-type": "application/json"})

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            404,
                            [], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


#
# POST /pet/:pet_id tests
#
def test_update_pet_post_form_all_fields_valid():
    # Generate random pet
    test_data = create_test_pet()

    # Generate updated random pet data
    new_test_data = generate_random_pet_data()

    # Perform a POST request to update the pet
    payload = {
        "name": new_test_data["name"],
        "status": "pending"
    }
    response = post(f'/v2/pet/{test_data["token"]}', None,
                    {"content-type": "application/x-www-form-urlencoded"}, None,
                    payload)

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                '"code":200',
                                '"type":"unknown"',
                                f'"message":"{test_data["token"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_schema_post_form():
    # Generate random pet
    test_data = create_test_pet()

    # Generate updated random pet data
    new_test_data = generate_random_pet_data()

    # Perform a POST request to update the pet
    payload = {
        "name": new_test_data["name"],
        "status": "pending"
    }
    response = post(f'/v2/pet/{test_data["token"]}', None,
                    {"content-type": "application/x-www-form-urlencoded"}, None,
                    payload)

    # Validate the outcome of the test with a single assert statement
    test_results = schema_validation("pet", "/v2/pet/:pet_id", "POST",
                                     response, False, True)
    assert test_results == "No mismatch values"


def test_update_pet_post_form_name_missing():
    # Generate random pet
    test_data = create_test_pet()

    # Perform a POST request to update the pet
    payload = {
        "status": "pending"
    }
    response = post(f'/v2/pet/{test_data["token"]}', None,
                    {"content-type": "application/x-www-form-urlencoded"}, None,
                    payload)

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                '"code":200',
                                '"type":"unknown"',
                                f'"message":"{test_data["token"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_post_form_name_over_1024_chars():
    # Generate random pet
    test_data = create_test_pet()

    # Perform a POST request to update the pet
    payload = {
        "name": string_gen(1025),
        "status": "pending"
    }
    response = post(f'/v2/pet/{test_data["token"]}', None,
                    {"content-type": "application/x-www-form-urlencoded"}, None,
                    payload)

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                '"code":200',
                                '"type":"unknown"',
                                f'"message":"{test_data["token"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_post_form_name_invalid_data_type():
    # Generate random pet
    test_data = create_test_pet()

    # Perform a POST request to update the pet
    payload = {
        "name": 123,
        "status": "pending"
    }
    response = post(f'/v2/pet/{test_data["token"]}', None,
                    {"content-type": "application/x-www-form-urlencoded"}, None,
                    payload)

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                '"code":200',
                                '"type":"unknown"',
                                f'"message":"{test_data["token"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_post_form_name_null():
    # Generate random pet
    test_data = create_test_pet()

    # Perform a POST request to update the pet
    payload = {
        "name": None,
        "status": "pending"
    }
    response = post(f'/v2/pet/{test_data["token"]}', None,
                    {"content-type": "application/x-www-form-urlencoded"}, None,
                    payload)

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                '"code":200',
                                '"type":"unknown"',
                                f'"message":"{test_data["token"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_post_form_status_missing():
    # Generate random pet
    test_data = create_test_pet()

    # Generate updated random pet data
    new_test_data = generate_random_pet_data()

    # Perform a POST request to update the pet
    payload = {
        "name": new_test_data["name"]
    }
    response = post(f'/v2/pet/{test_data["token"]}', None,
                    {"content-type": "application/x-www-form-urlencoded"}, None,
                    payload)

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                '"code":200',
                                '"type":"unknown"',
                                f'"message":"{test_data["token"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_post_form_status_unsupported():
    # Generate random pet
    test_data = create_test_pet()

    # Generate updated random pet data
    new_test_data = generate_random_pet_data()

    # Perform a POST request to update the pet
    payload = {
        "name": new_test_data["name"],
        "status": "unsupported"
    }
    response = post(f'/v2/pet/{test_data["token"]}', None,
                    {"content-type": "application/x-www-form-urlencoded"}, None,
                    payload)

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                '"code":200',
                                '"type":"unknown"',
                                f'"message":"{test_data["token"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_post_form_status_invalid_data_type():
    # Generate random pet
    test_data = create_test_pet()

    # Generate updated random pet data
    new_test_data = generate_random_pet_data()

    # Perform a POST request to update the pet
    payload = {
        "name": new_test_data["name"],
        "status": 123
    }
    response = post(f'/v2/pet/{test_data["token"]}', None,
                    {"content-type": "application/x-www-form-urlencoded"}, None,
                    payload)

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                '"code":200',
                                '"type":"unknown"',
                                f'"message":"{test_data["token"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_post_form_status_null():
    # Generate random pet
    test_data = create_test_pet()

    # Generate updated random pet data
    new_test_data = generate_random_pet_data()

    # Perform a POST request to update the pet
    payload = {
        "name": new_test_data["name"],
        "status": None
    }
    response = post(f'/v2/pet/{test_data["token"]}', None,
                    {"content-type": "application/x-www-form-urlencoded"}, None,
                    payload)

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                '"code":200',
                                '"type":"unknown"',
                                f'"message":"{test_data["token"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_post_form_id_bad():
    # Generate updated random pet data
    new_test_data = generate_random_pet_data()

    # Perform a POST request to update the pet
    payload = {
        "name": new_test_data["name"],
        "status": "pending"
    }
    response = post(f'/v2/pet/bad', None,
                    {"content-type": "application/x-www-form-urlencoded"}, None,
                    payload)

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            404,
                            [
                                '"code":404',
                                '"type":"unknown"',
                                f'"message":"java.lang.NumberFormatException: For input string:'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_update_pet_post_form_id_non_existing():
    # Find a non-existing pet ID
    bad_id = -1
    for i in range(1, 10):
        test_id = random.randint(1, 10000)
        response = get(f'/v2/pet/{test_id}')
        if response.status_code == 404:
            bad_id = test_id
            break

    # Generate updated random pet data
    new_test_data = generate_random_pet_data()

    # Perform a POST request to update the pet
    payload = {
        "name": new_test_data["name"],
        "status": "pending"
    }
    response = post(f'/v2/pet/{bad_id}', None,
                    {"content-type": "application/x-www-form-urlencoded"}, None,
                    payload)

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            404,
                            [
                                '"code":404',
                                '"type":"unknown"',
                                f'"message":"not found"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


#
# DELETE /pet/:pet_id tests
#
def test_delete_pet():
    # Generate random pet
    test_data = create_test_pet()

    # Fetch pet
    response = delete(f'/v2/pet/{test_data["token"]}')

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                '"code":200',
                                '"type":"unknown"',
                                f'"message":"{test_data["token"]}"'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_delete_pet_schema():
    # Generate random pet
    test_data = create_test_pet()

    # Delete pet
    response = delete(f'/v2/pet/{test_data["token"]}')

    # Validate the outcome of the test with a single assert statement
    test_results = schema_validation("pet", "/v2/pet/:pet_id", "DELETE",
                                     response, False, True)
    assert test_results == "No mismatch values"


def test_delete_pet_with_bad_token():
    # Fetch pet
    response = delete('/v2/pet/bad')

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            404,
                            [
                                '"type":"unknown"',
                                '"message":"java.lang.NumberFormatException: For input string',
                                'bad'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


#
# Pet Clean-up
#
def test_cleanup_created_pets():
    print(f"\n\nPost suite pet cleanup...")
    for pet_id in created_pet_ids:
        response = delete(f"/v2/pet/{pet_id}")
        if response.status_code == 200:
            print(f"Deleted pet with ID {pet_id}")
        else:
            print(f"Failed to delete pet with ID {pet_id}, status code: {response.status_code}")
