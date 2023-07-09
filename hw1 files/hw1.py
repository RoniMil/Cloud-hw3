from flask import Flask, request
from flask_restful import Resource, Api
import requests
import json

app = Flask(__name__)  # init Flask
api = Api(app)  # create API

# api key yy9bB6DaWfScfi2eDNI6PQ==w9MfBQ2l3ZfXQhgm

# Class DishCollection provides CRUD ops on dishes.
class DishCollection:
    def __init__(self):
        self.opNumDishes = 0  # Keeps count of the number of operations performed on the collection. Is used to give unique IDs to added dishes
        self.dishes = {}  # The entire collection of dishes

    # adds new dish to the collection. The string given will be the dish's name. If successful returns the dish ID. Otherwise, returns 0
    def addDish(self, dishName, cal, size, sodium, sugar):  # ???signature change???
        for dish in self.dishes.values():
            # checks if dish is already in collection
            if dish.get('name') == dishName:
                print("DishCollection: dish ", dishName, " already exists")
                return 0
        self.opNumDishes += 1
        id = self.opNumDishes
        newDish = {
            "name": dishName,
            "ID": id,
            "cal": cal,
            "size": size,
            "sodium": sodium,
            "sugar": sugar
        }
        self.dishes[id] = newDish
        print("DishCollection: inserted dish ", dishName, " with id ", id)
        return id

    # returns a dish given its ID (int)
    def getDishByID(self, dishID):
        # checks if the dish exists in collection
        for dish in self.dishes.values():
            if dish['ID'] == dishID:
                print("DishCollection: retrieved dish with ID ", dishID)
                return dish
        print("DishCollection: dish with ID ", dishID, " not found")
        return 0

    # returns a dish given its name (String)
    def getDishByName(self, dishName):
        for dish in self.dishes.values():
            if dish['name'] == dishName:
                print("DishCollection: retrieved dish with name ", dishName)
                return dish
        print("DishCollection: dish with name ", dishName, " not found")
        return 0

    def getDishIDByName(self, dishName):
        for id, dish in self.dishes.items():
            if dish['name'] == dishName:
                return id
        return 0

    # deletes a dish given its ID (int) from the collection. Returns the ID of the deleted dish.
    def deleteDishByID(self, dishID):
        for dish in self.dishes.values():
            if dish['ID'] == dishID:
                del self.dishes[dishID]
                print("DishCollection: deleted dish with ID ", dishID)
                return dishID
        print("DishCollection: dish with ID ", dishID, " not found")
        return 0

    # deletes a dish given its name (String) from the collection. Returns the name of the deleted dish.
    def deleteDishByName(self, dishName):
        for id, dish in self.dishes.items():
            if dish['name'] == dishName:
                del self.dishes[id]
                print("DishCollection: deleted dish with name ", dishName)
                return id
        print("DishCollection: dish with name ", dishName, " not found")
        return 0

    # returns the entire collection of dishes
    def getAllDishes(self):
        print("DishCollection: retrieving all dishes:")
        print(self.dishes)
        return self.dishes

    # checks whether a dish of the given ID exists in the collection
    def isDishInCol(self, dishID):
        for dish in self.dishes.values():
            if dish['ID'] == dishID:
                return True
        return False

    # if dish has more than one component, update it s.t the values are a sum of the components
    def processJson(self, dishFile):
        new_calories, new_size, new_sodium, new_sugar = 0, 0, 0, 0
        for dish in dishFile:
            new_calories += dish['calories']
            new_size += dish['serving_size_g']
            new_sodium += dish['sodium_mg']
            new_sugar += dish['sugar_g']
        new_dish = {
            "calories": new_calories,
            "serving_size_g": new_size,
            "sodium_mg": new_sodium,
            "sugar_g": new_sugar
        }
        return new_dish


colDishes = DishCollection()


# Class MealCollection provides CRUD ops on meals.

