import string
import sys

import requests

import connectionController

# asserts the status code
def assert_status_code(response: requests.Response, status_code: int):
    assert response.status_code == status_code

# asserts the returned value
def assert_ret_value(response: requests.Response, returned_value: any):
    assert response.json() == returned_value

# asserts a valid returned value of a post request
# if the id of a dish/meal posted is positive then it's valid
# otherwise, the post request was invalid
def assert_valid_added_resource(response: requests.Response):
    assert response.status_code == 201
    # should be positive ID
    VALID_RETURNED_RESOURCE_ID = 0
    print("print(response.json()) > 0? response.json() =")
    print(response.json())
    sys.stdout.flush()
    assert response.json() > VALID_RETURNED_RESOURCE_ID

# def assert_unique_id(dish_identifier: any, dishes_ids) -> None:
#     assert dish_identifier not in dishes_ids

# asserts that a given dish doesn't exist because ninja api can't find it

def assert_non_existing_dish(response: requests.Response, acceptable_codes) -> None:
    assert response.status_code in acceptable_codes, f"Unexpected status code: {response.status_code}"
    assert_ret_value(response, returned_value=-3)

# def assert_non_existing_dish(dish_identifier: any, acceptable_codes) -> None:
#     response = connectionController.http_post("dishes", {"name": dish_identifier})
#     assert response.status_code in acceptable_codes, f"Unexpected status code: {response.status_code}"
#     assert_ret_value(response, returned_value=-3)



# asserts that a given dish is already in the dish collection
def assert_dish_exists(dish_identifier: any, acceptable_codes) -> None:
    response = connectionController.http_post("dishes", {"name": dish_identifier})
    assert response.status_code in acceptable_codes, f"Unexpected status code: {response.status_code}"
    assert_ret_value(response, returned_value=-2)

# asserts that a given meal is already in the meal collection
def assert_meal_exists(meal_identifier: any, dishes, acceptable_codes) -> None:
    meal = {
        "name": meal_identifier,
        "appetizer": dishes[0],
        "main": dishes[1],
        "dessert": dishes[2]
    }
    response = connectionController.http_post("meals", meal)
    assert response.status_code in acceptable_codes, f"Unexpected status code: {response.status_code}"
    assert_ret_value(response, returned_value=-2)
