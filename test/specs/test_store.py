from test.helpers.utils import (generate_random_store_order_data, set_debug_file_name,
                                api_test, clear_log_file, schema_validation)
from test.api.basic_requests import post, delete
import json

created_order_ids = []


def test_setup():
    set_debug_file_name("api_store")
    clear_log_file("api_store")


#
# POST /store/order tests
#
def test_add_store_order():
    """
        Test the functionality of adding a new store order to the Pet Store.

        Actions:
        - Generate random store order data.
        - Perform a POST request to add a new store order with the generated data.
        - Retrieve the JSON response and HTTP status code.

        Expected Outcome:
        - The status code should be 201, indicating a successful addition.
        - The response JSON should contain the added store order's information.
        - The added store order data should match the generated data.
        - Cleanup: The added order ID is stored for later removal.
        """
    # Generate random order data
    test_data = generate_random_store_order_data()

    # Perform a POST request to add a new order
    payload = {
        "id": test_data["id"],
        "petId": test_data["pet_id"],
        "quantity": test_data["quantity"],
        "shipDate": test_data["ship_date"],
        "status": test_data["status"],
        "complete": test_data["complete"]
    }
    response = post("/v2/store/order", payload, {"content-type": "application/json"})
    order = json.loads(response.text)

    # Store the created pet ID for cleanup
    created_order_ids.append(order['id'])

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"id":{test_data["id"]}',
                                f'"petId":{test_data["pet_id"]}',
                                f'"quantity":{test_data["quantity"]}',
                                f'"shipDate":"{test_data["ship_date"]}"',
                                f'"status":"{test_data["status"].replace("Z", "+0000")}"',
                                f'"complete":{str(test_data["complete"]).lower()}'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_store_order_schema():
    """
        Test the schema of adding a new store order to the Pet Store.

        Actions:
        - Generate random store order data.
        - Perform a POST request to add a new store order with the generated data.
        - Retrieve the JSON response and HTTP status code.

        Expected Outcome:
        - The response body and headers should match the known good schema.
        - Cleanup: The added order ID is stored for later removal.
        """
    # Generate random order data
    test_data = generate_random_store_order_data()

    # Perform a POST request to add a new order
    payload = {
        "id": test_data["id"],
        "petId": test_data["pet_id"],
        "quantity": test_data["quantity"],
        "shipDate": test_data["ship_date"],
        "status": test_data["status"],
        "complete": test_data["complete"]
    }
    response = post("/v2/store/order", payload, {"content-type": "application/json"})
    order = json.loads(response.text)

    # Store the created pet ID for cleanup
    created_order_ids.append(order['id'])

    # Validate the outcome of the test with a single assert statement
    test_results = schema_validation("store", "/v2/store/order", "POST",
                                     response, True, True)
    assert test_results == "No mismatch values"


def test_add_store_order_id_missing():
    # Generate random order data
    test_data = generate_random_store_order_data()

    # Perform a POST request to add a new order
    payload = {
        "petId": test_data["pet_id"],
        "quantity": test_data["quantity"],
        "shipDate": test_data["ship_date"],
        "status": test_data["status"],
        "complete": test_data["complete"]
    }
    response = post("/v2/store/order", payload, {"content-type": "application/json"})
    order = json.loads(response.text)

    # Store the created pet ID for cleanup
    created_order_ids.append(order['id'])

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"petId":{test_data["pet_id"]}',
                                f'"quantity":{test_data["quantity"]}',
                                f'"shipDate":"{test_data["ship_date"]}"',
                                f'"status":"{test_data["status"].replace("Z", "+0000")}"',
                                f'"complete":{str(test_data["complete"]).lower()}'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_store_order_id_invalid_data_type():
    # Generate random order data
    test_data = generate_random_store_order_data()

    # Perform a POST request to add a new order
    payload = {
        "id": "bad",
        "petId": test_data["pet_id"],
        "quantity": test_data["quantity"],
        "shipDate": test_data["ship_date"],
        "status": test_data["status"],
        "complete": test_data["complete"]
    }
    response = post("/v2/store/order", payload, {"content-type": "application/json"})

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


def test_add_store_order_id_invalid_negative_1():
    # Generate random order data
    test_data = generate_random_store_order_data()

    # Perform a POST request to add a new order
    payload = {
        "id": -1,
        "petId": test_data["pet_id"],
        "quantity": test_data["quantity"],
        "shipDate": test_data["ship_date"],
        "status": test_data["status"],
        "complete": test_data["complete"]
    }
    response = post("/v2/store/order", payload, {"content-type": "application/json"})
    order = json.loads(response.text)

    # Store the created pet ID for cleanup
    created_order_ids.append(order['id'])

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"petId":{test_data["pet_id"]}',
                                f'"quantity":{test_data["quantity"]}',
                                f'"shipDate":"{test_data["ship_date"]}"',
                                f'"status":"{test_data["status"].replace("Z", "+0000")}"',
                                f'"complete":{str(test_data["complete"]).lower()}'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_store_order_id_zero():
    # Generate random order data
    test_data = generate_random_store_order_data()

    # Perform a POST request to add a new order
    payload = {
        "id": 0,
        "petId": test_data["pet_id"],
        "quantity": test_data["quantity"],
        "shipDate": test_data["ship_date"],
        "status": test_data["status"],
        "complete": test_data["complete"]
    }
    response = post("/v2/store/order", payload, {"content-type": "application/json"})
    order = json.loads(response.text)

    # Store the created pet ID for cleanup
    created_order_ids.append(order['id'])

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"petId":{test_data["pet_id"]}',
                                f'"quantity":{test_data["quantity"]}',
                                f'"shipDate":"{test_data["ship_date"]}"',
                                f'"status":"{test_data["status"].replace("Z", "+0000")}"',
                                f'"complete":{str(test_data["complete"]).lower()}'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


def test_add_store_order_id_null():
    # Generate random order data
    test_data = generate_random_store_order_data()

    # Perform a POST request to add a new order
    payload = {
        "id": None,
        "petId": test_data["pet_id"],
        "quantity": test_data["quantity"],
        "shipDate": test_data["ship_date"],
        "status": test_data["status"],
        "complete": test_data["complete"]
    }
    response = post("/v2/store/order", payload, {"content-type": "application/json"})
    order = json.loads(response.text)

    # Store the created pet ID for cleanup
    created_order_ids.append(order['id'])

    # Validate the outcome of the test with a single assert statement
    test_results = api_test(response, response.status_code,
                            200,
                            [
                                f'"petId":{test_data["pet_id"]}',
                                f'"quantity":{test_data["quantity"]}',
                                f'"shipDate":"{test_data["ship_date"]}"',
                                f'"status":"{test_data["status"].replace("Z", "+0000")}"',
                                f'"complete":{str(test_data["complete"]).lower()}'
                            ], None,
                            ['"Content-Type": "application/json"',
                             '"Transfer-Encoding": "chunked"',
                             '"Connection": "keep-alive"',
                             '"Access-Control-Allow-Origin": "*"',
                             '"Access-Control-Allow-Methods": "GET, POST, DELETE, PUT"',
                             '"Access-Control-Allow-Headers": "Content-Type, api_key, Authorization"'])
    assert test_results == "No mismatch values"


#
# Order Clean-up
#
def test_cleanup_created_order():
    print(f"\n\nPost suite order cleanup...")
    for order_id in created_order_ids:
        response = delete(f"/v2/store/order/{order_id}")
        if response.status_code == 200:
            print(f"Deleted order with ID {order_id}")
        else:
            print(f"Failed to delete order with ID {order_id}, status code: {response.status_code}")