class MealCollection:
    def __init__(self):
        self.opNumMeals = 0  # Keeps count of the number of operations performed on the collection. Is used to give unique IDs to added dishes
        self.meals = {}  # The entire collection of meals

    # adds new meal to the collection given its name and 3 dishes s.t the 1st is the appetizer, the 2nd is the main and the 3rd is the dessert.
    def addMeal(self, mealName, appetizer, main, dessert):
        if mealName in [meal["name"] for meal in self.meals.values()]:
            print("MealCollection: meal ", mealName, " already exists")
            return 0
        self.opNumMeals += 1
        id = self.opNumMeals
        newMeal = {
            "name": mealName,
            "ID": id,
            "appetizer": appetizer['ID'],
            "main": main['ID'],
            "dessert": dessert['ID'],
            "cal": appetizer['cal'] + main['cal'] + dessert['cal'],
            "sodium": appetizer['sodium'] + main['sodium'] + dessert['sodium'],
            "sugar": appetizer['sugar'] + main['sugar'] + dessert['sugar']
        }
        self.meals[id] = newMeal
        print("MealCollection: created meal ", mealName, " with id ", id, " with dishes: ", appetizer['name'], " ",
              main['name'], " and ", dessert['name'])
        return id

    # returns JSON of a meal given its ID (int)
    def getMealByID(self, mealID):
        for meal in self.meals.values():
            if meal['ID'] == mealID:
                print("MealCollection: retrieved meal with ID ", mealID)
                return meal
        print("MealCollection: meal with ID ", mealID, " not found")
        return 0

    # returns JSON of a meal given its name (String)
    def getMealByName(self, mealName):
        for meal in self.meals.values():
            if meal['name'] == mealName:
                print("MealCollection: retrieved meal with name ", mealName)
                return meal
        print("MealCollection: meal with name ", mealName, " not found")
        return 0

    # Updates an existing meal in the collection given its ID and new dishes
    def updateMeal(self, mealID, new_name, new_appetizer, new_main, new_dessert):
        meal = self.getMealByID(mealID)
        meal['name'] = new_name
        meal['appetizer'] = new_appetizer['ID']
        meal['main'] = new_main['ID']
        meal['dessert'] = new_dessert['ID']
        meal['cal'] = new_appetizer['cal'] + new_main['cal'] + new_dessert['cal']
        meal['sodium'] = new_appetizer['sodium'] + new_main['sodium'] + new_dessert['sodium']
        meal['sugar'] = new_appetizer['sugar'] + new_main['sugar'] + new_dessert['sugar']

    # deletes a meal given its ID (int) from the collection. Returns the ID of the deleted meal.
    def deleteMealByID(self, mealID):
        for meal in self.meals.values():
            if meal['ID'] == mealID:
                del self.meals[mealID]
                print("MealCollection: deleted meal with ID ", mealID)
                return mealID
        print("MealCollection: meal with ID ", mealID, " not found")
        return 0

    # deletes a meal given its name (String) from the collection. Returns the name of the deleted meal.
    def deleteMealByName(self, mealName):
        for id, meal in self.meals.items():
            if meal['name'] == mealName:
                del self.meals[id]
                print("MealCollection: deleted meal with name ", mealName)
                return id
        print("MealCollection: meal with name ", mealName, " not found")
        return 0

    # returns the entire collection of meals
    def getAllMeals(self):
        print("MealCollection: retrieving all meals:")
        print(self.meals)
        return self.meals


colMeals = MealCollection()


# The Dishes class implements the REST operations for the /dishes resource
class Dishes(Resource):
    global colDishes

    # adds a dish of the given name to the /dishes collection. If successful, returns the dish ID (positive int)
    def post(self):
        # checks if request content type is application/json
        if request.content_type != 'application/json':
            return 0, 415
        data = request.get_json()
        # checks if the request parameters are valid
        if 'name' not in data:
            return -1, 422
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(data['name'])
        response = requests.get(api_url, headers={'X-Api-Key': 'yy9bB6DaWfScfi2eDNI6PQ==w9MfBQ2l3ZfXQhgm'})
        status = response.status_code
        response_data = json.loads(response.text)
        # there was something wrong with the request to ninja api
        if status != requests.codes.ok:
            # api ninja is unreachable.
            if status == 504:
                return -4, 504
        # api ninja doesn't recognize dish name.
        if not response_data:
            return -3, 422
        dish_name = data['name']
        dish_info = colDishes.processJson(response_data)
        cal, size = dish_info['calories'], dish_info['serving_size_g']
        sodium, sugar = dish_info['sodium_mg'], dish_info['sugar_g']
        add_response = colDishes.addDish(dish_name, cal, size, sodium, sugar)
        # checks if dish is already in collection.
        if add_response == 0:
            return -2, 422
        return add_response, 201

    # returns the JSON object listing all dishes in the collection
    def get(self):
        return colDishes.getAllDishes(), 200

    # !!! delete /dishes? !!!


# The Dishes class implements the REST operations for the /dishes/{ID} resource
class DishID(Resource):
    global colDishes

    # returns the dish JSON that matches to the given dish ID.
    def get(self, dishID):
        res = colDishes.getDishByID(dishID)
        if res == 0:
            return -5, 404
        return res, 200

    # deletes the dish that matches to the given dish ID. If successful, returns the ID of the deleted dish. Also updates the meals that contain the deleted dish
    def delete(self, dishID):
        status = colDishes.deleteDishByID(dishID)
        if status == 0:
            return -5, 404
        for meal in colMeals.meals.values():
            if meal["appetizer"] == dishID:
                meal["appetizer"] = None
                meal["cal"] = None
                meal["sodium"] = None
                meal["sugar"] = None
            if meal["main"] == dishID:
                meal["main"] = None
                meal["cal"] = None
                meal["sodium"] = None
                meal["sugar"] = None
            if meal["dessert"] == dishID:
                meal["dessert"] = None
                meal["cal"] = None
                meal["sodium"] = None
                meal["sugar"] = None
        return status, 200


