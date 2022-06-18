import datetime
import pprint

# console for now
current_date = datetime.datetime.now().strftime('%A %B %d, %Y')

LIST_OF_CHOICES = ['ADD a recipe', 
                   'REMOVE a recipe', 
                   'GENERATE a new MEAL PLAN for the week!',
                   'VIEW RECIPE book', 
                   'VIEW SHOPPING LIST', 
                   'VIEW current MEAL PLAN', 
                   'SAVE & EXIT']

CHOICES = "".join(["{}. {}\n".format(i+1, LIST_OF_CHOICES[i]) for i in range(len(LIST_OF_CHOICES))])

START = """ 
        
░██╗░░░░░░░██╗███████╗██╗░░░░░░█████╗░░█████╗░███╗░░░███╗███████╗  ████████╗░█████╗░  ████████╗██╗░░██╗███████╗
░██║░░██╗░░██║██╔════╝██║░░░░░██╔══██╗██╔══██╗████╗░████║██╔════╝  ╚══██╔══╝██╔══██╗  ╚══██╔══╝██║░░██║██╔════╝
░╚██╗████╗██╔╝█████╗░░██║░░░░░██║░░╚═╝██║░░██║██╔████╔██║█████╗░░  ░░░██║░░░██║░░██║  ░░░██║░░░███████║█████╗░░
░░████╔═████║░██╔══╝░░██║░░░░░██║░░██╗██║░░██║██║╚██╔╝██║██╔══╝░░  ░░░██║░░░██║░░██║  ░░░██║░░░██╔══██║██╔══╝░░
░░╚██╔╝░╚██╔╝░███████╗███████╗╚█████╔╝╚█████╔╝██║░╚═╝░██║███████╗  ░░░██║░░░╚█████╔╝  ░░░██║░░░██║░░██║███████╗
░░░╚═╝░░░╚═╝░░╚══════╝╚══════╝░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚══════╝  ░░░╚═╝░░░░╚════╝░  ░░░╚═╝░░░╚═╝░░╚═╝╚══════╝

███╗░░░███╗███████╗░█████╗░██╗░░░░░  ██████╗░██╗░░░░░░█████╗░███╗░░██╗███╗░░██╗███████╗██████╗░██╗
████╗░████║██╔════╝██╔══██╗██║░░░░░  ██╔══██╗██║░░░░░██╔══██╗████╗░██║████╗░██║██╔════╝██╔══██╗██║
██╔████╔██║█████╗░░███████║██║░░░░░  ██████╔╝██║░░░░░███████║██╔██╗██║██╔██╗██║█████╗░░██████╔╝██║
██║╚██╔╝██║██╔══╝░░██╔══██║██║░░░░░  ██╔═══╝░██║░░░░░██╔══██║██║╚████║██║╚████║██╔══╝░░██╔══██╗╚═╝
██║░╚═╝░██║███████╗██║░░██║███████╗  ██║░░░░░███████╗██║░░██║██║░╚███║██║░╚███║███████╗██║░░██║██╗
╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚══════╝  ╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝╚═╝!

It is currently {}.

{}
""".format(current_date, CHOICES)

EDIT_OPTIONS = """
1. Ingredients
2. Meal times
3. Tags
"""


def print_meal_day(datestring, dishes):
    meal_day = "{}:\n\t".format(datestring)
    for dish in dishes:
        meal_day += "{}\n\t".format(dish)
    print(meal_day)


def print_shopping_list(shopping_list):
    #TODO: sort alphabetically; format <Ingr. name>: [<#> <unit_0>, <#> <unit_1>, ...]
    print('\nSHOPPING LIST')
    for item in shopping_list:
        str = "  - {}\n\t+ ".format(item.title())
        for idx, unit in enumerate(shopping_list[item]):
            str += "{} {}".format(shopping_list[item][unit], unit)
            if idx < len(shopping_list[item]) - 1:
                str += ","
            str += " "
        print(str)