import json
import os

from units import *
import user_menu


sample = {
    'Mapo Tofu' : { 
        'ingredients' : {'tofu' : (1, Units.PACKS),
                        'ground pork' : (500, Units.GRAMS) },
        'meal types' : [MealType.LUNCH, MealType.DINNER]
    }
}


def __init__():
    return


def add_recipe(recipes):
    name = input("Recipe name:")
    ingredients = {}


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


def write_data(recipes):
    # write json recipe back to file
    with open('recipes.json', 'w') as recipe_book:
        json.dump(sample, recipe_book, indent=4)




def main():
    recipes = collect_data()

    # user does stuff
    user_phase(recipes)

    write_data(recipes)

    input('Press ENTER to quit:')

if __name__ == "__main__":
    main()
