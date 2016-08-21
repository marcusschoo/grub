import grub

class Recipe:

	def __init__(self, name, directions):
		self.name = name
		self.directions = directions
		self.ingredients = []
		self.id = None

class Product:

	def __init__(self, name, measure=Measure.kVolume):
		self.name = name
		self.measure = measure
		self.id = None
		self.category = 'tins'

class Store:

	def __init__(self, name):
		self.name = name
		self.category_order = ['fresh produce','tins','freezer']

class Measure:

	def __init__(self):
		self.kVolume = 0
		self.kWeight = 1
		self.kUnits = 2

class Ingredient:

	def __init__(self, product, amount, unit=kCup):
		self.product = product
		self.amount = amount
		self.unit = unit
		#validate unit against product measure

grub_db = grub.read('path/grub.plist')

new_recipe = Recipe(name='foo', directions='something')
grub_db.save_recipe(new_recipe)
# info: new recipe created
cumin = grub_db.get_product_by_name('cumin')
if not cumin:
	cumin = Product('cumin', kVolume)
	grub_db.save_product(cumin)
new_recipe.add_ingredient(Ingredient(cumin, 1, Unit.kTsp))
grub_db.save_recipe(new_recipe)
# info: recipe updated

new_recipe = Recipe(name='foo', directions='something')
new_recipe.add_ingredient(Ingredient(grub_db.get_product_by_name('cumin'), 1, Unit.kTsp))
grub_db.save_recipe(new_recipe)
# info: recipe saved

import argparse
import plistlib
import uuid

FILE_PATH = './recipes.plist'

def save():
    plistlib.writePlist(db, FILE_PATH)

def printNames(db):
    for r in recipes:
        print r['NAME']

def parseMenu( file ):
    menu = []
    index = 0
    for l in file.readlines():
        if l.startswith('y '):
            menu.append(index)
        index = index + 1
    return menu

def printMenu(path_to_menu,db):
    indices = parseMenu(path_to_menu)
    for index in indices:
        print '==============================='
        print db[index]['NAME']
        print '-------------------------------'
        for i in db[index]['INGREDIENTS']:
            print i['QUANTITY'], i['MEASUREMENT'], i['DESCRIPTION'], i['DIRECTION']
        print '-------------------------------'
        print db[index]['DIRECTIONS']
    print '==============================='

def assign_recipe_ids(db):
    for r in db:
        id = r.get('RECIPE_ID', None)
        if not id:
            r['RECIPE_ID'] = str(uuid.uuid4())

def getCollectionMembership(id):
    result = ''
    for c in collections:
        if id in c['RECIPES']:
            result += 'Y'
        else:
            result += '-'
    return result

'''
Print 'add recipies to collections' form
'''
def printCollections():
    for c in collections:
        name = c['NAME']
        print '#', name
    print '#'
    for r in recipes:
        id = r.get('RECIPE_ID', None)
        if id:
            print getCollectionMembership(id), r.get('NAME')

'''
Import 'add recipies to collections' form from file
'''
def importCollections(file):
    for c in collections:
        c['RECIPES'] = []
    ri = 0
    for l in file.readlines():
        if l.startswith('#'):
            continue
        ci = 0
        for c in collections:
            if l[ci] == 'Y':
                c['RECIPES'].append(recipes[ri]['RECIPE_ID'])
            ci += 1
        ri += 1

'''
Find recipe by recipe ID
'''
def findRecipeById(id):
    for recipe in recipes:
        if recipe['RECIPE_ID'] == id:
            return recipe
    return None

'''
Find recipe by recipe name
'''
def findRecipeByName(name):
    for recipe in recipes:
        if recipe['NAME'] == name:
            return recipe
    return None

'''
Print 'shopping list' form
'''
def printShoppingListForm():
    for c in collections:
        print '#', c['NAME']
        for r in c['RECIPES']:
            print findRecipeById(r)['NAME']

'''
Generate and print shopping list from 'shopping list' form from file
'''
def printShoppingListFromForm(file):
    for line in file.readlines():
        if line.startswith('y '):
            recipe = findRecipeByName(line[2:-1])
            for ingredient in recipe['INGREDIENTS']:
                print ingredient['QUANTITY'], ingredient['MEASUREMENT'], ingredient['DESCRIPTION']

db=plistlib.readPlist(FILE_PATH)
recipes = db['RECIPES']
collections = db['COLLECTIONS']

argparser = argparse.ArgumentParser(description="Command line recipe tool.")
argparser.add_argument('-r','--recipes', dest='print_all_recipes', action='store_true',
                       help='print a list of all recipes')
argparser.add_argument('-c','--custom', dest='custom', action='store_true',
                       help='custom operation, changes frequently')
argparser.add_argument('-i','--customInput', dest='custom_input', action='store',
                       type=argparse.FileType('r'),
                       help='Like custom but with file argument')
argparser.add_argument('-s','--shoppinglist', dest='selected_recipes', action='store',
                       type=argparse.FileType('r'),
                       help='read in a file with selected recipes marked with "y " at the start of line and generate shopping list')
args = argparser.parse_args()

if args.print_all_recipes:
    printNames(db)
elif args.selected_recipes:
    printMenu(args.selected_recipes,db)
elif args.custom:
    #plistlib.writePlist({'RECIPES': db}, FILE_PATH)
    #printCollections()
    printShoppingListForm()
elif args.custom_input:
    #importCollections(args.custom_input)
    #save()
    printShoppingListFromForm(args.custom_input)