# The Dishes class implements the REST operations for the /dishes/{name} resource
class DishName(Resource):
    global colDishes

    # returns the dish JSON that matches to the given dish name.
    def get(self, dishName):
        res = colDishes.getDishByName(dishName)
        if res == 0:
            return -5, 404
        return res, 200

    # deletes the dish that matches to the given dish name. If successful, returns the ID of the deleted dish.
    def delete(self, dishName):
        status = colDishes.deleteDishByName(dishName)
        dishID = colDishes.getDishIDByName(dishName)
        if status == 0:
            return -5, 404
        for meal in colMeals.meals:
            if meal["appetizer"] == dishID:
                meal["appetizer"] = None
                meal["cal"] -= None
                meal["sodium"] -= None
                meal["sugar"] -= None
            if meal["main"] == dishID:
                meal["main"] = None
                meal["cal"] -= None
                meal["sodium"] -= None
                meal["sugar"] -= None
            if meal["dessert"] == dishID:
                meal["dessert"] = None
                meal["cal"] -= None
                meal["sodium"] -= None
                meal["sugar"] -= None
        return status, 200


# The Meals class implements the REST operations for the /meals resource
class Meals(Resource):
    global colMeals

    def post(self):
        # checks if request content type is application/json
        if request.content_type != 'application/json':
            return 0, 415
        data = request.get_json()
        # checks if the request parameters are valid
        if 'name' not in data or 'appetizer' not in data or 'main' not in data or 'dessert' not in data:
            return -1, 422
        meal_name = data['name']
        appetizerID, mainID, dessertID = data['appetizer'], data['main'], data['dessert']
        # checks if all dishes specific in the request exist in the collection (s.t they have an id)
        if colDishes.isDishInCol(appetizerID) and colDishes.isDishInCol(
                mainID) and colDishes.isDishInCol(dessertID):
            appetizer, main, dessert = colDishes.getDishByID(appetizerID), colDishes.getDishByID(
                mainID), colDishes.getDishByID(dessertID)
            res = colMeals.addMeal(meal_name, appetizer, main, dessert)
            # checks if a meal of the same name as meal_name exists in the collection already
            if res == 0:
                return -2, 422
            return res, 201
        return -6, 422

    # returns JSON object listing all the meals in the collection.
    def get(self):
        return colMeals.getAllMeals(), 200


# The MealsID class implements the REST operations for the /meals/{ID} resource
class MealID(Resource):
    global colMeals

    # returns the meal JSON that matches to the given meal ID.
    def get(self, mealID):
        res = colMeals.getMealByID(mealID)
        if res == 0:
            return -5, 404
        return res, 200

    # deletes the meal that matches to the given meal ID. If successful, return the ID of the deleted meal.
    def delete(self, mealID):
        res = colMeals.deleteMealByID(mealID)
        if res == 0:
            return -5, 404
        return res, 200

    # updates the meal that matches to the given meal ID.
    def put(self, mealID):
        # checks if request content type is application/json
        if request.content_type != 'application/json':
            return 0, 415
        if mealID not in [meal["ID"] for meal in colMeals.meals.values()]:
            return -5, 404
        data = request.get_json()
        # checks if the request parameters are valid
        if 'name' not in data or 'appetizer' not in data or 'main' not in data or 'dessert' not in data:
            return -1, 422
        meal_name = data['name']
        appetizerID, mainID, dessertID = data['appetizer'], data['main'], data['dessert']
        # checks if all dishes specific in the request exist in the collection (s.t they have an id)
        if colDishes.isDishInCol(appetizerID) and colDishes.isDishInCol(
                mainID) and colDishes.isDishInCol(dessertID):
            appetizer, main, dessert = colDishes.getDishByID(appetizerID), colDishes.getDishByID(
                mainID), colDishes.getDishByID(dessertID)
            colMeals.updateMeal(mealID, meal_name, appetizer, main, dessert)
            return mealID, 200
        return -6, 422


# The Dishes class implements the REST operations for the /meals/{name} resource
class MealName(Resource):
    global colMeals

    # returns the meal JSON that matches to the given meal name.
    def get(self, mealName):
        res = colMeals.getMealByName(mealName)
        if res == 0:
            return -5, 404
        return res, 200

    # deletes the meal that matches to the given meal name. If successful, return the ID of the deleted meal.
    def delete(self, mealName):
        res = colMeals.deleteMealByName(mealName)
        if res == 0:
            return -5, 404
        return res, 200


# Dishes is the collection of available dishes. Each dish has a unique name and ID number. Associated with '/dishes'.
# DishID is the unique ID number given to each dish in Dishes collection. Associated with '/dishes/{ID}'.
# DishName is the unique name given to each dish in Dishes collection. Associated with '/dishes/{name}'.
# Meals is the collection of available meals. A meal is made of 3 dishes (entree, main and dessert). Each meal has a unique name and ID number. Associated with '/meals'.
# MealID is the unique ID number given to each meal in Meals collection. Associated with '/meals/{ID}'.
# MealName is the unique name given to each meal in Meals collection. Associated with '/meals/{name}.

api.add_resource(Dishes, '/dishes')
api.add_resource(DishID, '/dishes/<int:dishID>')
api.add_resource(DishName, '/dishes/<string:dishName>')
api.add_resource(Meals, '/meals')
api.add_resource(MealID, '/meals/<int:mealID>')
api.add_resource(MealName, '/meals/<string:mealName>')

if __name__ == '__main__':
    # create collection dictionary and keys list
    print("running HW1.py")

