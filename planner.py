import json
import os
import random
import re
from datetime import *
from fractions import Fraction

from units import *
import user_menu

RECIPES = 'recipes'
MEAL_PLAN = 'meal_plan'
SHOPPING_LIST = 'shopping_list'

MEALS_PER_DAY = 3
DAYS_TO_PLAN = 7
DAYS_WITH_UNIQUE_MEALS = 3

sample = {
    'Mapo Tofu' : { 
        'ingredients' : {'tofu' : (1, Units.PACKS),
                        'ground pork' : (500, Units.GRAMS) },
        'meal times'  : [MealType.LUNCH, MealType.DINNER],
        'tags'        : ['asian', 'chinese', 'protein', 'spicy']
    }
}


#TODO: plan just one day

def write_data(data):
    # write json recipe back to file
    for field in data:
        with open("{}.json".format(field), 'w') as obj:
            json.dump(data[field], obj, indent=4)

def collect_data(data):

    def handle_json_read(filename):
        try:
            with open(filename, 'r',) as obj:
                return json.load(obj)
        except (json.JSONDecodeError, FileNotFoundError):
            print('Valid {} file not found. Continuing without reading...'.format(filename))

    for field in data:
        data[field] = handle_json_read('{}.json'.format(field))

def add_recipe(data):
    '''
    Adds a recipe with user-inputted name, quantity, ingredients, meal times, and tags.

    @param data     Dict containing a recipe book dict that contains all existing recipes to append onto
    '''
    try:
        recipes = data[RECIPES]
        name = str(input("Dish/Recipe name:"))

        info = {}
        info['ingredients'] = {}
        # Loop infinitely to add arbitrary # of ingredients
        while True:
            ingredient_name = input('Ingredient name:').lower().strip()
            quantity = input('Quantity: ')

            # Use regex to enforce correct formatting of input (eg. '0', '2 pcs', '3.4 grams', '1/4 cups', etc.)
            number = "\d+([\/|.]\d+){0,1}" # eg. 0, 1/4, 1.4 ...
            unit = "(\w|\s)*"              # eg. "pcs", "big cloves", "neatly sorted funions"
            test_str = "\A{}( {}){{0,1}}\Z".format(number, unit)
            if not bool(re.match(test_str, quantity)):
                print("Invalid quantity. Needs to be '<number> <units>' ")
                continue
            
            amount, unit = quantity.split(' ', 1)

            info['ingredients'][ingredient_name] = (amount, unit)
        
            # Loop infinitely to poll user for proper response to continue or not
            more_ingredients = False
            while True:
                to_continue = input('More ingredients? (y/n)').lower()
                if to_continue == 'y':
                    more_ingredients = True
                    break
                elif to_continue == 'n':
                    more_ingredients = False
                    break
                    
            if more_ingredients:
                continue
            else:
                break

        info['meal times'] = input('Meal times?').lower().replace(',','').split()

        info['tags'] = input('Tags (separate by spaces):').lower().split()

        recipes[name] = info

    except (ValueError, IndexError):
        print('Invalid input. Try again...')
    
    except(KeyError):
        print('FATAL error, no recipe book exists...')

def remove_recipe(data):
    '''
    Removes a recipe by the given name.

    @param data     Dict containing a recipes dict containing all existing recipes to remove from.
    '''
    try:
        recipes = data[RECIPES]
        print_recipes(data)
        
        choice = input('Select the recipe # you wish to delete:\n>> ')
        recipe = list(recipes.keys())[choice]

        del(recipes[recipe])

    except (KeyError, IndexError):
        print('Recipe does not exist.')
    
    except ValueError:
        print('Invalid choice.')

def gen_meal_plan(data):
    """
    Generates a new meal plan for the week, starting on the coming Monday.

    @param data     Dict containing recipes dict

    @return A tuple of:
            - Meal plan dict
            - Shopping list dict
    """
    try:
        recipes = data[RECIPES]
        DAYS_WITH_UNIQUE_MEALS = int(input('How many days with unique meals do you want?\n >> '))
        MEALS_PER_DAY = int(input('How many meals do you eat per day?\n >> '))
    except ValueError:
        print('Error: invalid input.')
        return
    except KeyError:
        print('FATAL error, recipe book does not exist...')
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
            if meal_type in recipes[dish]['meal times']:
                if len(too_recent) != 0:
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

        plan[day] = (meal_day.isoformat(), [(breakfast, recipes[breakfast]), (lunch, recipes[lunch]), (dinner, recipes[dinner])])

        meal_day += timedelta(days=1)

    # Record meal plan and its respective shopping list into data obj
    data[MEAL_PLAN] = plan
    
    gen_shopping_list(data)

    print() # newline

def gen_shopping_list(data):
    # TODO: if unit type isnt the same, just append onto list keyed by ingredient name; otherwise, add like units together
    try:
        meal_plan = data[MEAL_PLAN]
    except KeyError:
        print('FATAL error: meal plan does not exist...')
        return
    shopping_list = {}

    for day in meal_plan:
        dishes = meal_plan[day][1]
        for dish in dishes:
            dish_name = dish[0]
            dish_recipe = dish[1]
            ingredients = dish_recipe['ingredients']

            for i in ingredients:
                item = '{} {} ({})'.format(ingredients[i][0], ingredients[i][1], dish_name)
                # if ingredient already exists in this list, append quantity to its list
                if i in shopping_list:
                    # TODO: add like units together (fractions utilize the imported module)
                    shopping_list[i].append(item)
                else:
                    shopping_list[i] = [item]

    data[SHOPPING_LIST] = shopping_list



def print_recipes(data):
    try:
        recipes = data[RECIPES]
    except KeyError:
        print('FATAL error: recipe book does not exist...')

    recipe_names = list(recipes.keys())

    for idx, name in enumerate(recipe_names):
        print('{}. {}'.format(idx, name))

    input('Press ENTER to continue...')

def print_meal_plan(data):
    try:
        meal_plan = data[MEAL_PLAN]
    except KeyError:
        print('FATAL error: meal plan dict does not exist...')
        return

    for day_num in meal_plan:
        day = datetime.fromisoformat(meal_plan[day_num][0])
        dishes = meal_plan[day_num][1]
        
        datestring = day.strftime('%A %b %d %y')

        user_menu.print_meal_day(datestring, dishes)

def print_shopping_list(data):
    try:
        shopping_list = data[SHOPPING_LIST]
    except KeyError:
        print('FATAL error: meal plan does not exist...')
        return

    if shopping_list is None or len(shopping_list) == 0:
        print("Cannot print a shopping list that doesn't exist. Please generate a meal plan first.")
        return

    user_menu.print_shopping_list(shopping_list)

def exit_planner(data):
    write_data(data)
    quit()

def user_phase(data, options):

    while True:
        try:
            choice = int(input('>> ')) - 1

            # Index into list of function ptrs
            options[choice](data)

            print(user_menu.CHOICES)

        except (ValueError, KeyError):
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
    # refer to user_menu.py for ordering
    OPTIONS = [add_recipe, 
               remove_recipe, 
               gen_meal_plan, 
               print_recipes, 
               print_shopping_list,
               print_meal_plan,
               exit_planner]

    print(user_menu.START)

    DATA = { RECIPES : None,
             MEAL_PLAN : None,
             SHOPPING_LIST : None }
    
    collect_data(DATA)

    # user does stuff
    user_phase(DATA, OPTIONS)

if __name__ == "__main__":
    main()

