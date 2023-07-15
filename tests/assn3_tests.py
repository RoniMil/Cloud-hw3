import sys

import connectionController
from assertions import *

dish_col = {}
meal_col = {}


# helper functions

def get_dish_ID_by_name(col, dishName):
    for dish_id, dish in col.items():
        if dish.get("name") == dishName:
            return dish_id
    return 0

def get_dishes_ids(col, dishes):
    dishes_ids = []
    for dish in dishes:
        dishes_ids.append(get_dish_ID_by_name(col, dish))
    return dishes_ids


# def get_dish_by_id(dish_id):
#     resource = f"dishes/{dish_id}"
#     response = connectionController.http_get(resource)
#     return response
#
#
# def get_dish_by_name(dish_name):
#     resource = f"dishes/{dish_name}"
#     response = connectionController.http_get(resource)
#     return response
#
#
# def get_meal_by_id(meal_id):
#     resource = f"meals/{meal_id}"
#     response = connectionController.http_get(resource)
#     return response
#
#
# def get_meal_by_name(meal_name):
#     resource = f"meals/{meal_name}"
#     response = connectionController.http_get(resource)
#     return response

# tests for dishes service

def test1():
    dishes = ["orange", "spaghetti", "apple pie"]
    for dish in dishes:
        response = connectionController.http_post("dishes", {"name": dish})
        # asserts the dish is valid and can be added
        assert_valid_added_resource(response)
        dish_id = response.json()
        dish_json = connectionController.http_get(f"dishes/{dish_id}").json()
        curr_dishes = connectionController.http_get("dishes").json()
        # asserts the given id of the dish we add is unique
        assert dish_id not in get_dishes_ids(dish_col, curr_dishes)
        dish_col[dish_id] = dish_json

# !!! add assert correct form to post tests? !!!

def test2():
    dish_name = "orange"
    orange_id = get_dish_ID_by_name(dish_col, dish_name)
    # asserts the id of orange is valid
    assert orange_id > 0
    response = connectionController.http_get(f"dishes/{orange_id}")
    response_json = response.json()
    # asserts the sodium value of orange is in range
    assert (0.9 <= response_json["sodium"] <= 1.1)
    # asserts the status code of the request is 200 - successful
    assert_status_code(response, status_code=200)

def test3():
    response = connectionController.http_get("dishes")
    response_json = response.json()
    # asserts that the dish collection has 3 dishes in it
    assert len(response_json) == 3
    # asserts the return code in 200
    assert_status_code(response, status_code=200)


def test4():
    response = connectionController.http_post("dishes", {"name": "blah"})
    assert_non_existing_dish(response, [404, 400, 422])

def test5():
    response = connectionController.http_post("dishes", {"name": "orange"})
    assert_item_exists(response, [400, 404, 422])

# tests for meals service
def test6():
    dishes = ["orange", "spaghetti", "apple pie"]
    for dish in dishes:
        dish_response = connectionController.http_post("dishes", {"name": dish})
        # asserts that the dishes are in the dish collection and thus are able to be added to a meal
        assert_item_exists(dish_response, [400, 404, 422])
    dishes_ids = get_dishes_ids(dish_col, dishes)
    meal = {
        "name": "delicious",
        "appetizer": dishes_ids[0],
        "main": dishes_ids[1],
        "dessert": dishes_ids[2]
    }
    response = connectionController.http_post("meals", meal)
    # asserts the meal is valid and can be added and that the status return code is 201
    assert_valid_added_resource(response)
    meal_id = response.json()
    meal_json = connectionController.http_get(f"meals/{meal_id}").json()
    meal_col[response.json()] = meal_json

def test7():
    response = connectionController.http_get("meals")
    meals = response.json()
    print("meals: ", meals)
    assert len(meals) == 1
    for meal in meals:
        if meal.get("name") == "delicious":
            assert (400 <= meal["calories"] <= 500)
    assert_status_code(response, status_code=200)

