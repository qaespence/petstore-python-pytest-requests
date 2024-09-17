from test.api.basic_requests import post, get, put, delete


def add_pet(pet_id=None, category=None, name=None, status=None, photo_urls=None, tags=None):
    """
    Test the functionality of adding a new pet to the Pet Store with the updated payload structure.

    Parameters:
    - pet_id (int, optional): ID of the pet.
    - category (dict, optional): A dictionary containing 'id' and 'name' for the category.
    - name (str, optional): Name of the pet to be added.
    - status (str, optional): Status of the pet to be added.
    - photo_urls (list, optional): List of photo URLs for the pet.
    - tags (list, optional): List of tags for the pet, each a dictionary with 'id' and 'name'.

    Returns:
    - If the pet is successfully added, return a tuple containing the JSON response and the HTTP status code with a status code of 201.
    - If there is an error during the request, return a tuple containing the error message and the HTTP status code received in the response.
    """

    # Initialize the payload
    payload = {}

    # Add parameters to the payload if they are provided
    if pet_id is not None:
        payload["id"] = pet_id

    if category is not None:
        payload["category"] = category

    if name is not None:
        payload["name"] = name

    if status is not None:
        payload["status"] = status

    if photo_urls is not None:
        payload["photoUrls"] = photo_urls

    if tags is not None:
        payload["tags"] = tags

    # Make the POST request
    return post("/v2/pet", payload, {"content-type": "application/json"})


def get_pet(pet_id):
    """
    Test the functionality of retrieving a pet from the Pet Store by ID.

    Parameters:
    - pet_id (int): The unique identifier of the pet to retrieve.

    Returns:
    - If the pet is found, return a tuple containing the JSON response and the HTTP status code with a status code of 200.
    - If the pet is not found, return a tuple containing the error message 'Pet not found' and the HTTP status code with a status code of 404.
    - If there is an error during the request, return a tuple containing the error message and the HTTP status code received in the response.
    """

    return get(f"/v2/pet/{pet_id}")


def delete_pet(pet_id):
    """
    Test the functionality of deleting a pet from the Pet Store by ID.

    Parameters:
    - pet_id (int): The unique identifier of the pet to delete.

    Returns:
    - If the pet is successfully deleted, return a tuple containing the success message and the HTTP status code with a status code of 200.
    - If the pet is not found, return a tuple containing the error message 'Pet not found' and the HTTP status code with a status code of 404.
    - If there is an error during the request, return a tuple containing the error message and the HTTP status code received in the response.
    """

    return delete(f"/v2/pet/{pet_id}")

