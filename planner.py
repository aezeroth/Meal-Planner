import json
import os

import units
import user_menu

def __init__():
    return

def main():
    sample = {
        'name' : 'Mapo Tofu',
        'ingredients' : {'tofu' : (1, units.PACKS),
                         'ground pork' : (500, units.GRAMS) }
    }

    recipes = {}

    try:
        # read json recipe book from file
        with open('recipes.json', 'r',) as recipe_book:
            recipes = json.load(recipe_book)
    except json.JSONDecodeError:
        print('Valid .json file not found. Continuing wtihout reading...')

    # user does stuff
    print(user_menu.START)

    # write json recipe back to file
    with open('recipes.json', 'w') as recipe_book:
        json.dump(sample, recipe_book, indent=4)

    input('Press ENTER to quit:')

if __name__ == "__main__":
    main()
