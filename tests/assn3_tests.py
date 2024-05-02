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
    print("dish col is:", response_json)
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
    # asserts the returned code is 200
    assert_status_code(response, status_code=200)
    meals = response.json()
    # asserts the length of meals collection is 1
    assert len(meals) == 1
    for meal in meals.values():
        if meal.get("name") == "delicious":
            # asserts the meal calories value is in required range
            assert (400 <= meal["cal"] <= 500)


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
    # asserts the meal exists in collection meaning that posting returns -2 and that the status codes are 400 or 422
    assert_item_exists(response, [400, 422])
