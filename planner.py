import json
import os

from units import *
import user_menu


sample = {
    'Mapo Tofu' : { 
        'ingredients' : {'tofu' : (1, Units.PACKS),
                        'ground pork' : (500, Units.GRAMS) },
        'meal times'  : [MealType.LUNCH, MealType.DINNER],
        'tags'        : ['asian', 'chinese', 'protein', 'spicy']
    }
}


def __init__():
    return


def add_recipe(recipes):
    name = str(input("Dish/Recipe name:"))

    info = {}
    info['ingredients'] = {}

    try:
        while True:
            ingredient_name = input('Ingredient name:').lower()
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


def edit_recipes(recipes):
    recipe_names = list(recipes.keys())

    try:
        choice = int(input('Remove (0) or edit (1)?'))

        print('Type the number of the recipe name you wish to select:')

        for idx, name in enumerate(recipe_names):
            print('{}. {}'.format(idx, name))
    
        edit_idx = int(input('>> '))

        if choice == 0:
            del recipes[recipe_names[edit_idx]]
            return
        elif choice == 1:
            print("""
                
                 1. Ingredients
                 2. Meal times
                 3. Tags
                 """)
            return
        else:
            print('Invalid edit option.')
            return

    except (ValueError, IndexError):
        print('Invalid input.')



def edit_item_recursive(item):
    try:
        while True:
            if item is None:
                return

            if isinstance(item, dict):
                dict_list = list(item.keys())
                for idx, key in enumerate(dict_list):
                    print('{}. {}'.format(idx, key))

            elif isinstance(item, list):
                ...

            else:
                item = None
                
    except (ValueError, IndexError):
        print('Invalid choice.')




def collect_data():
    recipes = {}

    try:
        # read json recipe book from file
        with open('recipes.json', 'r',) as recipe_book:
            recipes = json.load(recipe_book)

    except json.JSONDecodeError:
        print('Valid .json file not found. Continuing wtihout reading...')

    return recipes


def user_phase(recipes):
    print(user_menu.START)

    try:
        choice = input('>> ')

        if choice == '1':
            add_recipe(recipes)
        elif choice == '2':
            edit_recipes(recipes)

    except ValueError:
        print('Invalid input.')


def write_data(recipes):
    # write json recipe back to file
    with open('recipes.json', 'w') as recipe_book:
        json.dump(recipes, recipe_book, indent=4)




def main():
    recipes = collect_data()

    # user does stuff
    user_phase(recipes)

    write_data(recipes)

    input('Press ENTER to quit:')

if __name__ == "__main__":
    main()
