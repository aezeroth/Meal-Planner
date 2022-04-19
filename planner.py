import json
import os
import units

def __init__():
    return

def main():
    sample = {
        'name' : 'Mapo Tofu',
        'ingredients' : {'tofu' : (1, units.PACKS),
                         'ground pork' : (500, units.GRAMS) }
    }

    recipes = None

    # read json recipe book from file
    with open('recipes.json', 'r',) as recipe_book:
        recipes = json.load(recipe_book)
        print(json.dumps(recipes, indent=4))

    # user does stuff

    # write json recipe back to file
    with open('recipes.json', 'w') as recipe_book:
        json.dump(sample, recipe_book, indent=4)

    input('Press ENTER to quit:')

if __name__ == "__main__":
    main()
