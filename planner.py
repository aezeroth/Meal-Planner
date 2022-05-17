import json
import os
import random
from datetime import *

from units import *
import user_menu

RECIPES = {}
MEAL_PLAN = {}

sample = {
    'Mapo Tofu' : { 
        'ingredients' : {'tofu' : (1, Units.PACKS),
                        'ground pork' : (500, Units.GRAMS) },
        'meal times'  : [MealType.LUNCH, MealType.DINNER],
        'tags'        : ['asian', 'chinese', 'protein', 'spicy']
    }
}

MEALS_PER_DAY = 3
DAYS_TO_PLAN = 7
DAYS_WITH_UNIQUE_MEALS = 3

#TODO: plan just one day

def write_data(recipes, meal_plan):
    # write json recipe back to file
    with open('recipes.json', 'w') as recipe_book:
        json.dump(recipes, recipe_book, indent=4)

    with open('planner.json', 'w') as planner:
        json.dump(meal_plan, planner, indent=4)


def collect_data():
    recipes, meal_plan = {}, {}

    try:
        # read json recipe book from file
        with open('recipes.json', 'r',) as recipe_book:
            recipes = json.load(recipe_book)

        with open('planner.json', 'r',) as planner:
            meal_plan = json.load(planner)

    except json.JSONDecodeError:
        print('Valid .json file not found. Continuing wtihout reading...')

    return recipes, meal_plan



def add_recipe(recipes):
    '''
    Adds a recipe with user-inputted name, quantity, ingredients, meal times, and tags.

    @param recipes  Dictionary containing all existing recipes to append onto.
    '''
    name = str(input("Dish/Recipe name:"))

    info = {}
    info['ingredients'] = {}

    try:
        while True:
            ingredient_name = input('Ingredient name:').lower().strip()
            quantity = input('Quantity: ').split()
            units = ''
            if (len(quantity) >= 2):
                units = quantity[1].lower()
            amount = float(quantity[0])

            info['ingredients'][ingredient_name] = (amount, units)
        
            to_continue = input('Continue? (y/*)').lower()
            if to_continue == 'y':
                continue
            else:
                break

        info['meal times'] = input('Meal times?').lower().split()

        info['tags'] = input('Tags (separate by spaces):').lower().split()

        recipes[name] = info

    except (ValueError, IndexError):
        print('Invalid input. Try again...')

def remove_recipe(recipes):
    '''
    Removes a recipe by the given name.

    @param recipes Dictionary containing all existing recipes to remove from.
    '''
    try:
        print_recipes(recipes)
        
        choice = input('Select the recipe # you wish to delete:\n>> ')
        recipe = list(recipes.keys())[choice]

        del(recipes[recipe])

    except (KeyError, IndexError):
        print('Recipe does not exist.')

def plan_meals(recipes):
    try:
        DAYS_WITH_UNIQUE_MEALS = int(input('How many days with unique meals do you want?'))
        MEALS_PER_DAY = int(input('How many meals do you eat per day?'))
    except ValueError:
        print('Error: invalid input.')
        return

    plan = {}
    too_recent = [None] * DAYS_WITH_UNIQUE_MEALS * MEALS_PER_DAY

    recipe_names = list(recipes.keys())

    if len(recipe_names) < len(too_recent):
        print('Not enough recipes to plan meals for {} days with unique meals and {} meals per day.'.format(DAYS_WITH_UNIQUE_MEALS, MEALS_PER_DAY))
        return
    
    def pick_meal(meal_type):
        # Track dishes traversed so we don't infinitely loop if there are no tags that include meal_type
        traversed = {}

        while True:
            dish = random.choice(recipe_names)
            traversed[dish] = recipes[dish]
            
            if dish in too_recent:
                continue
            if meal_type in recipes[dish]['tags']:
                too_recent.pop(0)
                too_recent.append(dish)
                return dish
            if traversed == recipes:
                print('Unable to find a valid {}.'.format(meal_type))
                return None

    # Make date object, start at next monday, cycle through each day in the week (modulo?), store into dict as date name
    # Dict fields: 
    #   - key = Day number
    #   - val = Tuple of (date object, [3 recipe items])
    meal_day = datetime.today()
    if meal_day.weekday() != 0:
        meal_day += timedelta(days = 7 - meal_day.weekday())

    for day in range(DAYS_TO_PLAN):
        breakfast = pick_meal(MealType.BREAKFAST)
        lunch = pick_meal(MealType.LUNCH)
        dinner = pick_meal(MealType.DINNER)

        plan[day] = (meal_day, [recipes[breakfast], recipes[lunch], recipes[dinner]])

        meal_day += timedelta(days=1)

    return plan

def print_recipes(recipes):
    recipe_names = list(recipes.keys())

    for idx, name in enumerate(recipe_names):
        print('{}. {}'.format(idx, name))

def get_shopping_list(meal_plan):
    return

def view_meal_plan(meal_plan):
    return


def user_phase(recipes, meal_plan):
    try:
        choice = input('>> ')

        if choice == '1':
            add_recipe(recipes)
        elif choice == '2':
            remove_recipe(recipes)
        elif choice == '3':
            MEAL_PLAN = plan_meals(recipes)
        elif choice == '4':
            print_recipes(recipes)
        elif choice == '5':
            get_shopping_list(meal_plan)
        elif choice == '6':
            view_meal_plan(meal_plan)

    except ValueError:
        print('Invalid input.')


def edit_item_recursive(item):
#     # use a stack queue
#     try:
#         stack = []

#         while True:
#             if item is None:
#                 return

#             if isinstance(item, dict):
#                 dict_list = list(item.keys())
#                 for idx, key in enumerate(dict_list):
#                     print('{}. {}'.format(idx, key))
#                 print('{}. Add item'.format(idx + 1))

#                 choice = int(input('Input number >> '))
                
#                 if choice == idx + 1:
#                     if item == RECIPES:
#                         add_recipe(RECIPES)
#                     else:
#                         # add flow
#                         ...
#                 else:
#                     item = item[dict_list[choice]]

#             elif isinstance(item, list):
#                 ...

#             else:
#                 print('')
#                 item = None

#     except (ValueError, IndexError):
#         print('Invalid choice.')
    return



def main():
    print(user_menu.START)

    (RECIPES, MEAL_PLAN) = collect_data()
    
    while True:
        # user does stuff
        user_phase(RECIPES, MEAL_PLAN)
        
        try:
            choice = input('Continue (y/n)')

            if (choice.lower() == 'y'):
                continue
            else:
                break

        except ValueError:
            print("Invalid input. Continuing regardless.")


    write_data(RECIPES, MEAL_PLAN)

    input('Press ENTER to quit:')

if __name__ == "__main__":
    main()

