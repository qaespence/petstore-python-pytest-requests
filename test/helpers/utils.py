import random
import string
import json
from datetime import datetime
import os
from faker import Faker
from flatdict import FlatDict
import logging

fake = Faker()
debug_file_name = ""


def load_config():
    with open("../config/config.json", "r") as config_file:
        config_data = json.load(config_file)
    return config_data


def generate_random_pet_data(pet_id=None, category_id=None, name=None, category=None, status=None, photo_urls=None,
                             tags=None):
    """
    Generate random pet data with optional overrides using Faker for realistic random data.

    Parameters:
    - pet_id (int, optional): The ID of the pet. If None, a random ID will be generated.
    - category_id (int, optional): The ID of the category. If None, a random ID will be generated.
    - name (str, optional): The name of the pet. If None, a random name will be generated using Faker.
    - category (str, optional): The category of the pet. If None, a random category will be generated.
    - status (str, optional): The status of the pet. If None, a random status will be generated.
    - photo_urls (list, optional): The photo URLs for the pet. If None, random photo URLs will be generated using Faker.
    - tags (list, optional): The tags for the pet. If None, random tags will be generated using Faker.

    Returns:
    - dict: A dictionary containing the pet data in the desired format.
    """

    def random_id():
        return random.randint(1, 10000)

    def random_array(length_range=(1, 3), element_generator=fake.url):
        return [element_generator() for _ in range(random.randint(*length_range))]

    # Predefined lists of categories and statuses
    categories = ["Dog", "Cat", "Bird", "Fish", "Reptile"]
    statuses = ["available", "pending", "sold"]

    # Use provided values or generate random ones using Faker
    pet_id = pet_id if pet_id is not None else random_id()
    category_id = category_id if category_id is not None else random_id()
    pet_name = name if name else fake.first_name()
    pet_category = category if category else random.choice(categories)
    pet_status = status if status else random.choice(statuses)

    # Generate random photoUrls and tags arrays using Faker
    photo_urls = photo_urls if photo_urls else random_array()
    tags = tags if tags else [{"id": random_id(), "name": fake.word()} for _ in range(random.randint(1, 3))]

    return {
        "id": pet_id,
        "category": {
            "id": category_id,
            "name": pet_category
        },
        "name": pet_name,
        "photoUrls": photo_urls,
        "tags": tags,
        "status": pet_status
    }


def verify_status_code(expected_status_code, actual_status_code):
    if expected_status_code == actual_status_code:
        return None
    else:
        return "Expected status " + str(expected_status_code) + " does not match actual status " + str(
            actual_status_code) + "\n"


def compiled_results(results: list):
    if results == [[]] or results == []:
        return "No mismatch values"
    else:
        final_results = ""
        for result in results:
            final_results = final_results + str(result) + "\n"
        final_results = final_results + "\n\nThere were " + str(len(results)) + " mismatches!\n"
        return final_results


def verify_expected_response_text(expected_response_text, response_body):
    results = []
    for text in expected_response_text:
        if str(text) not in response_body:
            results.append("Expected string \"" + str(text) + "\" does NOT appear in results content\n\n")
    if results is not []:
        return results
    else:
        return None


def verify_unexpected_response_text(unexpected_response_text, response_body):
    results = []
    for text in unexpected_response_text:
        if str(text) in response_body:
            results.append("Unexpected string \"" + str(text) + "\" DOES appear in results content\n\n")
    if results is not []:
        return results
    else:
        return None


def api_test(response, actual_status_code: int = None,
             expected_status_code: int = None,
             expected_response_text: list = None,
             unexpected_response_text: list = None,
             expected_headers_text: list = None,
             unexpected_headers_text: list = None):
    results = []
    if expected_status_code is not None:
        temp_results = verify_status_code(expected_status_code, actual_status_code)
        if temp_results is not None:
            results = results + [temp_results]

    if expected_response_text is not None:
        temp_results = verify_expected_response_text(expected_response_text, response.text)
        if temp_results is not None:
            results = results + temp_results

    if unexpected_response_text is not None:
        temp_results = verify_unexpected_response_text(unexpected_response_text,
                                                       json.dumps(dict(response.headers), indent=2))
        if temp_results is not None:
            results = results + temp_results

    if expected_headers_text is not None:
        temp_results = verify_expected_response_text(expected_headers_text,
                                                     json.dumps(dict(response.headers), indent=2))
        if temp_results is not None:
            results = results + temp_results

    if unexpected_headers_text is not None:
        temp_results = verify_unexpected_response_text(unexpected_headers_text, response.headers)
        if temp_results is not None:
            results = results + temp_results

    return compiled_results(results)


def set_debug_file_name(suite_name: str = "unnamed"):
    global debug_file_name
    debug_file_name = suite_name


def curl_builder(url: str, payload: dict, method: str, headers: dict):
    command = "curl -svX "
    command = command + method.upper() + " " + url + " "
    if headers is not None:
        for key, value in headers.items():
            command = command + "-H {'" + key + "':'" + value + "'} "
    if payload is not None:
        command = command + "-d '" + json.dumps(payload) + "'"
    return command


def api_logger(endpoint: str, payload: dict, headers: dict, response: str, method: str,
               start_time: datetime, end_time: datetime):
    log_dir = os.path.join('..', 'logs')
    log_file = os.path.join(log_dir, f"{debug_file_name}.log")

    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)

    total_duration = end_time - start_time
    config = load_config()
    url = f"{config['base_url']}{endpoint}"
    rebuilt_curl = curl_builder(url, payload, method, headers)
    log_entry = (
        "{\n"
        f"\tendpoint: {endpoint}\n"
        f"\turl: {url}\n"
        f"\ttime: {datetime.now()}\n"
        f"\tCURL: {rebuilt_curl}\n"
        f"\tduration: {int(total_duration.microseconds / 1000)} ms\n"
        f"\tpayload: {json.dumps(payload)}\n"
        f"\theaders: {json.dumps(headers)}\n"
        f"\tresponse: {''.join(response.splitlines())}\n"
        "}\n"
    )
    with open(log_file, 'a') as file:
        file.write(log_entry)