def test8():
    dishes = ["apple pie", "spaghetti", "orange"]
    dishes_ids = get_dishes_ids(dish_col, dishes)
    meal = {
        "name": "delicious",
        "appetizer": dishes_ids[0],
        "main": dishes_ids[1],
        "dessert": dishes_ids[2]
    }
    response = connectionController.http_post("meals", meal)
    assert_item_exists(response, [400, 422])


#
#     dishes = ["apple pie", "spaghetti", "orange"]
#     dishes_ids = get_dishes_ids(dish_col, dishes)
#     assert_meal_exists("delicious", dishes_ids, [400, 422])

# # chat gpt stuff
#
# import sys
# from assertions import *
# from connectionController import *
#
#
# def test_dishes_service():
#     # Test 1: Execute three POST /dishes requests
#     dish_names = ["orange", "spaghetti", "apple pie"]
#     dish_ids = []
#     for name in dish_names:
#         data = {"name": name}
#         response = http_post('dishes', data)
#         assert_status_code(response, 201)
#         dish_id = response.json().get('id')
#         assert dish_id not in dish_ids
#         dish_ids.append(dish_id)
#
#     # Test 2: Execute a GET dishes/<orange-ID> request
#     orange_id = dish_ids[dish_names.index("orange")]
#     response = http_get(f'dishes/{orange_id}')
#     assert_status_code(response, 200)
#     sodium_value = response.json().get('sodium')
#     assert 0.9 <= sodium_value <= 1.1
#
#     # Test 3: Execute a GET /dishes request
#     response = http_get('dishes')
#     assert_status_code(response, 200)
#     dishes = response.json()
#     assert len(dishes) == 3
#
#     # Test 4: Execute a POST /dishes request with dish name "blah"
#     data = {"name": "blah"}
#     response = http_post('dishes', data)
#     assert response.status_code in [404, 400, 422]
#     assert response.json().get('return_value') == -3
#
#     # Test 5: Perform a POST dishes request with dish name "orange"
#     data = {"name": "orange"}
#     response = http_post('dishes', data)
#     assert response.status_code in [400, 404, 422]
#     assert response.json().get('return_value') == -2
#
#
# def test_meals_service():
#     # Test 6: Perform a POST /meals request
#     dish_ids = [1, 2, 3]  # Replace with actual dish IDs
#     data = {
#         "name": "delicious",
#         "appetizer_id": dish_ids[0],
#         "main_id": dish_ids[1],
#         "dessert_id": dish_ids[2]
#     }
#     response = http_post('meals', data)
#     assert_status_code(response, 201)
#     meal_id = response.json().get('id')
#     assert meal_id > 0
#
#     # Test 7: Perform a GET /meals request
#     response = http_get('meals')
#     assert_status_code(response, 200)
#     meals = response.json()
#     assert len(meals) == 1
#     meal = meals[0]
#     assert 400 <= meal.get('calories') <= 500
#
#     # Test 8: Perform a POST /meals request with same meal name
#     data = {
#         "name": "delicious",
#         "appetizer_id": dish_ids[0],
#         "main_id": dish_ids[1],
#         "dessert_id": dish_ids[2]
#     }
#     response = http_post('meals', data)
#     assert response.status_code in [400, 422]
#     assert response.json().get('return_value') == -2
#
#
# if __name__ == '__main__':
#     # Run the test functions
#     test_dishes_service()
#     test_meals_service()
#
# # more chat gpt stuff
#
# import pytest
# import requests
#
#
# # Helper function to send a POST request and return the response
# def post_request(url, json_data):
#     response = requests.post(url, json=json_data)
#     return response
#
#
# # Helper function to send a GET request and return the response
# def get_request(url):
#     response = requests.get(url)
#     return response
#
#
# @pytest.fixture
# def base_url():
#     # Set the base URL for the services
#     return "http://localhost:5001"
#
#
# # Test 1: Execute three POST /dishes requests
# def test_post_dishes(base_url):
#     dishes = ["orange", "spaghetti", "apple pie"]
#     dish_ids = set()
#     status_codes = set()
#
#     for dish in dishes:
#         json_data = {"name": dish}
#         response = post_request(f"{base_url}/dishes", json_data)
#         dish_ids.add(response.json().get("id"))
#         status_codes.add(response.status_code)
#
#     assert len(dish_ids) == 3  # Unique dish IDs
#     assert all(status_code == 201 for status_code in status_codes)  # Return status code is 201
#
#
# # Test 2: Execute a GET dishes/<orange-ID> request
# def test_get_dish_by_id(base_url):
#     dish_id = "<orange-ID>"  # Replace with actual orange dish ID
#     response = get_request(f"{base_url}/dishes/{dish_id}")
#     json_data = response.json()
#     sodium = json_data.get("sodium")
#
#     assert sodium is not None and 0.9 <= sodium <= 1.1  # Sodium field is between .9 and 1.1
#     assert response.status_code == 200  # Return status code is 200
#
#
# # Test 3: Execute a GET /dishes request
# def test_get_dishes(base_url):
#     response = get_request(f"{base_url}/dishes")
#     json_data = response.json()
#
#     assert len(json_data) == 3  # 3 embedded JSON objects (dishes)
#     assert response.status_code == 200  # Return status code is 200
#
#
# # Test 4: Execute a POST /dishes request supplying the dish name "blah"
# def test_post_dishes_invalid(base_url):
#     json_data = {"name": "blah"}
#     response = post_request(f"{base_url}/dishes", json_data)
#
#     assert response.json().get("return_value") == -3  # Return value is -3
#     assert response.status_code in (404, 400, 422)  # Return status code is 404, 400, or 422
#
#
# # Test 5: Perform a POST dishes request with the dish name "orange"
# def test_post_dishes_duplicate(base_url):
#     json_data = {"name": "orange"}
#     response = post_request(f"{base_url}/dishes", json_data)
#
#     assert response.json().get("return_value") == -2  # Return value is -2
#     assert response.status_code in (400, 404, 422)  # Return status code is 400, 404, or 422
#
#
# # Test 6: Perform a POST /meals request
# def test_post_meals(base_url):
#     json_data = {
#         "name": "delicious",
#         "appetizer": "<orange-ID>",  # Replace with actual orange dish ID
#         "main": "<spaghetti-ID>",  # Replace with actual spaghetti dish ID
#         "dessert": "<apple-pie-ID>"  # Replace with actual apple pie dish ID
#     }
#     response = post_request(f"{base_url}/meals", json_data)
#     meal_id = response.json().get("id")
#
#     assert meal_id is not None and meal_id > 0  # Returned ID > 0
#     assert response.status_code == 201  # Return status code is 201
#
#
# # Test 7: Perform a GET /meals request
# def test_get_meals(base_url):
#     response = get_request(f"{base_url}/meals")
#     json_data = response.json()
#
#     assert len(json_data) == 1  # 1 meal
#     assert 400 <= json_data[0].get("calories") <= 500  # Calories between 400 and 500
#     assert response.status_code == 200  # Return status code is 200
#
#
# # Test 8: Perform a POST /meals request as in test 6 with the same meal name
# def test_post_meals_duplicate(base_url):
#     json_data = {
#         "name": "delicious",
#         "appetizer": "<orange-ID>",  # Replace with actual orange dish ID
#         "main": "<spaghetti-ID>",  # Replace with actual spaghetti dish ID
#         "dessert": "<apple-pie-ID>"  # Replace with actual apple pie dish ID
#     }
#     response = post_request(f"{base_url}/meals", json_data)
#
#     assert response.json().get("code") == -2  # Code is -2
#     assert response.status_code in (400, 422)  # Return status code is 400 or 422