def clear_log_files():
    """
    Finds and deletes all .log files in the logs directory.
    """
    log_dir = os.path.join('..', 'logs')

    # Create the directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Created log directory: {log_dir}")
    else:
        # Iterate over all files in the directory
        for file_name in os.listdir(log_dir):
            # Check if the file has a .log extension
            if file_name.endswith('.log'):
                log_file = os.path.join(log_dir, file_name)
                if os.path.isfile(log_file):
                    os.remove(log_file)
                    # print(f"Deleted log file: {log_file}")


# Setup logging (can also log to file if needed)
logging.basicConfig(level=logging.INFO)


def api_debugger(api_response):
    """
    Debugs the details of an API response, including status code, body, headers, and schema types.

    Parameters:
    - api_response: Response object from an HTTP request (for example, from the 'requests' library).
    """

    body_json = {}
    logging.info("\nAPI DEBUGGER\n\n")

    # Status code
    logging.info("\nSTATUS CODE: %s", api_response.status_code)

    # Raw JSON Body
    try:
        body_json = api_response.json()
        logging.info("\nRaw JSON Body: %s", json.dumps(body_json))
    except ValueError:
        logging.info("\nRaw JSON Body: %s", api_response.text)  # In case body is not JSON

    # Raw Headers
    logging.info("\nRaw Headers: %s", json.dumps(dict(api_response.headers)))

    # Raw Text Body
    logging.info("\nRaw Text Body: %s", api_response.text)

    # Log payload schema
    try:
        flattened_body = FlatDict(body_json, delimiter='.')
        results = {key: type(value).__name__ for key, value in flattened_body.items()}
        logging.info("\nPayload schema: %s", json.dumps(results, indent=2))
    except Exception as e:
        logging.error("Error flattening body: %s", e)

    # Log headers schema
    header_schema = {key: type(value).__name__ for key, value in api_response.headers.items()}
    logging.info("\nHeader schema: %s", json.dumps(header_schema, indent=2))

    logging.info("\nEND API DEBUGGER\n\n")


def schema_validation(service, endpoint, method, response=None, payload_must_match=False,
                      headers_must_match=False):
    """
    Validates the response body and headers against the schema defined in the schemaDB.json file.

    Parameters:
    - service (str): The service name (e.g., 'pet').
    - endpoint (str): The endpoint (e.g., '/v2/pet').
    - method (str): The HTTP method (e.g., 'POST').
    - response_body (dict, optional): The actual response body to validate.
    - response_headers (dict, optional): The actual response headers to validate.
    - payload_must_match (bool): If True, additional checks are made to ensure the payload exactly matches the schema.
    - headers_must_match (bool): If True, additional checks are made to ensure the headers exactly match the schema.

    Returns:
    - str: A string summarizing the validation results.
    """
    # Load the API schema database
    with open('../api/schema_db.json') as schema_file:
        api_schema_db = json.load(schema_file)

    flattened_actual_body = {}
    results = []

    # Validate the response body if provided
    if response is not None:
        try:
            body_json = response.json()
            flattened_actual_body = FlatDict(body_json, delimiter='.')
        except ValueError:
            print("Error occurs when flattening body")

        expected_payload = api_schema_db[service][endpoint][method]["body"]

        # Compare expected payload vs actual response body
        for key, expected_type in expected_payload.items():
            if key in flattened_actual_body:
                actual_value = flattened_actual_body[key]
                actual_type = type(actual_value).__name__
                if actual_type != expected_type:
                    results.append(
                        f"(BODY) Element > {key} < expected to be > {expected_type} < but actually > {actual_type} <\n")
            else:
                results.append(f"(BODY) Element > {key} < missing from schema\n")

        # Check for additional keys in the actual payload if payloadMustMatch is True
        if payload_must_match:
            for key in flattened_actual_body:
                if key not in expected_payload:
                    results.append(
                        f"Key      : {key}\n"
                        f"Test     : MISSING\n"
                        f"Expected : Element present\n"
                        f"Actual   : Element in payload but not in schema DB \n\n"
                    )

    # Validate the response headers if provided
    if response is not None:
        flattened_actual_headers = FlatDict(response.headers, delimiter='.')
        expected_headers = api_schema_db[service][endpoint][method]["headers"]

        # Compare expected headers vs actual response headers
        for key, expected_type in expected_headers.items():
            if key in flattened_actual_headers:
                actual_value = flattened_actual_headers[key]
                actual_type = type(actual_value).__name__
                if actual_type != expected_type:
                    results.append(
                        f"(HEADERS) Element > {key} < expected to be > {expected_type} < but actually > {actual_type} <\n")
            else:
                results.append(f"(HEADERS) Element > {key} < missing from schema\n")

        # Check for additional keys in the actual headers if headersMustMatch is True
        if headers_must_match:
            for key in flattened_actual_headers:
                if key not in expected_headers:
                    results.append(
                        f"Key      : {key}\n"
                        f"Test     : MISSING\n"
                        f"Expected : Element present\n"
                        f"Actual   : Element in headers but not in schema DB \n\n"
                    )

    # Summarize results
    if results:
        return f"\n{''.join(results)}\nThere are {len(results)} mismatches!\n"
    else:
        return "No mismatch values"